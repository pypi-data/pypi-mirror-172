# tetebeche

This is a tiny script of use only to eccentric publishers. It uses 
[PyPDF2](https://github.com/py-pdf/PyPDF2) to create a 
[tête-bêche book](https://en.wikipedia.org/wiki/Dos-%C3%A0-dos_binding#T%C3%AAte-b%C3%AAche)
from two input pdfs. The two pdfs are merged, with the second reversed and rotated 180°.

The user should ensure that the input PDFs have the same page dimensions and that both have
an even number of pages.

## Usage

    usage: tetebeche [-h] book1 book2 merged
    
    positional arguments:
      book1       path to first (non-reversed) book
      book2       path to second (reversed) book
      merged      path to merged output file
    
    options:
      -h, --help  show this help message and exit