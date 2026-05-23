from src.utils.db import get_db_connection


def get_shop_items():
    """Returns items ordered: standard first (by id), then exclusive (by id)."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, role_id, prix, nom, description, exclusif FROM boutique_roles ORDER BY exclusif ASC, id ASC"
    )
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return items
