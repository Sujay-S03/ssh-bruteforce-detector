import time
import re
from datetime import datetime
from database import create_database, save_attack

LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5

FAILED_PATTERN = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"

failed_attempts = {}


def monitor_logs():

    create_database()

    print("Monitoring SSH logs in real-time...\n")

    with open(LOG_FILE, "r") as file:

        file.seek(0, 2)

        while True:

            line = file.readline()

            if not line:
                time.sleep(0.5)
                continue

            match = re.search(FAILED_PATTERN, line)

            if match:

                ip = match.group(1)

                if ip not in failed_attempts:
                    failed_attempts[ip] = 0

                failed_attempts[ip] += 1
                count = failed_attempts[ip]

                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print(f"[FAILED] IP: {ip} | Attempts: {count}")
                save_attack(ip, count, current_time)

                if count == THRESHOLD:

                    print(f"[ALERT] Brute-force attack detected from {ip}")


if __name__ == "__main__":
    monitor_logs()