"""Config contracts."""
from .dataset import digest


def validate(config):
    if (
        not isinstance(config, dict)
        or not isinstance(config.get("model"), str)
        or (not config["model"].strip())
    ):
        raise ValueError("model is required")
    if not isinstance(config.get("prompt"), str) or "{input}" not in config["prompt"]:
        raise ValueError("prompt must include {input}")
    p = config.get("parameters", {})
    if not isinstance(p, dict):
        raise ValueError("parameters must be an object")
    if (
        type(p.get("temperature", 0)) not in (int, float)
        or not 0 <= p.get("temperature", 0) <= 2
    ):
        raise ValueError("temperature outside [0,2]")
    digest(config)

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if any(
                    (
                        secret in key.lower()
                        for secret in (
                            "api_key",
                            "password",
                            "secret",
                            "authorization",
                            "access_token",
                        )
                    )
                ):
                    raise ValueError(
                        "credentials must be provided through the environment"
                    )
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(config)
    return config


def render(config, text):
    validate(config)
    return config["prompt"].replace("{input}", text)


def run_identity(dataset_hash, config, seed=0):
    validate(config)
    return digest(
        {
            "dataset": dataset_hash,
            "config": config,
            "seed": seed,
            "evaluator_version": 1,
        }
    )
