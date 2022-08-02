## Get Started!

Ready to contribute? Here's how to set up `django-asgi-lifespan` for local development.

1. Fork the `django-asgi-lifespan` repo on GitHub.
2. Clone your fork locally

    ```
    $ git clone git@github.com:your_name_here/django-asgi-lifespan.git
    ```

3. Ensure [poetry](https://python-poetry.org/docs/) is installed.
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
    $ poetry run task test
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


# Formatting and linting

```
$ poetry task format
```

# Tests

```
$ poetry task test
```
