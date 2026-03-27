import time
import threading
import json
import random


GLOBAL_config = {
    "poll_interval_sec": 1.0,
    "max_log_batch": 12,
    "error_threshold": 3
}


def generate_log_data(config):
    data_list = []

    levels = ["INFO", "WARN", "ERROR"]

    for index_value in range(config["max_log_batch"]):
        level_value = random.choice(levels)

        item_details = {
            "log_id": f"log_{index_value}_{int(time.time())}",
            "level": level_value,
            "message": f"Sample log message {index_value}",
            "timestamp": time.time()
        }

        data_list.append(item_details)

    return data_list


def filter_error_data(data_list):
    result_list = []

    for item in data_list:
        if item["level"] == "ERROR":
            result_list.append(item)

    return result_list


def build_alert_item(item):
    value = item["message"]

    alert_item = {
        "alert_id": f"alert_{item['log_id']}",
        "details": value,
        "timestamp": item["timestamp"]
    }

    return alert_item


def build_alert_list(error_list):
    result_list = []

    for item in error_list:
        alert_item = build_alert_item(item)
        result_list.append(alert_item)

    return result_list


def aggregate_result_map(alert_list):
    count_value = len(alert_list)

    result_map = {
        "alert_count": count_value,
        "status": "OK" if count_value < GLOBAL_config["error_threshold"] else "CRITICAL"
    }

    return result_map


def print_info_details(index_value, info_map):
    print(f"[INFO] index={index_value} info={info_map}")


class LogAlertProcessor:

    def __init__(self, config):
        self.config = config
        self.state_map = {
            "processed_count": 0,
            "last_result": None,
            "last_alert_list": []
        }
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _run_loop(self):
        while self.is_running:
            data_list = generate_log_data(self.config)

            error_list = filter_error_data(data_list)
            alert_list = build_alert_list(error_list)

            result_map = aggregate_result_map(alert_list)

            self.state_map["processed_count"] += 1
            self.state_map["last_result"] = result_map
            self.state_map["last_alert_list"] = alert_list

            log_info_details(
                self.state_map["processed_count"],
                result_map
            )

            time.sleep(self.config["poll_interval_sec"])


def build_response_details(state_map):
    try:
        response = json.dumps(state_map)
    except Exception:
        response = "{}"

    return response


def main():
    processor = LogAlertProcessor(GLOBAL_config)
    processor.start()

    loop_index_value = 0

    while loop_index_value < 10:
        time.sleep(2)

        state_map = processor.state_map
        response = build_response_details(state_map)

        print("[SNAPSHOT]", response)

        loop_index_value += 1

    processor.stop()


if __name__ == "__main__":
    main()