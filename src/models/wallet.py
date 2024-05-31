from transaction_history import TransactionType

class Wallet:
  
  def __init__(self, user_id_discord):
    self.user_id_discord = user_id_discord
    self.balance = 300.00
    self.transaction_history = []

  def realize_transaction(self, transaction):
    if transaction.type_transaction == TransactionType.DEPOSIT:
        self.balance += transaction.value
    elif transaction.type_transaction == TransactionType.WITHDRAWAL:
        self.balance -= transaction.value
