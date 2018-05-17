#!/usr/local/bin/python3
import argparse
import pandas_profiling 

from daoustats import checkinout
from daoustats.settings import ROOT_DIR

DEBUG_MODE = True

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--merge",
    help="Merge checkin/out data files to the given name",
    type=str) 
parser.add_argument(
    "-p",
    "--profile",
    help="Create html profiling reports to the given name",
    type=str)
args = parser.parse_args()

stats = checkinout.Stats()
if args.merge:
    extension = '.xlsx'
    if not args.merge.endswith(extension):
        args.merge += extension

    stats.to_file(args.merge)
    print("Success : " + args.merge)
elif args.profile:
    extension = '.html'
    if not args.profile.endswith(extension):
        args.profile += extension

    profile = pandas_profiling.ProfileReport(stats.data_frame)
    profile_path = ROOT_DIR.joinpath(args.profile)
    profile.to_file(outputfile=profile_path)
    print("Success : " + profile_path.name)
else:
    parser.print_help()
