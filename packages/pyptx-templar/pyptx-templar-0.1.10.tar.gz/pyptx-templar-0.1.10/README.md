# pyptx-templar
Easily fill complex PowerPoint templates with Python.

## Installation
It can be installed with pip:
```sh
pip install pyptx-templar
```

## Usage
### Examples
See the `examples` directory for a few examples of how to use the library.

### Text placeholders
Python code can be directly written in a PowerPoint (as usual text), surrounded by `{{` and `}}`, and it will be replaced by its extended value.

#### Code interpretation
The specifics of how `{{<code>}}` is interpreted is by using `exec("_ret=" + <code>)` and then fetching the value of `_ret`.

##### Multi-statement code
In most situations, you will only have a single statement and you don't have to care about that,
but in some cases you might want to write several statements in the same bloc, for example `{{'';print('hello');_ret='world'}}`: `hello` will be printed and the value inserted in the PowerPoint will be `world`.

Similarly, you might want to write code purely for its side-effects, for example `{{‘’; table_dup_row(find_shape(_sl, ‘my_table’).table, 1, n=5, to=1)}}`
(cf `examples/3. arrays`) which duplicates a row of a table. If you don't write the empty string at the beginning, `None` will be returned, which is likely not the wanted behavior.

##### Code boundaries
Code is interpreted across runs (which can happen for example if the piece of code has different styles) but not across paragraphs or text frames.

If you don't know what runs, paragraph and text frames are in PowerPoint, just consider that this library only handles code which is in the same block of text, so avoid line breaks in the middle of a piece of code.

##### <a name="nestedcode"></a>Nested code
Nested code blocks are not interpreted as one might wish: when reading `{{1+{{1+1}}+1}}`, `1+{{1+1` will try to be interpreted (and fail), and then you will be left with `+1}}` in your slide.

It also means that having '}}' in your Python code (which is unlikely, but you never know) might break the interpretation.

*If you need nested code interpretation, feel free to write a PR.*

#### Output details
The code which is interpreted is removed, then interpreted and lastly the returned value is inserted.
It avoids any issue when the code duplicates its own slide / paragraph (which would mean an endless duplication).

The style (font, size, bold, italics, etc) of the text which will be inserted is the same as the style of the first opening curly bracket.

In case of error while interpreting the code, an empty string is used when replacing (so the code simply disappears from the presentation).

Whatever is returned will be converted to a string using the `str` function.

### Images placeholders
Not only dynamic text can be inserted, but also images (see `./examples/2. images`).
The pattern is similar to the textual placeholder: `{{img:<modifiers>:<code>}}`. The code is interpreted in the same way as a textual placeholder, but the string returned has to be the path to a local image.

*If you want to be able to use links, bytes or anything other than a local path, feel free to open a PR.*

The shape which contained the placeholder is removed, whether the image exists or not.

Contrarily to textual placeholders, image placeholders are searched at the TextFrame level (so an image placeholder can be spread across paragraphs), the reason is that the placeholder won't be replaced by anything, it will be deleted as well as its container, and an image be added at the same position, so we don't really care about boundaries nor style.

#### Alignment
The shape containing the placeholder is used to position the image, in particular the image will be inside the square defined by the text frame. Modifiers are a list of characters which define how the image will be aligned within:
- `r`: align the image to the right
- `l`: align the image to the left
- `c`: center the image horizontally
- if none of `r`, `l` and `c` are specified, the image will have the exact same width as the shape
- `t`: align the image to the top
- `b`: align the image to the bottom
- `m`: center the image vertically ('middle')
- if none of `t`, `b` and `m` are specified, the image will have the exact same height as the shape

Images are scaled to take as much space as possible (while keeping the initial height width ratio, except when no modifier is used), meaning that at least one dimension is maximized.

