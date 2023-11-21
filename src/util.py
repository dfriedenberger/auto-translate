import yaml
import os

def get_config():
    """ Given a filename,
        return the contents of that file
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../config/config.yaml')
    try:
        with open(filename, 'r',encoding="UTF-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"file {filename} not found")

