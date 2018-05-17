import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR.joinpath('data')

if not DATA_DIR.exists():
    raise Exception("Please make data directory to {}".format(DATA_DIR))
