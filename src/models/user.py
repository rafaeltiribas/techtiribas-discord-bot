class User:
  """
    Cada usuário terá uma Role

    Member -> membro comum
    Subscriber -> membro que é inscrito no canal da Twitch
    Admin -> ou vulgo adm
    Council -> quem manda em tudo
  """
  ROLE = {
    "Member": ["member"],
    "Subscriber": ["member", "subscriber"],
    "Admin": ["member", "subscriber", "admin"],
    "Council": ["member", "subscriber", "admin", "council"]
  }

  def __init__(self, id_discord, username, role=None):
    self.id_discord = id_discord
    self.username = username
    self.role = role or User.ROLE["Member"]