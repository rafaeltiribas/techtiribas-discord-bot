from sqlobject import SQLObject, StringCol, MultipleJoin

class User(SQLObject):
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
  
  HIERARCHY = {
    "Council": 4,
    "Admin": 3,
    "Subscriber": 2,
    "Member": 1
  }
  
  # Atributos do model
  id_discord = StringCol(unique=True)
  username = StringCol(unique=True)
  role = StringCol()
  wallet = MultipleJoin('Wallet')
  
  @staticmethod
  def is_valid_role(role_str):
    return role_str in User.ROLE