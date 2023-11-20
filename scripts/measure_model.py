import json,sys,time,platform,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
from regression_workbench.dataset import load
from regression_workbench.providers import TransformersProvider
from regression_workbench.runner import run
from regression_workbench.store import Store
from regression_workbench.comparison import compare_runs,operational
import torch,transformers
import argparse
p=argparse.ArgumentParser();p.add_argument('--model-path',required=True);p.add_argument('--revision',required=True);p.add_argument('--output',default='.local/model-evidence');args=p.parse_args()
E=pathlib.Path(args.output);E.mkdir(parents=True,exist_ok=True)
provider=TransformersProvider(args.model_path,args.revision)
data=load(ROOT/'fixtures/tasks-v1.json')
configs=[{'model':'google/flan-t5-small','prompt':'{input}','parameters':{'temperature':0,'max_new_tokens':64}},{'model':'google/flan-t5-small','prompt':'Follow the instruction carefully. Give only the requested answer. {input}','parameters':{'temperature':0,'max_new_tokens':64}}]
started=time.perf_counter()
with Store(E/'real-model.db') as s:
 ids=[]
 for index,(config,seed) in enumerate([(configs[0],0),(configs[0],1),(configs[1],0)]):
  rid=run(data,config,provider,s,seed=seed);ids.append(rid)
  print(index,rid,operational(s.results(rid)),flush=True)
 c=compare_runs(s,ids[0],ids[2],json.loads((ROOT/'fixtures/gate-policy.json').read_text()))
 repeat=all(a['output']==b['output'] for a,b in zip(s.results(ids[0]),s.results(ids[1])))
 evidence={'model':'google/flan-t5-small','revision':provider.revision,'runtime':{'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,'machine':platform.machine(),'threads':2},'dataset':data['name'],'case_count':len(data['cases']),'run_ids':ids,'wall_seconds':time.perf_counter()-started,'repeat_outputs_identical':repeat,'comparison':c,'runs':[dict(s.get_run(r),results=s.results(r)) for r in ids]}
 (E/'real-model-evidence.json').write_text(json.dumps(evidence,indent=2))
 print(json.dumps({'overall':c['overall'],'gate':c['gate'],'repeat_identical':repeat,'wall_seconds':evidence['wall_seconds']},indent=2))
