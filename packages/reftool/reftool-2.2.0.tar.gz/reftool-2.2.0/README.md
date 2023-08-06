### reftool

---

*reftool* is a command line interface for accessing reference archives. It allows to display
references, copy single reference items into the clipboard and optionally to apply encodings
to a copied reference. An example implementation for a reference archive is the
[usd-reference-archive](https://github.com/usdAG/usd-reference-archive).

![](https://github.com/usdAG/reftool/workflows/main%20Python%20CI/badge.svg?branch=main)
![](https://github.com/usdAG/reftool/workflows/develop%20Python%20CI/badge.svg?branch=develop)
[![](https://img.shields.io/badge/version-2.2.0-blue)](https://github.com/usdAG/reftool/releases)
[![](https://img.shields.io/badge/build%20system-pip-blue)](https://pypi.org/project/reftool)
![](https://img.shields.io/badge/python-9%2b-blue)
[![](https://img.shields.io/badge/license-GPL%20v3.0-blue)](https://github.com/usdAG/reftool/blob/main/LICENSE)


### Installation

----

*reftool* can be installed via *pip*, either by installing from [PyPi](https://pypi.org/reftool):

```console
[user@host ~]$ pip3 install --user reftool
```

or by building and installing it manually:

```console
[user@host ~]$ git clone https://github.com/usdAG/reftool
[user@host ~]$ cd reftool
[user@host ~]$ pip3 install -r requirements.txt
[user@host ~]$ python3 setup.py sdist
[user@host ~]$ pip3 install --user dist/reftool-*
```

*reftool* supports autocompletion for *bash*. To take advantage of autocompletion, you
need to have the [completion-helpers](https://github.com/qtc-de/completion-helpers) project
installed. If setup correctly, just copying the [completion script](/resources/bash_completion.d/ref)
to your ``~/.bash_completion.d`` folder enables autocompletion.


### Configuration

----

During the installation, *reftool* creates a configuration file ``~/.config/reftool.ini``.
Inside this file, the path for the reference archive and some other display related options
are set. You can adjust these options to your own preferences.

In order to be useful, at least one reference archive should be available within *reftools*
reference path. The [usd-reference-archive](https://github.com/usdAG/usd-reference-archive)
is one example for a *reftool* compatible archive. You can have several different archives
within your reference path.

For a default installation, the following commands can be used to setup a reference archive:

```console
[user@host ~]$ mkdir -p ~/.local/share/reftool-archives
[user@host ~]$ cd ~/.local/share/reftool-archives
[user@host ~]$ git clone https://github.com/usdAG/usd-reference-archive
```
