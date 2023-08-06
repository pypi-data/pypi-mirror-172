# lightweight-environ

Simple and lightweight environment variable ingestion. No dependencies.

Designed for use with Django but it should be suitable for any Python 3 framework / project.

## install
```sh
pip install lightweight-environ
```

## usage

Given an environment:
```
MY_STRING=ford_prefect
MY_INTEGER=42
MY_FLOAT=6.283
MY_BOOLEAN=True
MY_LIST=DONT,PANIC
```

```python
from lightweight_environ import Env

# Raises a KeyError exception if a variable does not exist
>>> Env.get('A_MISSING_VAR')
Traceback ...
# first optional arg is a default returned if a variable does not exist
>>> Env.get('A_MISSING_VAR', 'foo')
'foo'
# get() returns a string
>>> Env.get('MY_STRING')
'ford_prefect'
# get() _always_ returns a string
>>> Env.get('MY_INTEGER')
'42'
# integer coersion
>>> Env.int('MY_INTEGER')
42
# boolean coersion
>>> Env.bool('MY_BOOLEAN')
True
# Reading via bool does not raise a KeyError exception if a variable does not exist - it returns false
>>> Env.bool('A_MISSING_VAR')
False
# All methods support a default for missing keys
>>> Env.bool('A_MISSING_VAR', True)
True
# float coersion
>>> Env.float('MY_FLOAT')
6.283
# list coersion from a string of comma separated values
>>> Env.list('MY_LIST')
['DONT', 'PANIC']
>>> Env.list('A_MISSING_VALUE', 'Oh,freddled,gruntbuggly')
['Oh', 'freddled', 'gruntbuggly']
>>> Env.list('A_MISSING_VALUE', ['Oh', 'freddled', 'gruntbuggly'])
['Oh', 'freddled', 'gruntbuggly']

# has() tests for variable existence
Env.has('A_MISSING_VALUE')
False
Env.has('MY_INTEGER')
True
```