# AgriSoko Pocket G05

AgriSoko Pocket is an evidence-grounded mobile team directory. Visitors ask about a member by name, alias, role, skill, or feature; a deterministic TF-IDF service returns the best approved profile or safely declines to guess.

## Repository

- GitHub: [INES-SWE-2026-SWE-G05/COMBO_A3_G05](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05)
- Clone: `git clone https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05.git`

> **Data status:** Group code `COMBO_A3_G05` and six member identities are configured. Roles, skills, contributions, metrics, links, introductions, and tester evidence remain blank until the team supplies and approves them.

## Architecture

- `mobile/`: Expo + React Native + TypeScript, React Navigation, AsyncStorage, NetInfo
- `ai-api/`: FastAPI, Pydantic, scikit-learn TF-IDF/cosine similarity, pytest
- `ai-api/data/members.json`: six production identity records with unprovided profile fields left blank
- `ai-api/tests/fixtures/`: clearly labelled fictional test-only records

The mobile build also contains all six approved profiles and a tolerant local matcher. It always prefers the live API when reachable; if the request fails or exceeds five seconds, it automatically returns a clearly labelled result from the profiles built into the app. The directory and member profiles therefore work on a first launch without internet or a running backend.

The API indexes names, aliases, roles, skills, features, problems, contributions, and evidence summaries with `TfidfVectorizer(ngram_range=(1, 2), lowercase=True)`. Results below `0.45` are rejected. Exact name/alias mentions are deterministically assigned confidence `1.0`; exact approved role/feature phrases receive `0.95`.

## Run the API

```bash
cd ai-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build_index.py
pytest
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## Run the mobile app

```bash
cd mobile
npm install
EXPO_PUBLIC_API_BASE_URL=http://YOUR_LAN_IP:8000 npx expo start
```

Android Emulator uses `http://10.0.2.2:8000` by default. A physical device needs the development computer's LAN address and both devices on the same network.

## Configure real group data

1. Review the configured `COMBO_A3_G05` app/release identifiers.
2. Complete the blank profile fields directly in `ai-api/data/members.json` using only member-approved facts.
3. Have every member approve their record.
4. Run `python build_index.py`, `pytest`, and `python evaluation/evaluate.py` from `ai-api/`.
5. Add at least three approved evaluation queries per member to `evaluation/queries.json`.

## API

- `GET /health`
- `GET /members`
- `GET /members/{id}`
- `POST /ask` with `{ "question": "Who built offline mode?" }`
- `GET /model-info`

## Build an APK

After setting the real Android package identifier and signing into the group's Expo account:

```bash
cd mobile
npx eas-cli build --platform android --profile preview
```

Download the resulting APK as `build/AgriSokoPocket_G05.apk`. APK/device/tester/repository evidence cannot be produced truthfully without the real group data, accounts, devices, and people.

## Evidence status

See [evidence/COMPLETION_STATUS.md](evidence/COMPLETION_STATUS.md). It distinguishes automated software verification from the real-world submission work that the team must perform.

