import json
import os

def env_json():
		with open(os.path.abspath("path_archives.json"), 'r', encoding='utf-8') as file:
				return json.load(file)