### Main functions
The main function of the library are the ones in [`./pyptx_templar/placeholder.py`](./pyptx_templar/placeholder.py):
- `pres_replace`: replaces placeholders in a presentation
- `slide_replace`: replaces placeholders in a slide
- `table_replace`: replaces placeholders in a table
- `row_replace`: replaces placeholders in a table row
- `cell_replace`: replaces placeholders in a table cell
- `textframe_replace`: replaces placeholders in a textframe
- `paragraph_replace`: replaces placeholders in a paragraph
- `run_replace`: replaces placeholders in a run

#### Environment
You have to provide the full environment to the above functions for any variable, function or module to be available while executing the pieces of code in PowerPoint.

It is given as variadic named arguments (`kwargs`), which is convenient to add and remove variables, and to automatically copy the set, but has the big issue that some names might not be usable. It might be changed later to simply give the actual dictionary instead.

#### Context variables
When using the above functions, context variables are added to give more control from the executed pieces of code:
- `_pres`: the current [Presentation](https://python-pptx.readthedocs.io/en/latest/api/presentation.html#pptx.presentation.Presentation)
- `_idx`: the current slide index
- `_sl`: the current [Slide](https://python-pptx.readthedocs.io/en/latest/api/slides.html#slide-objects)
- `_table`: the current [Table](https://python-pptx.readthedocs.io/en/latest/api/table.html#pptx.table.Table)
- `_cell`: the current [Cell](https://python-pptx.readthedocs.io/en/latest/api/table.html#pptx.table._Cell)
- `_r`: the current table row index
- `_c`: the current table column index
- `_tf`: the current [TextFrame](https://python-pptx.readthedocs.io/en/latest/api/text.html#pptx.text.text.TextFrame)
- `_p`: the current [Paragraph](https://python-pptx.readthedocs.io/en/latest/api/text.html#pptx.text.text._Paragraph)

Note that they are only available when it makes sense, eg. `_table`, `_cell`, `_r` and `_c` are only available when the code is inside a table.

#### Interpretation order
- Inside a [Presentation](https://python-pptx.readthedocs.io/en/latest/api/presentation.html#pptx.presentation.Presentation), slides are interpreted in ascending order.
- Inside a [Slide](https://python-pptx.readthedocs.io/en/latest/api/slides.html#slide-objects), shapes are interpreted in bottom-up order of the slide 'Selection Pane' list (to open it, click on the `Select` button in the `Home` tab and then `Selection Pane`).
- Inside a [Table](https://python-pptx.readthedocs.io/en/latest/api/table.html#pptx.table.Table), rows are interpreted from top to bottom.
- Inside a [table Row](https://python-pptx.readthedocs.io/en/latest/api/table.html#pptx.table._Row), cells are interpreted from left to right.
- Inside a [TextFrame](https://python-pptx.readthedocs.io/en/latest/api/text.html#pptx.text.text.TextFrame), if there is an image placeholder, the container will be deleted and an image added at the same position, otherwise paragraphs are interpreted in text order.
- Inside a [Paragraph](https://python-pptx.readthedocs.io/en/latest/api/text.html#pptx.text.text._Paragraph), runs are first interpreted separately in text order, and then code is searched across runs (also in text order). This is the only situation where code can be interpreted in a non-intuitive way. It also means that if you have runs with the following content `{{1+`, `{{1+1}}` and `+1}}`, then it will be interpreted correctly (contrary to what is said in the [nested code](#nestedcode) section). However it's kind of delicate to make sure that PowerPoint puts some text in a single run, so you should avoid betting on that.
- Inside a [Run](https://python-pptx.readthedocs.io/en/latest/api/text.html#pptx.text.text._Run), code is interpreted in text order.

### Miscellaneous
Various other functions are provided, mostly because they were used at some point and might be useful to someone.

[style.py](./pyptx_templar/style.py) contains functions to change the style of a piece of text or the borders of a table, but it's way more convenient to directly set the wanted style on the code.

[copy.py](./pyptx_templar/copy.py) contains functions to copy the style and content from an element to another.

[presmanager.py](./pyptx_templar/presmanager.py) contains functions to delete, move and duplicate some elements of a presentation.

### Disclaimer
**Everything can fail, no guarantees are provided and using exec is very unsafe if you don't know what you are executing.**
