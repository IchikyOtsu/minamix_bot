import importlib
from pathlib import Path
import asyncio

async def load_commands(bot):
    commands_dir = Path("src/commands")

    if not commands_dir.exists():
        print("[WARN] Aucun dossier 'src/commands' trouvé.")
        return

    for path in sorted(commands_dir.rglob("*.py")):
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

                print(f"[CMD] Chargée : {module_name}")

        except Exception as e:
            print(f"[ERREUR IMPORT] {module_name}: {e}")