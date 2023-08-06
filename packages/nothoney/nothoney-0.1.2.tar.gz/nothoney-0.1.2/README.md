## nothoney

This is a small Python package that is able to recursively iterate through a nested (n-deep) dictionary or JSON object/file to retrieve data.

![nothoney](https://i.imgur.com/klWK9nP.jpg)

### So how do I fly this thing?

Install:

`pip install nothoney --user`

or

`python setup.py install --user`

Basic usage:
```python
>>> import nothoney
>>> test
{'x': [{'a': 'b', 'c': {'foo': 'hello'}}, {'y': 'z', 'blah': {'lala': 'funfun', 'foo': 'world'}}]}
>>> nothoney.eat(test, 'foo')
['hello', 'world']
>>> nothoney.eat(test, 'funfun', mode='value')
['lala']
```

File mode (test.json):
```json
[
  {
    "a": "b",
    "c": {
      "foo": "boom goes the dynamite!"
    }
  },
  {
    "x": "y",
    "z": [
      {
        "lalala": {
          "foo": "gotem coach!",
          "random": "stuff",
          "here": 1337
        }
      }
    ]
  }
]
```

```python
>>> nothoney.eat('test.json', 'foo', as_file=True)
['boom goes the dynamite!', 'gotem coach!']
```
