from pathlib import Path

def load_sql_files(db):
    model_dir = Path("src/model")

    if not model_dir.exists():
        print("[WARN] Aucun dossier 'src/model/' trouvé.")
        return

    sql_files = sorted(model_dir.rglob("*.sql"))

    if not sql_files:
        print("[INFO] Aucun fichier SQL trouvé dans src/model/")
        return

    cursor = db.cursor()

    for sql_file in sql_files:
        if sql_file.name.startswith("_"):
            continue

        try:
            with open(sql_file, "r", encoding="utf8") as f:
                sql = f.read()

            cursor.execute(sql)
            print(f"[SQL] Chargé : {sql_file}")

        except Exception as e:
            print(f"[ERREUR SQL] {sql_file}: {e}")

    cursor.close()