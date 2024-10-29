## How to release a new version

1. Merge all changes to the [main](https://github.com/illagrenan/django-asgi-lifespan/tree/main/) branch.
2. Document all changes in [the changelog](changelog.md).
3. Run the following command locally:
    ``` console linenums="0"
    poetry run bump-my-version bump major|minor|patch \
      --verbose --allow-dirty --dry-run
    ```
   This uses [bump-my-version](https://github.com/callowayproject/bump-my-version).
4. If everything looks OK, run the same command as in the previous step, but without the `--dry-run` switch.
5. Push the newly created tag:
    ``` console linenums="0"
    git push --verbose origin --tags
    ```
6. [The GitHub Workflow](https://github.com/illagrenan/django-asgi-lifespan/blob/main/.github/workflows/release.yml) will take care of the release to PyPI and to GitHub Releases.
7. Edit the release message in the GitHub repository to be nicely formatted, and then link to this documentation.
