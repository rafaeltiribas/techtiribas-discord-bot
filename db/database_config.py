from sqlobject import connectionForURI, sqlhub

from src.models.user import User
from src.models.wallet import Wallet
from src.models.transaction_history import TransactionHistory
from src.models.bot_bank import BotBank
from src.models.user_interactions import UserInteractionsHistory, UserInteractions
import src.utils.log as LOG

import os

def init_db():
    sqlhub.processConnection = get_connection()
    
def create_tables():
    User.createTable(ifNotExists=True)
    Wallet.createTable(ifNotExists=True)
    TransactionHistory.createTable(ifNotExists=True)
    BotBank.createTable(ifNotExists=True)
    UserInteractions.createTable(ifNotExists=True)
    UserInteractionsHistory.createTable(ifNotExists=True)
    
def open_transaction():
    con = get_connection()
    return con.transaction()

def get_connection():
    db_file = 'techtiribas_bot.db'
    db_path = os.path.abspath(db_file)
    return connectionForURI(f'sqlite:///{db_path}')

def generate_new_bot_bank():
    if (BotBank.select().getOne(None)) is None:
        LOG.warn("Não existe BotBank gerado, então vou criar um no database")
        BotBank(diary_tax=0.2, daily_prize=20.0, cron_execute="* * * * *") #Criar um banco