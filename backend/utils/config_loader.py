
import os
from dotenv import load_dotenv
from pathlib import Path
import yaml

load_dotenv()


def _project_root() -> Path:
    # print(Path(__file__).resolve().parents[0])
    # print(Path(__file__).resolve().parents[1])
    # print(Path(__file__).resolve().parents[2])
    # c:/users/admin/onedrive/desktop/knowledgeassistant_10pm/backend/config/config.yaml
    return Path(__file__).resolve().parents[2]


def load_config(config_path: str = None):

    env_path = os.getenv("config_path")
    print(env_path)

    if config_path is None:
        config_path = env_path

    path = Path(config_path)

    # backend/config/config.yaml

    if not path.is_absolute():
        path = _project_root()/path

    if not path.exists():
        raise FileExistsError("config file not found")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


print(load_config())
