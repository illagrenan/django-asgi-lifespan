# Installation

!!! info "Supported Python and Django versions"

    This package supports only Django release series 4.0+ and Python 3.9+. If you need to support an older version in your project, please contact me or [open a pull request](https://github.com/illagrenan/django-asgi-lifespan/pulls).

## Stable release

!!! danger "Important warning"

    This is an experimental package and a hobby project. Although I use this package in my production projects without any problems, it does not mean that everything will work with your project.

    Please read [other limitations](limitations.md) – especially those related to the deployment.


To install Django ASGI Lifespan, run this command in your
terminal:

``` console
$ pip install --upgrade django-asgi-lifespan
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
