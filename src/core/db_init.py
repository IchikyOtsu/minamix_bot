from pathlib import Path


# Column migrations: (table, column, ALTER statement)
_COLUMN_MIGRATIONS = [
    (
        "boutique_roles",
        "exclusif",
        "ALTER TABLE boutique_roles ADD COLUMN exclusif TINYINT(1) NOT NULL DEFAULT 0",
    ),
    (
        "users",
        "last_seen",
        "ALTER TABLE users ADD COLUMN last_seen TIMESTAMP NULL",
    ),
    (
        "rp_characters",
        "nax_balance",
        "ALTER TABLE rp_characters ADD COLUMN nax_balance BIGINT NOT NULL DEFAULT 0",
    ),
]


def _run_migrations(db):
    cursor = db.cursor()

    for table, column, sql in _COLUMN_MIGRATIONS:
        cursor.execute(
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s",
            (table, column),
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(sql)
            db.commit()
            print(f"[MIGRATION] {table}.{column} ajouté")

    # Make discoveries global: remove guild_id if still present
    cursor.execute(
        "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'discoveries' AND COLUMN_NAME = 'guild_id'"
    )
    if cursor.fetchone()[0] > 0:
        cursor.execute(
            "DELETE d1 FROM discoveries d1 "
            "INNER JOIN discoveries d2 "
            "ON d1.user_id = d2.user_id AND d1.egg_key = d2.egg_key "
            "AND d1.found_at > d2.found_at"
        )
        cursor.execute("ALTER TABLE discoveries DROP PRIMARY KEY")
        cursor.execute("ALTER TABLE discoveries DROP COLUMN guild_id")
        cursor.execute("ALTER TABLE discoveries ADD PRIMARY KEY (user_id, egg_key)")
        db.commit()
        print("[MIGRATION] discoveries rendu global (guild_id supprimé)")

    cursor.close()


def init_db(db):
    model_dir = Path("src/model")
    if not model_dir.exists():
        print("[WARN] Dossier 'src/model/' introuvable.")
        return

    cursor = db.cursor()
    for sql_file in sorted(model_dir.rglob("*.sql")):
        if sql_file.name.startswith("_"):
            continue
        try:
            cursor.execute(sql_file.read_text(encoding="utf-8"))
            print(f"[SQL] {sql_file}")
        except Exception as e:
            print(f"[ERREUR SQL] {sql_file}: {e}")
    cursor.close()

    _run_migrations(db)
