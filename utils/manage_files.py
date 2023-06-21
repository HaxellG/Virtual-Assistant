import yaml
import json

def read_file(filename, filetype):
    """
    Function to read various types of files.

    Parameters:
        filename (str): The name of the file to read
        filetype (str): The extension of the file
    """
    
    try:
        with open("{}.{}".format(filename, filetype), "r") as file:
            if filetype.lower() == "yaml":
                return yaml.safe_load(file)
            elif filetype.lower() == "json":
                return json.load(file)
            else:
                return file.read()
    except Exception as e:
        print(f"Error occurred while reading the file: {e}")
        return None


def write_file(data, filename, filetype):
    """
    Function to write data to a file.

    Parameters:
        data (str/list/dict): Data to write
        filename (str): The name of the file
        filetype (str): The extension of the file
    """
    try:
        with open("{}.{}".format(filename, filetype), "a") as file:
            if isinstance(data, str):
                file.write(data + '\n')  # append a new line after each data
            elif isinstance(data, (list, dict)) and filetype.lower() in ["yaml", "json"]:
                if filetype.lower() == "yaml":
                    yaml.dump(data, file)
                else:  # json
                    json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error occurred while writing to the file: {e}")