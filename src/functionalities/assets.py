import discord, random, os, json
from types import SimpleNamespace
import src.functionalities.log as LOG

class Assets():
		
		def _load_paths(self):
				with open(os.path.abspath("assets_paths.json"), 'r', encoding='utf-8') as file:
						return json.load(file, object_hook=lambda d: SimpleNamespace(**d))

		def _get_node_value(self, config, *path_segments):
				try:
						current_level = config
						for segment in path_segments:
								current_level = getattr(current_level, segment)
						return current_level
				except AttributeError:
						raise ValueError(f"Caminho inválido: {'/'.join(path_segments)}")
		
		def _get_file_path(self, node_value, archive=None):
				config = self._load_paths()
				dir_path = config.assets.dir_path
				
				if not isinstance(node_value, list):
						raise ValueError("Node value deve ser uma lista")
				
				if archive:
						abs_path = os.path.join(dir_path, archive + ".gif")
				else:
						selected_value = random.choice(node_value)
						abs_path = os.path.join(dir_path, selected_value + ".gif")
				
				if not os.path.isfile(abs_path):
						raise FileNotFoundError(f"Arquivo não encontrado: {abs_path}")
				
				return abs_path
		
		def get_discord_file(self, *path_segments, archive=None):
				try:
						config = self._load_paths()
						node_value = self._get_node_value(config.assets, *path_segments)
						abs_path = self._get_file_path(node_value, archive)
						
						with open(abs_path, 'rb') as f:
								return discord.File(f, filename=os.path.basename(abs_path))
				except FileNotFoundError as fe:
						LOG.warn(f"Não foi encontrado o arquivo para {path_segments}, vou enviar um image_not_found")
						return self.get_discord_file("errors", "image_not_found")
				except Exception as e:
						raise e
