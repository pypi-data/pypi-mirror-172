<img src="./logo.png" width=55 height=55 align="right"/>

# tinyunicodeblock
> A tiny utility to get the Unicode block of a character

[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![Pylint](https://img.shields.io/badge/pylint-10.00/10.00-ffbf48)](https://pylint.pycqa.org/en/latest/)
[![License](https://img.shields.io/gitlab/license/whoatemybutter/tinyunicodeblock)](https://spdx.org/licenses/GPL-3.0-or-later.html)
[![PyPi](https://img.shields.io/pypi/v/tinyunicodeblock)](https://pypi.org/project/tinyunicodeblock/)
[![Pipeline status](https://gitlab.com/whoatemybutter/tinyunicodeblock/badges/master/pipeline.svg)](https://gitlab.com/whoatemybutter/tinyunicodeblock/-/commits/master)  

This module provides only one ability that is absent from the built-in module `unicodedata`.
<br/>
It contains one function, `block()`, which returns the name of a
[Unicode block](https://www.unicode.org/faq/blocks_ranges.html) that a character belongs to.

## Table of contents
- [📦 Installation](#📦-installation)
- [🛠 Usage](#🛠-usage)
- [📰 Changelog](#📰-changelog)
- [📜 License](#📜-license)

---

## 📦 Installation

`tinyunicodeblock` is available on PyPi. 
It requires a Python version of **at least 3.7.0.** and depends on **no packages**.

To install with pip:
```shell
python -m pip install tinyunicodeblock
```

To install through Git:
```shell
python -m pip install git+https://gitlab.com/whoatemybutter/tinyunicodeblock.git
```

---

## 🛠 Usage

Only one function is publicly available, `block(character)`.
It will return the name of a Unicode block that `character` belongs to.

```python
>>> import tinyunicodeblock
>>> tinyunicodeblock.block("a")
'Basic Latin'
>>> tinyunicodeblock.block("\ufdfd")
'Arabic Presentation Forms-A'
>>> tinyunicodeblock.block("\ue845")
'Private Use Area'
>>> tinyunicodeblock.block("\ue845")
'Private Use Area'
>>> tinyunicodeblock.block("\U0009FFFF")
'No Block'
```

---

## 📰 Changelog

The changelog is at [CHANGELOG.md](CHANGELOG.md).

---

## 📜 License

`tinyunicodeblock` is licensed under
[GNU General Public License 3.0 or later](https://spdx.org/licenses/GPL-3.0-or-later.html).
<br/>
