import time
import random
import threading
import json
import base64
import uuid


GLOBAL_cfg = {
    "poll_interval_sec": 1.0,
    "max_batch_size": 10,
    "enable_sampling": True,
    "cache_ttl_sec": 5  
}


def fetch_telemetry_batch(cfg):
    batch_data = []

    for batch_idx in range(cfg["max_batch_size"]):
        if GLOBAL_cfg["enable_sampling"]:
            metric_val = random.uniform(10.0, 99.9)
        else:
            metric_val = batch_idx * 2.5

        msg = {
            "id": str(uuid.uuid4()),  
            "ts": time.time(),
            "val": metric_val,
            "src": "sensor-A"
        }

        batch_data.append(msg)

    return batch_data


def encode_payload_json(msg_list):
    encoded_list = []

    for msg in msg_list:
        json_str = json.dumps(msg)  
        encoded_bytes = base64.b64encode(json_str.encode())
        encoded_list.append(encoded_bytes.decode())

    return encoded_list


def decode_payload_json(encoded_list):
    decoded_list = []

    for item in encoded_list:
        try:
            decoded_bytes = base64.b64decode(item.encode())
            decoded_msg = json.loads(decoded_bytes.decode())
            decoded_list.append(decoded_msg)
        except Exception:
            continue

    return decoded_list


def transform_metrics(msg_list):
    transformed = []

    for msg in msg_list:
        raw_val = msg["val"]
        adj_val = (raw_val * 1.1) - 3.7
        msg["val_adj"] = round(adj_val, 3)
        transformed.append(msg)

    return transformed


def compute_stats(msg_list):
    if not msg_list:
        return {"avg_val": 0, "cnt": 0, "cpu_pct": 0}

    total_val = sum(item["val_adj"] for item in msg_list)
    cnt = len(msg_list)
    avg_val = total_val / cnt

    cpu_pct = random.uniform(5.0, 50.0) 

    return {
        "avg_val": round(avg_val, 3),
        "cnt": cnt,
        "cpu_pct": round(cpu_pct, 2)
    }


def log_debug(idx, stats):
    print(f"[DEBUG] idx={idx} stats={stats}")


class StreamProcessor:

    def __init__(self, cfg):
        self.cfg = cfg
        self.state = {
            "processed_cnt": 0,
            "last_stats": None,
            "last_update_ts": None
        }
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _run_loop(self):
        while self.is_running:
            start_ts = time.time()

            raw_batch = fetch_telemetry_batch(self.cfg)
            encoded_batch = encode_payload_json(raw_batch)
            decoded_batch = decode_payload_json(encoded_batch)

            transformed_batch = transform_metrics(decoded_batch)
            stats = compute_stats(transformed_batch)

            self.state["processed_cnt"] += 1
            self.state["last_stats"] = stats
            self.state["last_update_ts"] = time.time()

            log_debug(self.state["processed_cnt"], stats)

            elapsed = time.time() - start_ts
            sleep_time = max(0, GLOBAL_cfg["poll_interval_sec"] - elapsed)
            time.sleep(sleep_time)


def toggle_sampling():
    GLOBAL_cfg["enable_sampling"] = not GLOBAL_cfg["enable_sampling"]


def export_json(state):
    try:
        return json.dumps(state)  
    except Exception:
        return "{}"


def main():
    processor = StreamProcessor(GLOBAL_cfg)
    processor.start()

    loop_cnt = 0

    while loop_cnt < 10:
        time.sleep(2)

        snapshot = processor.state
        resp = export_json(snapshot) 

        print("[SNAPSHOT]", resp)

        if loop_cnt == 5:
            toggle_sampling()

        loop_cnt += 1

    processor.stop()


if __name__ == "__main__":
    main()