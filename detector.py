import re
from database import create_database, save_attack

LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5

FAILED_PATTERN = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"


def detect_failed_logins():

    failed_attempts = {}

    with open(LOG_FILE, "r") as file:
        logs = file.readlines()

    for line in logs:

        match = re.search(FAILED_PATTERN, line)

        if match:

            ip = match.group(1)

            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

    return failed_attempts


def detect_bruteforce():

    create_database()

    attempts = detect_failed_logins()

    print("\n=== SSH Brute Force Detection Report ===\n")

    for ip, count in attempts.items():

        if count >= THRESHOLD:

            print(f"[ALERT] Suspicious IP: {ip} | Attempts: {count}")

            save_attack(ip, count)

        else:
            print(f"[INFO] IP: {ip} | Attempts: {count}")


if __name__ == "__main__":
    detect_bruteforce()