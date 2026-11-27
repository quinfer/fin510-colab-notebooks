"""Validate Lab 3 from repo root, labs and an isolated Colab-like directory.

python scripts/validate_price_dividend.py            # fresh Python per run
python scripts/validate_price_dividend.py --jupyter  # fresh Jupyter kernels

Neither mode claims to execute on Google's Colab service. The isolated run
exercises the notebook's unchanged public HTTP data fallback without a loader.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'labs/lab03_price_dividend.ipynb'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jupyter', action='store_true')
    args = parser.parse_args()
    nbformat.validate(nbformat.read(NOTEBOOK, as_version=4))
    outputs = ROOT / 'validation'
    outputs.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        runner = tmp / 'execute.py'
        # All notebook cells run in order in a new interpreter, no shared modules.
        runner.write_text('''import json, sys
from pathlib import Path
nb = json.loads(Path(sys.argv[1]).read_text())
ns = {}
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        exec(compile(''.join(cell['source']), f'<notebook cell {i}>', 'exec'), ns)
if len(sys.argv) > 2:
    ns['comparison'].to_csv(sys.argv[2], index=False)
''')
        runs = {}
        for label, cwd in [('repo_root', ROOT), ('labs', ROOT / 'labs'), ('isolated_remote', tmp)]:
            if args.jupyter:
                from nbclient import NotebookClient
                from jupyter_client import KernelManager
                from jupyter_client.kernelspec import KernelSpecManager
                kernels = tmp / 'kernels'
                spec = kernels / 'lab3-validation'
                spec.mkdir(parents=True, exist_ok=True)
                (spec / 'kernel.json').write_text(json.dumps({
                    'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                    'display_name': 'Lab 3 validation', 'language': 'python'}))
                manager = KernelManager(kernel_name='lab3-validation',
                    kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernels)]))
                nb = nbformat.read(NOTEBOOK, as_version=4)
                NotebookClient(nb, km=manager, timeout=120,
                    resources={'metadata': {'path': str(cwd)}}).execute()
            command = [sys.executable, str(runner), str(NOTEBOOK)]
            if label == 'repo_root':
                command.append(str(outputs / 'lab03_regression_comparison.csv'))
            env = {**os.environ, 'MPLBACKEND': 'Agg'}
            # Do not inherit any caller's course-code import paths in isolated mode.
            env.pop('PYTHONPATH', None)
            subprocess.run(command, cwd=cwd, env=env, check=True, timeout=120)
            runs[label] = 'passed'
            print(label, 'passed', flush=True)
        versions = {name: importlib.metadata.version(name) for name in
                    ('pandas', 'numpy', 'statsmodels', 'pyarrow', 'matplotlib', 'nbformat', 'nbclient')}
        report = {'python': platform.python_version(), 'packages': versions,
                  'mode': 'jupyter and fresh Python' if args.jupyter else 'fresh Python',
                  'execution': runs, 'notebook_schema': 'passed',
                  'notebook_sha256': hashlib.sha256(NOTEBOOK.read_bytes()).hexdigest(),
                  'extract_sha256': hashlib.sha256((ROOT / 'resources/price_dividend_ratio.parquet').read_bytes()).hexdigest(),
                  'jupyter_kernel': 'passed' if args.jupyter else 'not run in this mode',
                  'google_colab_service': 'not run; isolated_remote tests no-local-loader HTTP fallback'}
        (outputs / 'lab03_execution.json').write_text(json.dumps(report, indent=2) + '\n')

if __name__ == '__main__':
    main()
