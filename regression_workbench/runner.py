"""Runner contracts."""

import time
import uuid
from . import dataset as datasets,config as configs,evaluators
from .providers import RetryableError

def run(dataset,config,provider,store,seed=0,stop_after=None,max_attempts=3,lease_seconds=300,sleep=time.sleep):
    datasets.validate(dataset);configs.validate(config)
    if not dataset['cases']: raise ValueError('cannot run an empty dataset')
    identity=configs.run_identity(datasets.fingerprint(dataset),config,seed)
    store.register(identity,datasets.fingerprint(dataset),config,seed,len(dataset['cases']))
    owner=uuid.uuid4().hex
    store.claim(identity,owner,lease_seconds)
    completed=0
    try:
        done={r['case_id'] for r in store.results(identity)}
        for case in sorted(dataset['cases'],key=lambda c:c['id']):
            if case['id'] in done: continue
            store.claim(identity,owner,lease_seconds)
            prompt=configs.render(config,case['input'])
            started=time.perf_counter()
            response=provider.generate(prompt,case,config)
            scored=evaluators.evaluate(case,response.output)
            payload=dict(scored,slices=case.get('slices',[]),output=response.output,prompt=prompt,trace=response.trace,latency_ms=(time.perf_counter()-started)*1000,input_tokens=response.input_tokens,output_tokens=response.output_tokens,usage_kind=response.usage_kind,status='ok')
            store.save_owned_result(identity,case['id'],payload,owner)
            completed+=1
        store.finish(identity,owner,'complete')
        return identity
    except BaseException:
        store.finish(identity,owner,'failed');raise
