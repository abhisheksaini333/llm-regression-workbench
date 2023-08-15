"""Portable upstream evaluation data adapters."""

import json
from pathlib import Path
from .dataset import validate

def import_evals(path):
    cases=[]
    for index,line in enumerate(Path(path).read_text().splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line);messages=row.get('input');ideal=row.get('ideal')
        if not isinstance(messages,list) or not isinstance(ideal,str): raise ValueError('supported Evals subset requires chat input and string ideal')
        if not all(isinstance(m,dict) and isinstance(m.get('content'),str) and m.get('role') in {'system','user','assistant'} for m in messages): raise ValueError('invalid chat messages')
        cases.append({'id':f'evals-{index}','task':'summary','input':'\n'.join(m['role']+': '+m['content'] for m in messages),'expected':{'keywords':ideal.split()},'slices':['imported']})
    return validate({'version':1,'name':'imported-evals-chat','cases':cases})
