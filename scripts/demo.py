"""Create two deterministic demonstration runs; safe to repeat."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from regression_workbench.dataset import load
from regression_workbench.providers import FixtureProvider
from regression_workbench.runner import run
from regression_workbench.store import Store
from regression_workbench.comparison import compare_runs

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--db',default='.local/runs.db');args=parser.parse_args()
    Path(args.db).parent.mkdir(parents=True,exist_ok=True)
    data=load(ROOT/'fixtures/tasks-v1.json')
    with Store(args.db) as store:
        ids=[]
        for name in ('baseline','candidate'):
            config=json.loads((ROOT/f'fixtures/{name}-config.json').read_text())
            outputs=json.loads((ROOT/f'fixtures/{name}-outputs.json').read_text())
            ids.append(run(data,config,FixtureProvider(outputs),store))
        report=compare_runs(store,*ids,json.loads((ROOT/'fixtures/gate-policy.json').read_text()))
        print(json.dumps({'baseline':ids[0],'candidate':ids[1],'overall':report['overall'],'gate':report['gate']},indent=2))
if __name__=='__main__':main()
