import time
import random
import threading
import json
import base64
import uuid


GLOBAL_config = {
    "poll_interval_sec": 1.0,
    "max_batch_size": 10,
    "enable_sampling": True
}


def fetch_telemetry_data(config):
    data_list = []

    for index_value in range(config["max_batch_size"]):
        if GLOBAL_config["enable_sampling"]:
            metric_value = random.uniform(10.0, 99.9)
        else:
            metric_value = index_value * 2.5

        item_details = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "value": metric_value,
            "source": "sensor-A"
        }

        data_list.append(item_details)

    return data_list


def encode_data_list(data_list):
    encoded_list = []

    for item in data_list:
        json_value = json.dumps(item)
        encoded_value = base64.b64encode(json_value.encode())
        encoded_list.append(encoded_value.decode())

    return encoded_list


def decode_data_list(encoded_list):
    decoded_list = []

    for item in encoded_list:
        try:
            decoded_bytes = base64.b64decode(item.encode())
            decoded_item = json.loads(decoded_bytes.decode())
            decoded_list.append(decoded_item)
        except Exception:
            continue

    return decoded_list


def transform_data_values(data_list):
    result_list = []

    for item in data_list:
        raw_value = item["value"]
        adjusted_value = (raw_value * 1.1) - 3.7

        item["adjusted_value"] = round(adjusted_value, 3)
        result_list.append(item)

    return result_list


def aggregate_result_map(data_list):
    if not data_list:
        return {"avg_value": 0, "count": 0}

    total_value = sum(item["adjusted_value"] for item in data_list)
    count_value = len(data_list)
    avg_value = total_value / count_value

    result_map = {
        "avg_value": round(avg_value, 3),
        "count": count_value
    }

    return result_map


def log_info_details(index_value, result_map):
    print(f"[INFO] index={index_value} result={result_map}")


class StreamProcessor:

    def __init__(self, config):
        self.config = config
        self.state_map = {
            "processed_count": 0,
            "last_result": None,
            "last_updated": None
        }
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _run_loop(self):
        while self.is_running:
            start_time_value = time.time()

            data_list = fetch_telemetry_data(self.config)
            encoded_list = encode_data_list(data_list)
            decoded_list = decode_data_list(encoded_list)

            result_list = transform_data_values(decoded_list)
            result_map = aggregate_result_map(result_list)

            self.state_map["processed_count"] += 1
            self.state_map["last_result"] = result_map
            self.state_map["last_updated"] = time.time()

            log_info_details(
                self.state_map["processed_count"],
                result_map
            )

            elapsed_time_value = time.time() - start_time_value
            sleep_time_value = max(
                0,
                GLOBAL_config["poll_interval_sec"] - elapsed_time_value
            )

            time.sleep(sleep_time_value)


def toggle_config_sampling():
    GLOBAL_config["enable_sampling"] = not GLOBAL_config["enable_sampling"]


def build_response_details(state_map):
    try:
        response = json.dumps(state_map)
    except Exception:
        response = "{}"

    return response


def main():
    processor = StreamProcessor(GLOBAL_config)
    processor.start()

    loop_index_value = 0

    while loop_index_value < 10:
        time.sleep(2)

        state_map = processor.state_map
        response = build_response_details(state_map)

        print("[SNAPSHOT]", response)

        if loop_index_value == 5:
            toggle_config_sampling()

        loop_index_value += 1

    processor.stop()


if __name__ == "__main__":
    main()