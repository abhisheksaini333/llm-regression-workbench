"""Providers contracts."""

from dataclasses import dataclass,field

@dataclass(frozen=True)
class Response:
    output: str
    input_tokens: int=0
    output_tokens: int=0
    usage_kind: str='unknown'
    trace: dict=field(default_factory=dict)
    def __post_init__(self):
        if not isinstance(self.output,str): raise ValueError('output must be text')
        if type(self.input_tokens) is not int or type(self.output_tokens) is not int or min(self.input_tokens,self.output_tokens)<0: raise ValueError('invalid token counts')
        if self.usage_kind not in {'tokens','estimated_words','unknown'}: raise ValueError('invalid usage kind')

class RetryableError(RuntimeError): pass

class FixtureProvider:
    name='fixture'
    def __init__(self,outputs): self.outputs=dict(outputs)
    def generate(self,prompt,case,config):
        if case['id'] not in self.outputs: raise ValueError('missing fixture output for '+case['id'])
        output=self.outputs[case['id']]
        return Response(output,len(prompt.split()),len(output.split()),'estimated_words',{'provider':'fixture'})

class TransformersProvider:
    name='transformers'
    def __init__(self,path,revision,threads=2):
        from pathlib import Path
        if not Path(path).is_dir(): raise ValueError('local model directory is required')
        if not revision: raise ValueError('model revision is required')
        import torch
        from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
        torch.set_num_threads(threads)
        self.torch=torch
        self.revision=revision
        self.tokenizer=AutoTokenizer.from_pretrained(path,local_files_only=True)
        self.model=AutoModelForSeq2SeqLM.from_pretrained(path,local_files_only=True)
        self.model.eval()
    def generate(self,prompt,case,config):
        maximum=config.get('parameters',{}).get('max_new_tokens',64)
        if type(maximum) is not int or not 1<=maximum<=256: raise ValueError('max_new_tokens must be 1..256')
        inputs=self.tokenizer(prompt,return_tensors='pt',truncation=True,max_length=512)
        with self.torch.no_grad():
            output=self.model.generate(**inputs,max_new_tokens=maximum,do_sample=False,num_beams=1)
        text=self.tokenizer.decode(output[0],skip_special_tokens=True)
        return Response(text,int(inputs['input_ids'].numel()),int(output[0].numel())-1,'tokens',{'provider':self.name,'revision':self.revision,'deterministic':True})
