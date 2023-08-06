
# PySpeakItOut Package

PySpeakItOut package is a audiobook that makes you fall in love with reading books, it extract content from pdf and convert it into a audiobook to increase your reading efficiency

## Installation

Install PySpeakItOut package by giving command

```bash
  pip install PySpeakItOut
```
    
## Important Note

    before passing book name in reader method as a 
    parameter, please make sure that book is present in 
    the same directory where you are coding
## Examples

```python

    from PySpeakItOut import reader

    reader.readitout(book='bookname.pdf',
                  voice='male' or 'female',
                  page_number=8,
                  speech_rate=160)

```

## Author

@krishna_sonune

Author
@kris