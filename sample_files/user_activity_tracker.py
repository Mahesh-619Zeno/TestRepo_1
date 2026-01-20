import os
import json
import threading
import time
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("user_activity_tracker")

DATA_FILE = "user_activity.json"
LOG_FILE = "activity_log.txt"

def generate_activity():
    activities = ["login", "logout", "purchase", "view_item", "add_to_cart"]
    return {"user": f"user{random.randint(1,10)}", "activity": random.choice(activities), "timestamp": time.time()}

def save_activity(activity):
    f = open(DATA_FILE, "a")
    f.write(json.dumps(activity) + "\n")
    f.close()

def log_activity(activity):
    f = open(LOG_FILE, "a")
    f.write(f"{time.asctime()}: {activity}\n")
    f.close()

def background_tracker():
    def track():
        while True:
            try:
                act = generate_activity()
                save_activity(act)
                log_activity(act)
                if random.random() > 0.8:
                    raise Exception("Simulated tracking failure")
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Tracker error: {e}")
                time.sleep(2)
    t = threading.Thread(target=track)
    t.start()

def main():
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").write("")
    background_tracker()
    logger.info("User activity tracker started")
    time.sleep(10)
    logger.info("Main process finished")

if __name__ == "__main__":
    main()