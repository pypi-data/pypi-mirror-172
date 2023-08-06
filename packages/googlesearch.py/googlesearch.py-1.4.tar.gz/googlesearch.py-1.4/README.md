# googlesearch.py 1.4
The search API for [Google](https://www.google.com).

```
pip install googlesearch.py
```

## Example

```py
from gsearchlib import Search

result = Search("what is programming language")

print(result)

# output
# [
#     {
#         "title": "Programming language - Wikipedia",
#         "url": "https://en.wikipedia.org/wiki/Programming_language",
#         "netloc" : "en.wikipedia.org"
#     }
# ...
# ]
```

## License
This Python package is distributed under the [Unlicense](https://unlicense.org/)