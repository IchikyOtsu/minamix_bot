import importlib
from pathlib import Path
import asyncio

async def load_events(bot):
    events_dir = Path("src/events")

    if not events_dir.exists():
        print("[WARN] Aucun dossier 'src/events' trouvé.")
        return

    for path in sorted(events_dir.rglob("*.py")):
        if path.name.startswith("_"):
            continue

        rel = path.relative_to("src")
        module_name = f"src.{rel.with_suffix('').as_posix().replace('/', '.')}"
        
        try:
            module = importlib.import_module(module_name)

            if hasattr(module, "register"):
                register_fn = getattr(module, "register")
                if asyncio.iscoroutinefunction(register_fn):
                    await register_fn(bot)
                else:
                    register_fn(bot)

                print(f"[EVENT] Chargé : {module_name}")

        except Exception as e:
            print(f"[ERREUR IMPORT] {module_name}: {e}")