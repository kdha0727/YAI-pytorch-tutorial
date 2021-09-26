"""
Lazy-evaluated module wrapper: required module will be downloaded while being imported.
"""

try:

    from . import easyrun

except ImportError:

    import os
    import sys
    import types

    import requests

    name = "easyrun"
    url = "https://raw.githubusercontent.com/kdha0727/easyrun-pytorch/main/easyrun.py"

    easyrun = types.ModuleType("{}.{}".format(__name__, name))

    try:
        response = requests.get(url)
    except Exception as e:
        raise ImportError(
            "Cannot connect to url '{}'.".format(url)
        ) from e

    try:  # save module if we have writing permission
        with open(os.path.join(os.path.dirname(__file__), "{}.py".format(name)), mode="w") as f:
            f.write(response.text)
    except OSError as e:
        pass

    closure = {}
    exec(compile(response.text, easyrun.__name__, "exec"), closure)
    easyrun.__dict__.update({k: v for k, v in closure.items() if not k.startswith('_')})

    sys.modules[easyrun.__name__] = easyrun

    del os, sys, types, requests, name, url, response, closure


# alias
easyrun.Trainer = easyrun.Easyrun  # type: ignore
