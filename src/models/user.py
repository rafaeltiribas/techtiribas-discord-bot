from sqlobject import SQLObject, StringCol, MultipleJoin, IntCol
from enum import Enum

class Role(Enum):
  """
    Cada usuário terá uma Role

    Member -> membro comum
    Subscriber -> membro que é inscrito no canal da Twitch
    Admin -> ou vulgo adm
    Council -> quem manda em tudo
  """
  Member = 1
  Subscriber = 2
  Admin = 3
  Council = 4
  
  @staticmethod
  def is_valid(role_str):
    return role_str in Role.__members__
  

class User(SQLObject):
  # Atributos do model
  id_discord = StringCol(unique=True)
  username = StringCol(unique=True)
  role = StringCol()
  wallet = MultipleJoin('Wallet')
  
  @staticmethod
  def compare_roles(role1: str, role2: str):
    role1 = role1.capitalize()
    role2 = role2.capitalize()
    if not Role.is_valid(role1):
      raise ValueError(f'A role {role1} é inválida')
    if not Role.is_valid(role2):
      raise ValueError(f'A role {role2} é inválida')
    
    hierarchy1 = Role[role1].value
    hierarchy2 = Role[role2].value
    
    if hierarchy1 > hierarchy2:
      return 1
    elif hierarchy1 < hierarchy2:
      return -1
    else:
      return 0