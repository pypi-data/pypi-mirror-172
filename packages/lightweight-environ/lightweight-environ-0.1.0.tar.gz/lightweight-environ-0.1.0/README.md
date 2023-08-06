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

>>> Env.get('A_MISSING_VAR')            # Raises a KeyError exception if 'MY_ENV_VAR' is not set
Traceback ...
>>> Env.get('A_MISSING_VAR', 'foo')     # first optional arg is a default returned if 'MY_ENV_VAR' is not set
'foo'
>>> Env.get('MY_STRING')                # get returns a string
'ford_prefect'
>>> Env.get('MY_INTEGER')               # get returns a string
'42'
>>> Env.int('MY_INTEGER')               # integer coersion
42
>>> Env.bool('MY_BOOLEAN')              # boolean coersion
True
>>> Env.bool('A_MISSING_VAR')           # Reading via bool does not raise an exception if the value is missing
False                                   # It defaults to `False`
>>> Env.bool('A_MISSING_VAR', True)     # All methods support a default for missing keys
True
>>> Env.float('MY_FLOAT')               # float coersion
6.283
>>> Env.list('MY_LIST')                  # list coersion from a string of comma separated values
['DONT', 'PANIC']
>>> Env.list('A_MISSING_VALUE', 'Oh,freddled,gruntbuggly')
['Oh', 'freddled', 'gruntbuggly']
>>> Env.list('A_MISSING_VALUE', ['Oh', 'freddled', 'gruntbuggly'])
['Oh', 'freddled', 'gruntbuggly']

Env.has('A_MISSING_VALUE')              # Test if a variable exists
False
Env.has('MY_INTEGER')
True

```