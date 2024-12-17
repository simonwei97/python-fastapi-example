import os
from pathlib import Path

from dynaconf import Dynaconf

_BASE_DIR = Path(__file__).parent.parent

# settings.local.toml for local test
# priority: settings.local.toml < settings.toml
# 

settings_files = [
    Path(__file__).parent / "settings.toml",
]  # set absolute path

settings = Dynaconf(
    settings_files=settings_files,
    load_dotenv=True,  # load .env
    lowercase_read=True,  # 
    # /app/conf/settings.toml
    includes=[os.path.join("/app", "conf", "settings.toml")],
    base_dir=_BASE_DIR, 
)
