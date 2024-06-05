class UserError(Exception):
		"""Exceção personalizada para erro do Usuario."""
		def __init__(self, mensagem):
				self.mensagem = mensagem
				super().__init__(self.mensagem)