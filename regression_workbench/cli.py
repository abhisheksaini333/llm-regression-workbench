"""Cli contracts."""

import argparse
import json
import sys
from pathlib import Path
from . import dataset,config,runner,comparison,report
from .providers import FixtureProvider,TransformersProvider
from .store import Store
from .redaction import sanitize

def parser():
    p=argparse.ArgumentParser(prog='regression',description='Evaluate model changes and enforce release gates')
    commands=p.add_subparsers(dest='command',required=True)
    v=commands.add_parser('validate');v.add_argument('dataset')
    return p

def dispatch(args):
    if args.command=='validate':
        data=dataset.load(args.dataset)
        return {'name':data['name'],'cases':len(data['cases']),'fingerprint':dataset.fingerprint(data)},0
    raise ValueError('unknown command')

def main(argv=None):
    args=parser().parse_args(argv)
    try:
        result,code=dispatch(args)
        print(json.dumps(sanitize(result),indent=2,allow_nan=False))
        return code
    except (ValueError,KeyError,OSError) as error:
        print(json.dumps({'error':sanitize(str(error))}),file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())
