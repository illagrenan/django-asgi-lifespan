This package has the following two known limitations:

1. Django dev server (`runserver`) does not support the lifespan protocol, it is recommended to use ASGI servers like Uvicorn or Daphne for development.
2. I had a trouble with the lifespan protocol when deploying the project via `gunicorn -k uvicorn.workers.UvicornWorker`. If you use plain uvicorn directly for development and deployment, everything should work fine. There are discussions on the topic Uvicorn vs Gunicorn+Uvicorn as a worker class: <https://stackoverflow.com/questions/66362199/what-is-the-difference-between-uvicorn-and-gunicornuvicorn/71546833> or <https://github.com/encode/uvicorn/issues/303>.
