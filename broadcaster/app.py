import os
import json
import urllib.request
import nats
import asyncio


NATS_URL = os.environ.get(
    "NATS_URL",
    "nats://my-nats.nats.svc.cluster.local:4222"
)

GENERIC_URL = os.environ.get("GENERIC_URL", "")
LOG_ONLY = os.environ.get("LOG_ONLY", "false").lower() == "true"


async def main():
    nc = await nats.connect(NATS_URL)

    js = nc.jetstream()

    try:
        await js.add_stream(
            name="TODO_EVENTS",
            subjects=["todo.events"]
        )
    except Exception:
        pass

    sub = await js.pull_subscribe(
        "todo.events",
        durable="broadcaster"
    )

    print("Broadcaster started", flush=True)

    while True:
        messages = await sub.fetch(1, timeout=10)

        for msg in messages:
            try:
                data = json.loads(msg.data.decode())

                message = data.get(
                    "message",
                    "A todo was updated"
                )

                if LOG_ONLY:
                    print(
                        f"Message received: {message}",
                        flush=True
                    )
                    await msg.ack()
                    continue

                payload = json.dumps({
                    "user": "bot",
                    "message": message
                }).encode()

                request = urllib.request.Request(
                    GENERIC_URL,
                    data=payload,
                    headers={
                        "Content-Type": "application/json"
                    },
                    method="POST"
                )

                with urllib.request.urlopen(request) as response:
                    print(
                        f"Message sent, status: {response.status}",
                        flush=True
                    )

                await msg.ack()

            except Exception as e:
                print(
                    f"Failed to process message: {e}",
                    flush=True
                )


if __name__ == "__main__":
    asyncio.run(main())