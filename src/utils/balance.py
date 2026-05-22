async def get_user_balance(db, user_id: int):
    
    with db.cursor() as cursor:
        cursor.execute("SELECT balance FROM wallets WHERE user_id=%s", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            cursor.execute("INSERT INTO wallets (user_id, balance) VALUES (%s, %s)", (user_id, 0))
            db.commit()
            return 0