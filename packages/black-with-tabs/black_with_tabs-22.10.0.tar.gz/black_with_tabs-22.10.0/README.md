[![Black (With Tabs) Logo](https://i.imgur.com/p8aSBKs.png)](https://black.readthedocs.io/en/stable/)

<h2 align="center">The Somewhat Compromised Code Formatter</h2>

> “Any color you like.”

**This is not the official Black package!** Get that
[here](https://github.com/psf/black).

_Black (with tabs)_ is the uncompromising Python code formatter. By using it, you agree
to cede control over minutiae of hand-formatting. In return, _Black (with tabs)_ gives
you speed, determinism, and freedom from `pycodestyle` nagging about formatting. You
will save time and mental energy for more important matters.

Oh, also, now it's using tabs for indentation instead of spaces. In general, whitespace
(except for the initial indent) in docstrings is left alone. Whitespace in multiline
string literals should always be left alone.

Tabs are good for indenting. Don't use them for alignment. No shade at folks who choose
spaces instead. We just prefer tabs.

Blackened code looks the same regardless of the project you're reading. Formatting
becomes transparent after a while and you can focus on the content instead.

_Black (with tabs)_ makes code review faster by producing the smallest diffs possible.

Try out the original using the [Black Playground](https://black.vercel.app). Watch the
[PyCon 2019 talk](https://youtu.be/esZLCuWs_2Y) to learn more.

---

**IMPORTANT**

_Black (with tabs)_ does NOT provide a separate command line interface from the original
_Black_. It's still just `black`. So, they cannot coexist (without virtual environments,
anyways). Pick one!

**[Read the documentation on ReadTheDocs!](https://black.readthedocs.io/en/stable)**

---

## Installation and usage

### Installation

_Black (with tabs)_ can be installed by running `pip install black-with-tabs`. It
requires Python 3.7+ to run. If you want to format Jupyter Notebooks, install with
`pip install 'black[jupyter]'`.

If you can't wait for the latest _hotness_ and want to install from GitHub...

Too bad!! We don't have the black-with-tabs source up publicly at the moment. Though
please email jrowley at marcusengineering dot com to receive a copy.

### Usage

To get started right away with sensible defaults:

```sh
black {source_file_or_directory}
```

You can run _Black (with tabs)_ as a package if running it as a script doesn't work:

```sh
python -m black {source_file_or_directory}
```

Further information can be found in our docs:

- [Usage and Configuration](https://black.readthedocs.io/en/stable/usage_and_configuration/index.html)

_Black_ is already [successfully used](https://github.com/psf/black#used-by) by many
projects, small and big. _Black_ has a comprehensive test suite, with efficient parallel
tests, and our own auto formatting and parallel Continuous Integration runner. Now that
we have become stable, you should not expect large formatting to changes in the future.
Stylistic changes will mostly be responses to bug reports and support for new Python
syntax. For more information please refer to the
[The Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html).

Also, as a safety measure which slows down processing, _Black_ will check that the
reformatted code still produces a valid AST that is effectively equivalent to the
original (see the
[Pragmatism](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#ast-before-and-after-formatting)
section for details). If you're feeling confident, use `--fast`.

## The _Black_ code style

_Black_ is a PEP 8 compliant\*\* opinionated formatter. _Black_ reformats entire files
in place. Style configuration options are deliberately limited and rarely added. It
doesn't take previous formatting into account (see
[Pragmatism](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#pragmatism)
for exceptions).

Our documentation covers the current _Black_ code style, but planned changes to it are
also documented. They're both worth taking a look:

- [The _Black_ Code Style: Current style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
- [The _Black_ Code Style: Future style](https://black.readthedocs.io/en/stable/the_black_code_style/future_style.html)

Changes to the _Black_ code style are bound by the Stability Policy:

- [The _Black_ Code Style: Stability Policy](https://black.readthedocs.io/en/stable/the_black_code_style/index.html#stability-policy)

Please refer to this document before submitting an issue. What seems like a bug might be
intended behaviour.

\*\* except, of course, _Black (with tabs)_ is not using spaces for indentation...

### Pragmatism

Early versions of _Black_ used to be absolutist in some respects. They took after its
initial author. This was fine at the time as it made the implementation simpler and
there were not many users anyway. Not many edge cases were reported. As a mature tool,
_Black_ does make some exceptions to rules it otherwise holds.

- [The _Black_ code style: Pragmatism](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#pragmatism)

Please refer to this document before submitting an issue just like with the document
above. What seems like a bug might be intended behaviour.

## Configuration

_Black_ is able to read project-specific default values for its command line options
from a `pyproject.toml` file. This is especially useful for specifying custom
`--include` and `--exclude`/`--force-exclude`/`--extend-exclude` patterns for your
project.

You can find more details in our documentation:

- [The basics: Configuration via a file](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-via-a-file)

And if you're looking for more general configuration documentation:

- [Usage and Configuration](https://black.readthedocs.io/en/stable/usage_and_configuration/index.html)

**Pro-tip**: If you're asking yourself "Do I need to configure anything?" the answer is
"No". _Black_ is all about sensible defaults. Applying those defaults will have your
code in compliance with many other _Black_ formatted projects.

## Used by

Marcus Engineering, LLC

And YOU!

## Testimonials

**James Rowley**, [engineer at Marcus Engineering](https://marcusengineering.com/):

> Deferring to the judgement of this wonderful automated tool has saved so much time and
> effort, not just in writing the code but of course in merging and reviewing it. But I
> will never surrender my tabs!

**Mark Omo**, professional smartguy:

> ![lol](https://warehouse-camo.ingress.cmh1.psfhosted.org/c86835a06049d1679d1d225e2d320881e1c3b669/68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f6665727265742d6775792f626c61636b2d776974682d746162732f6d61737465722f646f63732f5f7374617469632f726561646d652d746162732e6a7067)

## License

MIT

## Contributing

Welcome! Happy to see you willing to make the project better. You can get started by
reading this:

- [Contributing: The basics](https://black.readthedocs.io/en/latest/contributing/the_basics.html)

You can also take a look at the rest of the contributing docs or talk with the
developers:

- [Contributing documentation](https://black.readthedocs.io/en/latest/contributing/index.html)
- [Chat on Discord](https://discord.gg/RtVdv86PrH)

## Change log

The log has become rather long. It moved to its own file.

See [CHANGES](https://black.readthedocs.io/en/latest/change_log.html).

## Authors

The author list is quite long nowadays, so it lives in its own file.

See [AUTHORS.md](./AUTHORS.md)

## Code of Conduct

Everyone participating in the _Black_ project, and in particular in the issue tracker,
pull requests, and social media activity, is expected to treat other people with respect
and more generally to follow the guidelines articulated in the
[Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

At the same time, humor is encouraged. In fact, basic familiarity with Monty Python's
Flying Circus is expected. We are not savages.

And if you _really_ need to slap somebody, do it with a fish while dancing.
