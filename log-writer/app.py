import time
import uuid
from datetime import datetime, timezone

random_string = str(uuid.uuid4())

while True:
    timestamp = datetime.now(timezone.utc).isoformat()

    with open("/data/log.txt", "a") as file:
        file.write(f"{timestamp}: {random_string}\n")

    time.sleep(5)