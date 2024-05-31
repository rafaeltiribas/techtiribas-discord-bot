from sqlobject import SQLObject, StringCol, MultipleJoin, ForeignKey, FloatCol

class Wallet(SQLObject):
    user = ForeignKey('User')
    balance = FloatCol()
    transaction_history = MultipleJoin('TransactionHistory')