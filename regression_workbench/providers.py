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
