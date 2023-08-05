perfect-banner
==============

Your python project might have a cool looking
ascii art banner. But did you took into account
that some users may have a terminal open which
has a character width that is smaller than the one
of the art.

Perhaps you want to create multiple banners with
different sizes so users with a smaller/bigger
terminal screen can take a look at your wonderful

```
  ____                              
 |  _ \                             
 | |_) | __ _ _ __  _ __   ___ _ __ 
 |  _ < / _` | '_ \| '_ \ / _ \ '__|
 | |_) | (_| | | | | | | |  __/ |   
 |____/ \__,_|_| |_|_| |_|\___|_|   
                                    
```


Installation
------------

```
pip install perfect-banner
```


Example Usage
-------------

This example imports the `art` package from
[the `art` library](https://pypi.org/project/art/).

```python
import banner
import art

def get_banners():
    for font in art.FONT_NAMES:
        yield art.text2art("python", font)

choice = banner.choose(*get_banners())
print(choice)
```

You can also optionally set `width` or `hight`
to `False` in the `choose` function to ignore
the `width` or `height`. By default `width` is
set to `True` and `height` to `False` (due to
the feasibility to scroll).
