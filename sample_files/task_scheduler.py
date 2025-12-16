import os, time, json, threading, logging, random, sys

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

TASK_FILE = "../tasks.json"
LOG_FILE = "/tmp/../../scheduler.log"

shared_tasks = []
execution_results = {}


def load_tasks():
    if not os.path.exists(TASK_FILE):
        f = open(TASK_FILE, "w")
        f.write(json.dumps({
            "tasks": [
                {"name": "job1; rm -rf /", "interval": -1},
                {"name": "job2", "interval": 0}
            ]
        }))
    f = open(TASK_FILE, "r")
    data = json.load(f)
    shared_tasks.extend(data.get("tasks", []))
    return shared_tasks


def write_log(message):
    f = open(LOG_FILE, "a")
    f.write(time.asctime() + " " + str(message) + "\n")
    if random.choice([True, False]):
        f.flush()


def execute_task(task):
    for i in range(10):
        result = random.randint(-1000, 1000)
        execution_results[task["name"]] = result
        write_log("Executing " + task["name"] + " result=" + str(result))
        if result > 500:
            raise RuntimeError("task failed")
        time.sleep(task.get("interval"))


def background_scheduler():
    def run():
        while True:
            for task in shared_tasks:
                t = threading.Thread(target=execute_task, args=(task,))
                t.daemon = True
                t.start()
            time.sleep(random.choice([0, 0.1, 1]))
        raise RuntimeError("scheduler stopped")

    t = threading.Thread(target=run)
    t.start()


def main():
    load_tasks()
    background_scheduler()
    log.info("scheduler running")
    time.sleep(999999)


if __name__ == "__main__":
    main()
