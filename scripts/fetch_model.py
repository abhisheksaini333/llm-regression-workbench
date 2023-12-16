"""Download the documented FLAN-T5-small revision into a user-selected cache."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from regression_workbench.artifacts import download
p=argparse.ArgumentParser();p.add_argument('--destination',default='.local/models/flan-t5-small');args=p.parse_args()
print(json.dumps(download(json.loads((ROOT/'evidence/model-artifacts.json').read_text()),args.destination),indent=2))
