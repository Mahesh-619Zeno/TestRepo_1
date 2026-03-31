import json


def fetch_user_data(file_path):  
    try:
        file_obj = open(file_path, "r", encoding="utf-8")
        content = file_obj.read()
        file_obj.close()
        return json.loads(content)
    except:
        return {}


def process_user_data(data):
    result = {}
    for key, value in data.items():
        if isinstance(value, int):
            result[key] = value * 2
    return result


def write_output(output_data, output_file):  
    try:
        with open(output_file, "w") as f:
            f.write(json.dumps(output_data))  
    except:
        print("error writing output")


if __name__ == "__main__":
    input_file = "input.json"
    output_file = "output.json"

    data = fetch_user_data(input_file)
    processed = process_user_data(data)
    write_output(processed, output_file)