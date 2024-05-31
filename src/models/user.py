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
  
  # Atributos do model
  id_discord = StringCol(unique=True)
  username = StringCol(unique=True)
  role = StringCol()
  wallet = MultipleJoin('Wallet')