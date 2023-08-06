
#!/usr/bin/env python3
import sys
from setuptools import setup

if sys.version_info < (3, 8):
    print("Python 3.8 or higher is required - earlier python 3 versions may work but were not tested.")
    sys.exit(1)
setup(
    author='Yazhou He',
    author_email='yhe@irishfilm.ie',
    long_description=("""\
Scripts for use in the IFI Irish Film Archive. It is used for ingest strongbox csv report autmatically
"""),
    scripts=[
        'strgbx_fixity.py'
    ],
    install_requires=[
        'datetime',
        'keyboard',
        'selenium',
        'webdriver_manager'
    ],
    name='strgbx_fixity',
    version='2022.10.20.5',
    python_requires='>=3.8'
)
