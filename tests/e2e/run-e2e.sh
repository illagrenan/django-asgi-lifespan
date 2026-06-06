#!/usr/bin/env bash
# End-to-end smoke test: boot the test Django app in Docker against each
# supported ASGI server and verify the lifespan-managed endpoints respond.
#
# Per docs/asgi.md, daphne is intentionally skipped here: it does not
# implement the ASGI lifespan protocol at all (see django/daphne#264), so
# no lifespan signal would ever fire. Hypercorn is exercised, but only on
# the signal-based endpoint, because hypercorn does not propagate
# lifespan scope state to HTTP scopes (see pgjones/hypercorn#107).
set -euo pipefail

IMAGE=asgi-e2e:local
CONTAINER=asgi-e2e
PORT=8080
HOST=127.0.0.1

echo ">> Building image $IMAGE"
docker build -t "$IMAGE" .

# Usage: run_server NAME "ENDPOINT [ENDPOINT ...]" SERVER_CMD...
run_server() {
    local name=$1
    local endpoints=$2
    shift 2
    local first_endpoint
    first_endpoint=$(echo "$endpoints" | awk '{print $1}')

    echo
    echo "================================================================"
    echo ">> Server: $name"
    echo "================================================================"

    docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
    docker run -d --rm --name "$CONTAINER" -p "$PORT:$PORT" \
        --workdir /usr/src/app/tests/ "$IMAGE" "$@"

    echo ">> Waiting up to 30s for $name to become ready"
    for _ in $(seq 1 30); do
        if curl -fsS -o /dev/null "http://$HOST:$PORT$first_endpoint"; then
            echo ">> $name is ready"
            break
        fi
        sleep 1
    done

    if ! curl -fsS -o /dev/null "http://$HOST:$PORT$first_endpoint"; then
        echo ">> $name failed to become ready, container logs:"
        docker logs "$CONTAINER" || true
        docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
        exit 1
    fi

    for endpoint in $endpoints; do
        echo ">> Hitting $endpoint"
        curl --fail-with-body --max-time 10 "http://$HOST:$PORT$endpoint"
        echo
    done

    docker stop "$CONTAINER" >/dev/null
    echo ">> $name: OK"
}

run_server uvicorn "/client-from-app-config /client-from-scope-state" \
    uv run uvicorn django_test_application.asgi:application \
    --host 0.0.0.0 --port 8080 --lifespan on

# Hypercorn supports lifespan but not lifespan scope state, so only the
# signal-based endpoint is exercised here. See docs/asgi.md.
run_server hypercorn "/client-from-app-config" \
    uv run hypercorn --bind 0.0.0.0:8080 \
    django_test_application.asgi:application

echo
echo ">> All servers passed"
