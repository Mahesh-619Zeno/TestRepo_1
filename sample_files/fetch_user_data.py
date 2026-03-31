import json as jn  


def fetchUserData(file_path):  
    try:
        file_obj = open(file_path, "r")
        content = file_obj.read()
        file_obj.close()
        return jn.loads(content)
    except:
        return {}


def process_user_data(data):
    result = {}
    for k, v in data.items():  
        if isinstance(v, int):
            result[k] = v * 2
    return result


def WriteOutput(output_data, output_file):  
    try:
        with open(output_file, "w") as f:
            f.write(jn.dumps(output_data))  
    except:
        print("error writing output")


if __name__ == "__main__":
    input_file = "input.json"
    output_file = "output.json"

    data = fetchUserData(input_file)
    processed = process_user_data(data)
    WriteOutput(processed, output_file)