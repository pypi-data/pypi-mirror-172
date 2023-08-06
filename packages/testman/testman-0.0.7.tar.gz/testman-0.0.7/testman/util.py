import logging
logger = logging.getLogger()

import os
import importlib
import re
import datetime

import yaml
import json

from dotmap import DotMap

def get_function(func):
  if "." in func:
    mod_name, func_name = func.rsplit(".", 1)
    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)
  else:
    return eval(func)

def expand(value, vars=None):
  # dict?
  if isinstance(value, dict):
    return { k : expand(v, vars) for k, v in value.items() }

  # list?
  if isinstance(value, list):
    return [ expand(v, vars) for v in value ]

  # load from file (prefix ~)
  if value[0] == "~":
    with open(value[1:]) as fp:
      value = fp.read()

  # expand
  if not vars:
    vars = {}
  else:
    vars = dict(vars) # copy to avoid leaking back
  # logger.info(json.dumps(vars, indent=2, default=str))
  vars.update(os.environ) # add environment variables
  # turn all values into mapped values
  vars = { k: mapped(v) for k,v in vars.items() }
  r = re.compile(r"{([^}]+)}")
  for stmt in r.findall(value):
    replacement = eval(stmt, {}, vars)
    if replacement:
      if value == "{" + stmt + "}":
        value = replacement
      else:
        value = value.replace("{"+stmt+"}", str(replacement))
    else:
      raise ValueError(f"unknown variable '{var}'")

  # try it as a function
  try:
    func, process = parse_command(value)
    value = postprocess(func(), process)
  except:
    pass

  # try eval
  try:
    value = eval(value, vars)
  except:
    pass

  return value

def parse_command(cmd):
  # parse string into func and filters
  if isinstance(cmd, str):
    try:
      filters = [ filter.strip() for filter in cmd.split("|") ]
      func    = get_function(filters.pop(0))
      return func, filters
    except ModuleNotFoundError as e:
      raise ValueError(f"unknown module for {cmd}") from e
    except AttributeError as e:
        raise ValueError(f"unknown function {cmd}") from e
  if callable(cmd):
    return cmd, []
  raise ValueError(f"not a valid command string")

def format_command(func, filters=""):
  if filters:
    filters = "|" + "|".join(filters)
  return f"{func.__module__}.{func.__name__}{filters}"

def postprocess(output, processors):
  for processor in processors:
    if isinstance(output, dict):
      if processor in dict:
        output = output[processor]
    elif isinstance(output, object) and hasattr(output, processor):
      p = getattr(output, processor)
      if callable(p):
        output = p()
      else:
        output = p
    else:
      try:
        f = get_function(processor)
        if callable(f):
          output = f(output)
      except:
        pass

  if not type(output) in [ int, float, bool, str, list, dict ]:
    try:
      output = output.__dict__
    except:
      output = str(output)

  return output

def prune(d):
  return { k:v for k,v in d.items() if v or v == False }

def load_ml(filename):
  _, ext = filename.rsplit(".", 1)
  loader = {
    "yaml" : yaml.safe_load,
    "yml"  : yaml.safe_load,
    "json" : json.load
  }[ext]
  with open(filename) as fp:
    return loader(fp)

def mapped(value):
  if isinstance(value, dict):
    return DotMap(value)
  if isinstance(value, list):
    return [ mapped(v) for v in value ]
  return value

def utcnow():
  return datetime.datetime.utcnow()
