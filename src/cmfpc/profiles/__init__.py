import json
from importlib import resources


def load(name: str) -> dict:
    with resources.files(__package__).joinpath(f"{name}.json").open() as f:
        return json.load(f)


def available():
    return sorted(p.name[:-5] for p in resources.files(__package__).iterdir() if p.name.endswith(".json"))
