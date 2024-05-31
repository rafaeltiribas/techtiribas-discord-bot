from sqlobject import connectionForURI, sqlhub

from src.models.user import User
from src.models.wallet import Wallet
from src.models.transaction_history import TransactionHistory

import os

def init_db():
    db_file = 'techtiribas_bot.db'
    db_path = os.path.abspath(db_file)
    connection = connectionForURI(f'sqlite:///{db_path}')
    sqlhub.processConnection = connection
    
def create_tables():
    User.createTable(ifNotExists=True)
    Wallet.createTable(ifNotExists=True)
    TransactionHistory.createTable(ifNotExists=True)