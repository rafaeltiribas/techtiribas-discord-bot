from enum import Enum
from sqlobject import SQLObject, StringCol, ForeignKey, FloatCol

class TransactionType(Enum):
  START = 0
  DEPOSIT = 1
  RECEIPT = 2
  WITHDRAWAL = 3
  TRANSFER = 4
  PAYMENT = 5
  PURCHASE = 6


class TransactionHistory(SQLObject):
  wallet = ForeignKey('Wallet')  # Chave estrangeira para Wallet
  value = FloatCol()
  type_transaction = StringCol()
  description = StringCol()