import argparse
import sys
import os
import pickle
sys.modules['dtsr'] = __import__('cdr') # Hack for backward compatibility
from cdr.config import Config
from cdr.model import CDREnsemble
from cdr.util import filter_models, stderr

if __name__ == '__main__':
    argparser = argparse.ArgumentParser('''
        Compute root mean squared deviation of fitted IRFs from gold synthetic IRFs.
    ''')
    argparser.add_argument('paths', nargs='+', help='Path(s) to config file(s) defining experiments')
    argparser.add_argument('-m', '--models', nargs='*', default = [], help='Model names for which to compute RMSD. Regex permitted. If unspecified, uses all CDR models.')
    argparser.add_argument('-n', '--n_samples', type=int, default=None, help='Number of samples to draw. If unspecified, use MLE/MAP.')
    argparser.add_argument('--cpu_only', action='store_true', help='Use CPU implementation even if GPU is available.')
    args = argparser.parse_args()

    n_samples = args.n_samples

    for path in args.paths:
        p = Config(path)

        if not p.use_gpu_if_available or args.cpu_only:
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

        model_list = sorted(set(p.model_list) | set(p.ensemble_list))
        models = filter_models(model_list, args.models, cdr_only=True)

        synth_path = os.path.dirname(os.path.dirname(p.X_train)) + '/d.obj'
        if not os.path.exists(synth_path):
            raise ValueError('Path to synth data %s does not exist. Check to make sure that model is fitted to synthetic data and that paths are correct in the config file.')
        with open(synth_path, 'rb') as f:
            d = pickle.load(f)
        def gold_irf_lambda(x):
            return d.irf(x, coefs=True)

        for m in models:
            p.set_model(m)
            formula = p.models[m]['formula']
            m_path = m.replace(':', '+')

            stderr('Retrieving saved model %s...\n' % m)
            cdr_model = CDREnsemble(p.outdir, m_path)

            stderr('Computing RMSD...\n')

            rmsd_mean, rmsd_lower, rmsd_upper, rmsd_samples = cdr_model.irf_rmsd(
                gold_irf_lambda,
                n_samples=n_samples
            )

            summary = '=' * 50 + '\n'
            summary += 'CDR regression\n\n'
            summary += 'Model name: %s\n\n' % m
            summary += 'Formula:\n'
            summary += '  ' + formula + '\n\n'
            summary += 'Path to synth model:\n'
            summary += '  ' + synth_path + '\n\n'
            summary += 'RMSD from gold: %s\n'
            summary += '  Mean:  %s\n' % rmsd_mean[cdr_model.response_names[0]]['mean']
            summary += '  2.5%%:  %s\n' % rmsd_lower[cdr_model.response_names[0]]['mean']
            summary += '  97.5%%: %s\n' % rmsd_upper[cdr_model.response_names[0]]['mean']
            summary += '=' * 50 + '\n'

            out_name = 'synth_rmsd'

            with open(p.outdir + '/' + m_path + '/' + out_name + '.txt', 'w') as f:
                f.write(summary)
            sys.stdout.write(summary)



