#!/usr/bin/env bash
# End-to-end smoke test: boot the test Django app in Docker against each
# supported ASGI server and verify both lifespan-managed endpoints respond.
set -euo pipefail

IMAGE=asgi-e2e:local
CONTAINER=asgi-e2e
PORT=8080
HOST=127.0.0.1

echo ">> Building image $IMAGE"
docker build -t "$IMAGE" .

run_server() {
    local name=$1
    shift
    echo
    echo "================================================================"
    echo ">> Server: $name"
    echo "================================================================"

    docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
    docker run -d --rm --name "$CONTAINER" -p "$PORT:$PORT" \
        --workdir /usr/src/app/tests/ "$IMAGE" "$@"

    echo ">> Waiting up to 30s for $name to become ready"
    for _ in $(seq 1 30); do
        if curl -fsS -o /dev/null "http://$HOST:$PORT/client-from-app-config"; then
            echo ">> $name is ready"
            break
        fi
        sleep 1
    done

    if ! curl -fsS -o /dev/null "http://$HOST:$PORT/client-from-app-config"; then
        echo ">> $name failed to become ready, container logs:"
        docker logs "$CONTAINER" || true
        docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
        exit 1
    fi

    echo ">> Hitting /client-from-app-config"
    curl --fail-with-body --max-time 10 "http://$HOST:$PORT/client-from-app-config"
    echo

    echo ">> Hitting /client-from-scope-state"
    curl --fail-with-body --max-time 10 "http://$HOST:$PORT/client-from-scope-state"
    echo

    docker stop "$CONTAINER" >/dev/null
    echo ">> $name: OK"
}

run_server uvicorn \
    uv run uvicorn django_test_application.asgi:application \
    --host 0.0.0.0 --port 8080 --lifespan on

echo
echo ">> All servers passed"
