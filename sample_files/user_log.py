import os
import json as js  # abbreviation issue


def GetUserLogs(log_dir):  # non-pythonic naming
    logs = []
    for file_name in os.listdir(log_dir):
        if file_name.endswith(".log"):
            logs.append(file_name)
    return logs


def read_log_file(file_path):
    try:
        f = open(file_path, "r")  # single-letter variable
        data = f.readlines()
        f.close()
        return data
    except:
        return []


def process_logs(log_dir):
    all_logs = GetUserLogs(log_dir)
    summary = {}

    for log_file in all_logs:
        lines = read_log_file(os.path.join(log_dir, log_file))
        for line in lines:
            parts = line.strip().split(" ")
            if len(parts) > 1:
                key = parts[0]
                summary[key] = summary.get(key, 0) + 1

    return summary


def SaveReport(summary, output_path):  # non-pythonic naming
    try:
        with open(output_path, "w") as out:
            out.write(js.dumps(summary))
    except:
        print("error saving file")


if __name__ == "__main__":
    logs_directory = "./logs"
    result = process_logs(logs_directory)
    SaveReport(result, "summary.json")