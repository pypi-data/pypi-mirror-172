imports = (
    'import numpy as np',
    'import numpy.ma as ma',
    'import pandas as pd',
    'import xarray as xr',
    'import math',
    'import json',
    'import xlrd',
    'from tqdm import tqdm',
    'import scipy.stats as sp',
    'import matplotlib.pyplot as plt',
    'import pymannkendall',
    'import pyhomogeneity',
    'import statsmodels.api as sm',
    'import scipy.special as ss',
    'import scipy',
    'from collections import namedtuple',
    'import multiprocessing as mp',
    'import pickle',
    'import datetime',
    'import copy',
    'import requests',
    'import csv',
    'import getpass',
    'import h5py',
    'import openpyxl',
    'import time as tm',
    'import shutil',
    'from pathlib import Path',
    'from IPython.display import clear_output',
    'from dateutil.relativedelta import relativedelta',
)

import pip

pip.main(['install', '--upgrade', '--force-reinstall', '-i', 'https://test.pypi.org/simple/ hidro-UNC-joaquin.segura.ellis'])
pip.main(['install', 'pyhomogeneity'])
pip.main(['install', 'pymannkendall'])
pip.main(['install', 'scipy'])
pip.main(['install', 'tqdm'])
pip.main(['install', 'matplotlib'])
pip.main(['install', 'xarray'])
pip.main(['install', 'pandas'])
pip.main(['install', 'statsmodels'])
pip.main(['install', 'requests'])
pip.main(['install', 'openpyxl'])
pip.main(['install', 'imageio'])
pip.main(['install', 'global_land_mask'])

for imp in imports:
    exec(imp)

clear_output()

""" Tool for testing a string of code. """

def test_code(f):
    import cProfile, pstats, io
    from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()
    f()
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())