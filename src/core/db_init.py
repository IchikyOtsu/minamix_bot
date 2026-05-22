from pathlib import Path


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
