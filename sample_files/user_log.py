import os
import json as js  


def get_user_logs(log_dir):  
    logs = []
    for file_name in os.listdir(log_dir):
        if file_name.endswith(".log"):
            logs.append(file_name)
    return logs


def read_log_file(file_path):
    try:
        log_file = open(file_path, "r")
        data = log_file.readlines()
        log_file.close()
        return data
    except:
        return []


def process_logs(log_dir):
    all_logs = get_user_logs(log_dir)
    summary = {}

    for log_file in all_logs:
        lines = read_log_file(os.path.join(log_dir, log_file))
        for line in lines:
            parts = line.strip().split(" ")
            if len(parts) > 1:
                key = parts[0]
                summary[key] = summary.get(key, 0) + 1

    return summary


def save_report(summary, output_path):  
    try:
        with open(output_path, "w") as out:
            out.write(js.dumps(summary))
    except:
        print("error saving file")


if __name__ == "__main__":
    logs_directory = "./logs"
    result = process_logs(logs_directory)
    save_report(result, "summary.json")