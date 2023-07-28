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
    r=commands.add_parser('run');r.add_argument('dataset');r.add_argument('--config',required=True);r.add_argument('--db',default='.local/runs.db');r.add_argument('--outputs');r.add_argument('--model-path');r.add_argument('--model-revision');r.add_argument('--seed',type=int,default=0);r.add_argument('--stop-after',type=int);r.add_argument('--max-attempts',type=int,default=3)
    c=commands.add_parser('compare');c.add_argument('baseline');c.add_argument('candidate');c.add_argument('--db',default='.local/runs.db');c.add_argument('--policy');c.add_argument('--markdown')
    return p

def dispatch(args):
    if args.command=='validate':
        data=dataset.load(args.dataset)
        return {'name':data['name'],'cases':len(data['cases']),'fingerprint':dataset.fingerprint(data)},0
    if args.command=='run':
        data=dataset.load(args.dataset);settings=json.loads(Path(args.config).read_text())
        if bool(args.outputs)==bool(args.model_path): raise ValueError('choose exactly one provider: --outputs or --model-path')
        provider=FixtureProvider(json.loads(Path(args.outputs).read_text())) if args.outputs else TransformersProvider(args.model_path,args.model_revision)
        Path(args.db).parent.mkdir(parents=True,exist_ok=True)
        with Store(args.db) as store:
            identity=runner.run(data,settings,provider,store,args.seed,args.stop_after,args.max_attempts)
            return store.get_run(identity),0
    if args.command=='compare':
        policy=json.loads(Path(args.policy).read_text()) if args.policy else {}
        with Store(args.db) as store: result=comparison.compare_runs(store,args.baseline,args.candidate,policy)
        if args.markdown: Path(args.markdown).write_text(report.markdown(result))
        return result,0 if result['gate']['passed'] else 1
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
