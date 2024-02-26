## Get Started!

Ready to contribute? Here's how to set up `django-asgi-lifespan` for local development.

1. Fork the `django-asgi-lifespan` repo on GitHub.
2. Clone your fork locally

    ```
    $ git clone git@github.com:your_name_here/django-asgi-lifespan.git
    ```

3. Ensure [Poetry](https://python-poetry.org/docs/) is installed.
4. Install dependencies and start your virtualenv:

    ```
    $ poetry install
    ```

5. Create a branch for local development:

    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the
   tests, including testing other Python versions, with tox:

    ```
    $ task test
    ```

7. Commit your changes and push your branch to GitHub:

    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

8. Submit a pull request through the GitHub website.

!!! tip "Taskfile"

    We recommend installing Task (<https://taskfile.dev/>) for easy launching of development tasks.

## Formatting and linting

```
$ poetry task format
```

## Tests

```
$ poetry task test
```

## Run a Django test project locally

The tests include a Django test project for integration testing. You can also run this test project locally (like any other Django project), sometimes it's useful to observe how a real application behaves.

```
$ cd ./tests/
$ poetry run uvicorn django_test_application.asgi:application --log-level=debug --reload
$ curl -v http://127.0.0.1:8000/test

## Test ASGI servers

```
$ cd ./tests/
$ poetry run uvicorn django_test_application.asgi:application --log-level=debug --reload
$ poetry run hypercorn django_test_application.asgi:application --log-level debug --reload
$ poetry run daphne django_test_application.asgi:application
$ poetry run granian --interface asgi django_test_application.asgi:application
$ poetry run gunicorn django_test_application.asgi:application -k uvicorn.workers.UvicornWorker --log-level debug --reload
```

