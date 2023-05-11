"""Runner contracts."""

import time
import uuid
from . import dataset as datasets,config as configs,evaluators
from .providers import RetryableError

def run(dataset,config,provider,store,seed=0,stop_after=None,max_attempts=3,lease_seconds=300,sleep=time.sleep):
    datasets.validate(dataset);configs.validate(config)
    if type(max_attempts) is not int or not 1<=max_attempts<=10: raise ValueError('max_attempts must be 1..10')
    if stop_after is not None and (type(stop_after) is not int or stop_after<1): raise ValueError('stop_after must be positive')
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
            response=None
            failure=None
            for attempt in range(1,max_attempts+1):
                try:
                    response=provider.generate(prompt,case,config)
                    break
                except RetryableError as error:
                    store.record_attempt(identity,case['id'],{'attempt':attempt,'error':str(error),'retryable':True})
                    if attempt==max_attempts: failure=str(error)
                    sleep(min(0.05*2**(attempt-1),1.0))
            if response is None:
                payload={'task':case['task'],'slices':case.get('slices',[]),'score':0.0,'reason':'provider retry budget exhausted','status':'error','error':failure,'output':'','latency_ms':(time.perf_counter()-started)*1000,'input_tokens':0,'output_tokens':0,'usage_kind':'unknown'}
                store.save_owned_result(identity,case['id'],payload,owner)
                continue
            scored=evaluators.evaluate(case,response.output)
            payload=dict(scored,slices=case.get('slices',[]),output=response.output,prompt=prompt,trace=response.trace,latency_ms=(time.perf_counter()-started)*1000,input_tokens=response.input_tokens,output_tokens=response.output_tokens,usage_kind=response.usage_kind,status='ok')
            store.save_owned_result(identity,case['id'],payload,owner)
            completed+=1
            if stop_after is not None and completed>=stop_after:
                store.finish(identity,owner,'paused');return identity
        store.finish(identity,owner,'complete')
        return identity
    except BaseException:
        store.finish(identity,owner,'failed');raise
