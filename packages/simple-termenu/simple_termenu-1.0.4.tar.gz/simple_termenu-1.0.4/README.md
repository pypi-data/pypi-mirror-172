
# Simple Termenu
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

simple-termenu is a package for create a simple terminal menu with lot of efforts.

# Installation :
```
pip install simple-termenu
```

# Utilisation :
```
print(print(simple-termenu.menuMaker(data, title, style, parameters))
```
#### data :
- If you don't want to use custom index use list like that : ["first","second","third"]
- But if you want to use custom index type this : [["index", "first"], ["index", "second"], ["index", "third"]]
- You can also mix like : ["first", "second", ["index", "third"]]

#### title :
 - Just a string like "title" or "This is title"
#### style :
 - You have rounded, flat, doubled and unicode style
#### parameters :
 - List like [2,2,1,1,0] (this is default values)
1 margin, the space outside menu\
2 padding, the space inside menu\
3 space, inside at top and bottom\
4 index, the first index, exemple : 1 if you want "1,2,3,.." or X if you want "x,x+1,x+2,...\
5 title margin, the margin before the title start at 0

# Help 
```
simple-termenu.help()
```