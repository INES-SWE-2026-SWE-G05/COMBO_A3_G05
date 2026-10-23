import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(os.getenv("AGRISOKO_DATA_PATH", ROOT / "data" / "members.json"))
METADATA_PATH = Path(os.getenv("AGRISOKO_METADATA_PATH", ROOT / "model_metadata.json"))
GROUP_CODE = os.getenv("AGRISOKO_GROUP_CODE", "COMBO_A3_G05")
APP_VERSION = os.getenv("AGRISOKO_APP_VERSION", "1.0.0")
MODEL_VERSION = "tfidf-v1"
MATCH_THRESHOLD = float(os.getenv("AGRISOKO_MATCH_THRESHOLD", "0.45"))
MAX_QUESTION_LENGTH = 300

