"""Config contracts."""

from .dataset import digest

def validate(config):
    if not isinstance(config,dict) or not isinstance(config.get('model'),str) or not config['model'].strip():
        raise ValueError('model is required')
    if not isinstance(config.get('prompt'),str) or '{input}' not in config['prompt']:
        raise ValueError('prompt must include {input}')
    p=config.get('parameters',{})
    if not isinstance(p,dict): raise ValueError('parameters must be an object')
    if not isinstance(p.get('temperature',0),(int,float)) or not 0<=p.get('temperature',0)<=2:
        raise ValueError('temperature outside [0,2]')
    digest(config)
    return config

def render(config, text):
    validate(config)
    return config['prompt'].replace('{input}',text)

def run_identity(dataset_hash, config, seed=0):
    validate(config)
    return digest({'dataset':dataset_hash,'config':config,'seed':seed,'evaluator_version':1})
