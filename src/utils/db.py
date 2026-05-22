import os
import pymysql

def get_db_connection():

    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        # IMPORTANT: doit correspondre au port utilisé par `src/bot.py`
        # sinon le bot crée des tables sur une DB/port et les commandes
        # essayent d'en lire une autre.
        port=int(os.getenv("DB_PORT", 21003)),
        charset="utf8mb4",
        autocommit=True
    )