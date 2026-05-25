import os
from datetime import datetime

TRACK_FILE = os.path.join("logs", "auto_second_request_pending.txt")


def track_auto_second_request(mg_idpreg: str, branch: str) -> None:
    os.makedirs(os.path.dirname(TRACK_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TRACK_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}\t{mg_idpreg}\t{branch}\n")
