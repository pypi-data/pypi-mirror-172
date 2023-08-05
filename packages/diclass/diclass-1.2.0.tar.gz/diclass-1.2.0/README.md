# diclass: convert python dict to python class object
[![PyPI Latest Release](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.org/project/diclass/)

## What is it?

**diclass** It fully converts a python dict to a python class object and all dict keys and internal dict are converted to python class objects as well.


```python
# !pip install diclass
```

    Collecting diclass
      Downloading diclass-1.0.0-py3-none-any.whl (4.2 kB)
    Installing collected packages: diclass
    Successfully installed diclass-1.0.0


## Example


```python
from diclass import DictClass

obj = DictClass({'id':1, 'data':{'name':'John', 'age':31, 'wife':{'name':'Jessica', 'age':28}}})

print(obj.id, obj.data.name, obj.data.wife.name)
```

    1 John Jessica

