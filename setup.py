import sys
import subprocess
import pkg_resources
import platform

required = {'numpy', 'pymorphy2', 'torch', 'pandas', 'ntplib', 'pathlib'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

params = [
    {
        "arg": "--trusted-host",
        "value": "pypi.python.org"
    },
    {
        "arg": "--trusted-host",
        "value": "pypi.org"
    },
    {
        "arg": "--trusted-host",
        "value": "files.pythonhosted.org"
    }
]

config = {
    'Windows': {
        'torch': 'https://download.pytorch.org/whl/cpu/torch-0.4.1-cp37-cp37m-win_amd64.whl'
    },
}

args = []

for i, p in enumerate(params):
    args.append(p['arg'])
    args.append(p['value'])

for package in missing:
    currentOs = config.get(platform.system(), {})
    if package in currentOs:
        package = currentOs[package]
    s = subprocess.check_output(['pip', 'install', package, *args])
    print(s)
    print('\n')
