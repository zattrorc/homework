from RestrictedPython import compile_restricted,  safe_builtins
from RestrictedPython.PrintCollector import PrintCollector
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import math
import numpy
import scipy
import sklearn
import random
import re
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']

#白名单库，如需其它包直接修改以下列表并修改_safe_import
# _SAFE_MODULES = ["math","seaborn", "os", "pandas","numpy", "sklearn","scipy.stats","statsmodels.api",
#                  "sklearn.linear_model","scipy", "matplotlib","matplotlib.pyplot"]


def _safe_import(name, *args, **kwargs):
    # if name not in _SAFE_MODULES:
    #     raise Exception(f"Importing of module {name!r} is not allowed")
    return __import__(name, *args, **kwargs)

def _hook_write(obj):
    return obj

def generate_random_path():
    number = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"./cache/{number}.jpg"

def replace_plt_show_with_savefig(code_str):
    matches = re.finditer(r'plt\.show\(\)', code_str)
    save_paths = []
    offset = 0
    for match in matches:
        start, end = match.start() + offset, match.end() + offset
        random_path = generate_random_path()
        save_paths.append(random_path)
        replacement = f'plt.savefig("{random_path}")'
        code_str = code_str[:start] + replacement + code_str[end:]
        offset += len(replacement) - len(match.group())


    return code_str, save_paths


def execute_in_sandbox(df, code):
    my_globals = {
        "__builtins__": {
            **safe_builtins,
            "__import__": _safe_import,
            "_print_": PrintCollector,
            "_getitem_": lambda x, y: x[y],
            "_write_": _hook_write
        },
    }
    modules = {
            'pandas': pd,
            'pd':pd,
            'np':numpy,
            'matplotlib': matplotlib,
            'math': math,
            'numpy': numpy,
            'scipy': scipy,
            'sklearn': sklearn,
            'plt': plt,
            'sns':sns
        }
    my_globals.update(modules)

    local_vars = {
        'df': df
    }
    code, save_paths = replace_plt_show_with_savefig(code)
    code = code
    byte_code = compile_restricted(
        code + "\nprint(' ')",
        filename='<user code>',
        mode='exec'
    )

    try:
        exec(byte_code, my_globals, local_vars)
        result_text = local_vars['_print']()
    except Exception as e:
        print(e)
        result_text = "No text message is generated by code. Error: " + str(e)
    data = {
        'text': "\n\n"+ result_text,
        'images': save_paths}
    if len(data['images'])>0:
        data['text'] = result_text + "The chart has been completed, task finished.\n"
        print(data)
    return data
