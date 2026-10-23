import json
import subprocess

from app.data_loader import dataset_fingerprint, load_members
from app.matcher import MemberMatcher
from app.settings import DATA_PATH, MATCH_THRESHOLD, METADATA_PATH, MODEL_VERSION


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def main() -> None:
    members = load_members(DATA_PATH)
    MemberMatcher(members, MATCH_THRESHOLD)
    metadata = {
        "modelVersion": MODEL_VERSION,
        "vectorizer": "TfidfVectorizer(ngram_range=(1, 2), lowercase=True)",
        "threshold": MATCH_THRESHOLD,
        "datasetFingerprint": dataset_fingerprint(DATA_PATH),
        "memberCount": len(members),
        "buildCommit": git_commit(),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()

