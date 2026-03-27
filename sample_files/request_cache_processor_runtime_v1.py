import time
import threading
import json
import hashlib
import random


GLOBAL_config = {
    "cache_ttl_sec": 5,
    "poll_interval_sec": 1.5,
    "max_request_batch": 8
}


def generate_request_data(config):
    data_list = []

    for index_value in range(config["max_request_batch"]):
        value = random.randint(100, 999)

        item_details = {
            "request_id": f"req_{index_value}_{int(time.time())}",
            "value": value,
            "timestamp": time.time()
        }

        data_list.append(item_details)

    return data_list


def process_request_data(data_list):
    result_list = []

    for item in data_list:
        value = item["value"]

        processed_value = value * 2 + 5

        result_item = {
            "request_id": item["request_id"],
            "processed_value": processed_value,
            "timestamp": item["timestamp"]
        }

        result_list.append(result_item)

    return result_list


def build_cache_key(item):
    raw_string_value = f"{item['request_id']}_{item['timestamp']}"
    hashed_value = hashlib.sha256(raw_string_value.encode()).hexdigest()
    return hashed_value


class CacheManager:

    def __init__(self, config):
        self.config = config
        self.cache_map = {}

    def set_item(self, key, item):
        self.cache_map[key] = {
            "item": item,
            "expiry": time.time() + self.config["cache_ttl_sec"]
        }

    def get_item(self, key):
        item_details = self.cache_map.get(key)

        if not item_details:
            return None

        if time.time() > item_details["expiry"]:
            del self.cache_map[key]
            return None

        return item_details["item"]

    def cleanup_expired(self):
        current_time_value = time.time()

        keys_to_delete = [
            key for key, details in self.cache_map.items()
            if current_time_value > details["expiry"]
        ]

        for key in keys_to_delete:
            del self.cache_map[key]


def aggregate_result_map(result_list):
    if not result_list:
        return {"total_value": 0, "count": 0}

    total_value = sum(item["processed_value"] for item in result_list)
    count_value = len(result_list)

    result_map = {
        "total_value": total_value,
        "count": count_value
    }

    return result_map


def log_info_details(index_value, info_map):
    print(f"[INFO] index={index_value} info={info_map}")


class RequestProcessor:

    def __init__(self, config):
        self.config = config
        self.cache = CacheManager(config)
        self.state_map = {
            "processed_count": 0,
            "last_result": None
        }
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _run_loop(self):
        while self.is_running:
            data_list = generate_request_data(self.config)
            result_list = process_request_data(data_list)

            for item in result_list:
                key = build_cache_key(item)
                self.cache.set_item(key, item)

            result_map = aggregate_result_map(result_list)

            self.state_map["processed_count"] += 1
            self.state_map["last_result"] = result_map

            log_info_details(
                self.state_map["processed_count"],
                result_map
            )

            self.cache.cleanup_expired()

            time.sleep(self.config["poll_interval_sec"])


def build_response_details(state_map):
    try:
        response = json.dumps(state_map)
    except Exception:
        response = "{}"

    return response


def main():
    processor = RequestProcessor(GLOBAL_config)
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