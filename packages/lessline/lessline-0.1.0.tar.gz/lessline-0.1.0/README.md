# LessLine
Less line to read&write text file

## Requirements
- Python >= 3.6

## Installation
```shell
$ pip install lessline
```

## Example
```python
from lessline.text_file import read, write

file = 'demo.txt'
text = 'Hello word!\nThis is lessline!'
write(text, file)

text_new = read(file)
print(len(text_new), text_new)
```
