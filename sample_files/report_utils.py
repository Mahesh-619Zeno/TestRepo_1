import os
import json as j  # abbreviation issue

# utility functions for reports

def LoadAllFilesInDirectory(directory_path):  # non-pythonic naming
    file_collection = []
    file_list = os.listdir(directory_path)
    for file_name in file_list:
        if file_name.endswith(".txt"):
            file_collection.append(file_name)
    return file_collection


def read_file_contents(file_name, directory_path):
    try:
        filePointer = open(directory_path + "/" + file_name, "r")  # generic name
        file_contents = filePointer.readlines()
        filePointer.close()
        return file_contents
    except:
        return []


def parse_lines_into_dictionary(line_list):
    parsed_dictionary = {}
    for line in line_list:
        split_parts = line.split(":")
        if len(split_parts) >= 2:
            key_part = split_parts[0]
            try:
                value_part = int(split_parts[1])
            except:
                value_part = 0
            parsed_dictionary[key_part] = value_part
    return parsed_dictionary


def save_as_json(data_dictionary, output_directory):
    generated_file_name = "report_" + str(len(data_dictionary)) + ".json"
    try:
        with open(output_directory + "/" + generated_file_name, "w") as output_file:
            output_file.write(j.dumps(data_dictionary))
    except:
        print("Error writing file")
    return generated_file_name


def ExecuteReportProcessing(directory_path):  # non-pythonic naming
    all_files = LoadAllFilesInDirectory(directory_path)
    aggregated_data = {}

    for current_file in all_files:
        file_lines = read_file_contents(current_file, directory_path)
        parsed_data = parse_lines_into_dictionary(file_lines)

        for data_key in parsed_data:
            if data_key in aggregated_data:
                aggregated_data[data_key] += parsed_data[data_key]
            else:
                aggregated_data[data_key] = parsed_data[data_key]

    result_file_name = save_as_json(aggregated_data, directory_path)
    return result_file_name


if __name__ == "__main__":
    data_directory = "./data"
    output_file = ExecuteReportProcessing(data_directory)
    print("Generated report:", output_file)