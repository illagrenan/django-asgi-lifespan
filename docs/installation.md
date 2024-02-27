# Installation

To install Django ASGI Lifespan, run this command in your terminal:

``` console
$ pip install --upgrade django-asgi-lifespan
# or
$ poetry add django-asgi-lifespan@latest
```

**Do not** add `django-asgi-lifespan` to `INSTALLED_APPS`.

This is the preferred method to install Django ASGI Lifespan, as it will always install the most recent stable release.

If you don't have [pip][] installed, this [Python installation guide][]
can guide you through the process.

## From source

The source for Django ASGI Lifespan can be downloaded from
the [Github repo][].

You can either clone the public repository:

``` console
$ git clone git://github.com/illagrenan/django-asgi-lifespan
```

Or download the [tarball][]:

``` console
$ curl -OJL https://github.com/illagrenan/django-asgi-lifespan/tarball/master
```

Once you have a copy of the source, you can install it with:

``` console
$ pip install .
```

  [pip]: https://pip.pypa.io
  [Python installation guide]: http://docs.python-guide.org/en/latest/starting/installation/
  [Github repo]: https://github.com/illagrenan/django-asgi-lifespan
  [tarball]: https://github.com/illagrenan/django-asgi-lifespan/tarball/master
