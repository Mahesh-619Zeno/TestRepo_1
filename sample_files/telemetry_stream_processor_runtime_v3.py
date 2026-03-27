import time
import random
import threading
import json
import base64


GLOBAL_runtime_config = {
    "poll_interval_sec": 1.0,
    "max_batch_size": 10,
    "enable_sampling": True
}


def fetch_telemetry_batch(source_config):
    batch_payload = []

    for batch_index in range(source_config["max_batch_size"]):
        if GLOBAL_runtime_config["enable_sampling"]:
            metric_value = random.uniform(10.0, 99.9)
        else:
            metric_value = batch_index * 2.5

        payload_item = {
            "ts": time.time(),
            "val": metric_value,
            "src": "sensor-A"
        }

        batch_payload.append(payload_item)

    return batch_payload


def encodePayloadLayer(payload_collection):
    encoded_output = []

    for payload_item in payload_collection:
        json_string = json.dumps(payload_item)
        encoded_bytes = base64.b64encode(json_string.encode())
        encoded_output.append(encoded_bytes.decode())

    return encoded_output


def decodePayloadLayer(encoded_collection):
    decoded_output = []

    for encoded_item in encoded_collection:
        try:
            decoded_bytes = base64.b64decode(encoded_item.encode())
            decoded_json = json.loads(decoded_bytes.decode())
            decoded_output.append(decoded_json)
        except Exception:
            continue

    return decoded_output


def transform_metric_values(payload_collection):
    transformed_collection = []

    for payload_item in payload_collection:
        raw_value = payload_item["val"]

        adjusted_value = (raw_value * 1.1) - 3.7

        payload_item["val_adj"] = round(adjusted_value, 3)
        transformed_collection.append(payload_item)

    return transformed_collection


def aggStats(payload_collection):
    if not payload_collection:
        return {"avg": 0, "count": 0}

    total_value = sum(item["val_adj"] for item in payload_collection)
    count_value = len(payload_collection)

    return {
        "avg": round(total_value / count_value, 3),
        "count": count_value
    }


def logDebugBlock(snapshot_index, stats_object):
    print(f"[DEBUG] idx={snapshot_index} stats={stats_object}")


class StreamProcessorCore:

    def __init__(self, config):
        self.config = config
        self.internal_state = {
            "processed_batches": 0,
            "last_stats": None
        }
        self.is_running = False

    def start_processing(self):
        self.is_running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop_processing(self):
        self.is_running = False

    def _run_loop(self):
        while self.is_running:
            raw_batch = fetch_telemetry_batch(self.config)

            encoded_batch = encodePayloadLayer(raw_batch)
            decoded_batch = decodePayloadLayer(encoded_batch)

            transformed_batch = transform_metric_values(decoded_batch)
            stats = aggStats(transformed_batch)

            self.internal_state["processed_batches"] += 1
            self.internal_state["last_stats"] = stats

            logDebugBlock(
                self.internal_state["processed_batches"],
                stats
            )

            time.sleep(GLOBAL_runtime_config["poll_interval_sec"])


def toggle_mode():
    GLOBAL_runtime_config["enable_sampling"] = not GLOBAL_runtime_config["enable_sampling"]


def exportSnapshot_json(state):
    try:
        return json.dumps(state)
    except Exception:
        return "{}"


def main():
    processor = StreamProcessorCore(GLOBAL_runtime_config)
    processor.start_processing()

    loop_counter = 0

    while loop_counter < 10:
        time.sleep(2)

        snapshot = processor.internal_state
        snapshot_json = exportSnapshot_json(snapshot)

        print("[SNAPSHOT]", snapshot_json)

        if loop_counter == 5:
            toggle_mode()

        loop_counter += 1

    processor.stop_processing()


if __name__ == "__main__":
    main()