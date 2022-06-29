# md-to-html-CONVERTER

The program converts input .md files to .html using regex. Due to unforseen issues resulting from the read method the converter is far from perfect. Fixing these limitations will require complete rework of the script.

## LIMITATIONS:

- no nested lists
- lists have to be followed by newline before a blockquote
- lists do not render correctly if near end of file  
- no mid-word bolds and italics:
  - *it **bold**ti*not
- no bold italics if they start together:    
  - ***boldit***
- no bolds/italics when followed by a comma: 
  - **bold**, not 
