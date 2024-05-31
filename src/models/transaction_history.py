from enum import Enum

class TransactionType(Enum):
  START = 0
  DEPOSIT = 1
  RECEIPT = 2
  WITHDRAWAL = 3
  TRANSFER = 4
  PAYMENT = 5
  PURCHASE = 6

class TransactionHystory:
  def __init__(self, id_wallet, value, type_transaction, description=None):
    self.id_wallet = id_wallet
    self.value = value
    self.type_transaction = type_transaction or TransactionType.START
    self.description = description