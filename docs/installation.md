# Using package manager

To install Django ASGI Lifespan, run following command in your terminal:

=== ":simple-poetry: Poetry" 

    ```console linenums="0"
    poetry add django-asgi-lifespan@latest
    ```

=== ":simple-python: pip"

    ```console linenums="0"
    pip install --upgrade django-asgi-lifespan
    ```

**Do not** add `django-asgi-lifespan` to `INSTALLED_APPS`.

This is the preferred method to install this package, as it will always install the most recent stable release.

# From source

The source for Django ASGI Lifespan can be downloaded from
the [Github repo](https://github.com/illagrenan/django-asgi-lifespan).

You can either clone the public repository:

``` console linenums="0"
$ git clone git://github.com/illagrenan/django-asgi-lifespan
```

Or download the [tarball](https://github.com/illagrenan/django-asgi-lifespan/tarball/master):

``` console linenums="0"
curl --proto '=https' --tlsv1.3 -fsSL \
    --connect-timeout 10 \
    --retry 3 \
    --max-redirs 3 \
    -OJ https://github.com/illagrenan/django-asgi-lifespan/tarball/main
```

Once you have a copy of the source, you can install it with:

``` console linenums="0"
$ pip install .
```
