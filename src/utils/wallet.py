# src/utils/wallet.py
import pymysql

async def modify_user_balance(db: pymysql.connections.Connection, user_id: int, amount: int, operation: str = "add") -> int:

    with db.cursor() as cursor:

        cursor.execute("SELECT balance FROM wallets WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO wallets (user_id, balance) VALUES (%s, 0)", (user_id,))
            db.commit()
            current_balance = 0
        else:
            current_balance = result[0]

        if operation == "add":
            new_balance = current_balance + amount
        elif operation == "remove":
            new_balance = max(current_balance - amount, 0)
        elif operation == "set":
            new_balance = amount
        else:
            raise ValueError(f"Opération inconnue: {operation}")

        cursor.execute("UPDATE wallets SET balance = %s WHERE user_id = %s", (new_balance, user_id))
        db.commit()

        return new_balance