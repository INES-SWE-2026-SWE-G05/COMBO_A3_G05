# AgriSoko Pocket (COMBO_A3_G05) — 3-Minute Demonstration Video Script & Storyboard

**File Requirement:** `evidence/COMBO_A3_G05_DEMO.mp4`  
**Max Duration:** 3 minutes (180 seconds)  
**Production Format:** Continuous, single-take, unedited live screen and device recording  
**Mandatory Visuals:** Live terminal/device clock, Group Code `COMBO_A3_G05`, Final Commit Hash `8f1e4a6`, all 6 members speaking.

---

## 1. Sequence & Timeline Breakdown (00:00 – 03:00)

```
00:00 - 00:20: Opening, Identity, Live Clocks, Group Code & Git State
00:20 - 00:48: Speaker 1 (Kawaya Gueylord) — Backend, AI Matcher, /model-info, Fingerprint
00:49 - 01:15: Speaker 2 (Adam Ibrahim Hachim) — Standalone APK Launch, UI Navigation, Search
01:16 - 01:42: Speaker 3 (Isimbi Huguette Parvine) — Airplane Mode, Offline Lookup & Source Tag
01:43 - 02:08: Speaker 4 (Sebit Umkalsum Karim) — Server Drop, Timeout Guard, Retry & Recovery
02:09 - 02:32: Speaker 5 (Tuyisingize Dieudonne) — FastAPI Endpoints, Swagger Docs & Schema
02:33 - 02:58: Speaker 6 (Yaya Gouni Souleyman) — GitHub Repo, v1.0.0 Release, APK & Sign-offs
02:58 - 03:00: Final Live Clock & Verification Close
```

---

## 2. Detailed Scene-by-Scene Script

### Scene 1: Introduction & Clock Verification (00:00 – 00:20)
* **Visual on Screen:**
  - Split screen showing physical Android device (Samsung Galaxy A14) and laptop terminal.
  - Terminal displays:
    ```bash
    $ date --iso-8601=seconds
    2026-10-23T07:11:42+02:00
    $ git log -1 --oneline
    8f1e4a6 (HEAD -> main, tag: v1.0.0) Release v1.0.0 standalone APK and evidence docs
    $ echo "GROUP: COMBO_A3_G05"
    GROUP: COMBO_A3_G05
    ```
* **Speaker:** Group Lead (Kawaya Gueylord)
* **Spoken Lines:**
  > *"Hello evaluators. We are Group COMBO_A3_G05 presenting AgriSoko Pocket version 1.0.0. Our live terminal clock is running on October 23, 2026, and our final commit hash is 8f1e4a6. All six team members will demonstrate their directly implemented features in this continuous, unedited 3-minute recording."*

---

### Scene 2: Backend AI Matching & Fingerprint Verification (00:20 – 00:48)
* **Visual on Screen:**
  - Terminal running FastAPI service at `http://127.0.0.1:8000`.
  - Browser/Curl showing `GET /model-info`:
    ```json
    {
      "modelVersion": "tfidf-v1",
      "threshold": 0.45,
      "datasetFingerprint": "6362e1fa001e85c5ab9f1e3d5ebdde87f0bd402da0b347d153a5656cd9c12275",
      "memberCount": 6,
      "buildCommit": "8f1e4a6"
    }
    ```
  - Running `python evaluation/evaluate.py` showing `top1Accuracy: 1.0` and `noMatchRejectionAccuracy: 1.0`.
* **Speaker:** Kawaya Gueylord (Lead Backend & AI Engineer)
* **Spoken Lines:**
  > *"My name is Kawaya Gueylord. I engineered the deterministic TF-IDF matching engine and dataset fingerprint pipeline. Here is our GET /model-info endpoint with our SHA-256 fingerprint ending in 12275 and our 0.45 confidence threshold. Running our evaluation test suite confirms 100% top-1 accuracy across all 18 team queries and 100% rejection on out-of-domain queries with zero hallucination."*

---

### Scene 3: Standalone Mobile Launch & Live Query Demonstration (00:49 – 01:15)
* **Visual on Screen:**
  - Physical Android home screen showing app icon titled "AgriSoko Pocket".
  - Tapping icon: pure standalone cold start (No Expo Go splash screen).
  - Home screen renders hero badge "AS", `COMBO_A3_G05`, and green "Online" pill.
  - Tapping "Ask the team" tab; typing "Tell me about Kawaya Gueylord" -> displays matched profile with 100% confidence.
  - Typing "Who built Mobile UI & Navigation Architecture?" -> displays Adam Ibrahim Hachim with 95% confidence.
  - Tapping "Open full profile" to show GitHub PR and commit links.
* **Speaker:** Adam Ibrahim Hachim (Mobile Core & Navigation Developer)
* **Spoken Lines:**
  > *"My name is Adam Ibrahim Hachim. I designed the responsive mobile interface and navigation architecture. As seen on this physical device, AgriSoko Pocket launches as a native standalone APK. Querying an exact name or feature immediately returns the grounded member card, confidence score, and verified repository links."*

---

### Scene 4: Offline Persistence & Offline Match Demonstration (01:16 – 01:42)
* **Visual on Screen:**
  - Swiping down Android notification drawer and enabling **Airplane Mode**.
  - App status pill immediately switches from green "Online" to orange "Offline".
  - Submitting query in Ask screen: "What did Huguette build?".
  - Result renders instantly:
    - Title: **Isimbi Huguette Parvine**
    - Source Tag: **Source: Offline Match**
    - Confidence: **100%**
    - Reason: "Exact cached name, alias, role, or feature match."
* **Speaker:** Isimbi Huguette Parvine (Offline Storage & Persistence Specialist)
* **Spoken Lines:**
  > *"My name is Isimbi Huguette Parvine. I implemented the AsyncStorage caching and NetInfo connectivity listeners. Notice that in Airplane Mode, the app detects zero network and executes our tokenized offline lookup algorithm against the local cache. The card explicitly displays 'Source: Offline Match' with instant retrieval."*

---

### Scene 5: Network Timeout, Server Failure & State Preservation (01:43 – 02:08)
* **Visual on Screen:**
  - Airplane mode turned off.
  - In laptop terminal, stopping Uvicorn server (`Ctrl+C`).
  - On phone, typing query: "Can you predict tomorrow's rainfall?".
  - App attempts connection, hits timeout guard, and cleanly transitions:
    - Alert: "Network request failed. Your previous search result was safely preserved."
    - "View Last Saved Result" button appears. Tapping it restores Huguette's profile without loss.
  - Restarting Uvicorn server; submitting out-of-domain query -> cleanly displays "No confident match" state.
* **Speaker:** Sebit Umkalsum Karim Mustafa (Resilience & Network Recovery Engineer)
* **Spoken Lines:**
  > *"My name is Sebit Umkalsum Karim Mustafa. I built the resilience and network recovery layer. When our backend was stopped, our 10-second timeout guard prevented freezing, preserved the user's previous search result, and provided a one-tap recovery button. Testing an out-of-domain query safely returned our no-match state."*

---

### Scene 6: REST API Contract & Schema Compliance (02:09 – 02:32)
* **Visual on Screen:**
  - Browser showing Swagger documentation at `http://127.0.0.1:8000/docs`.
  - Executing `GET /health` (`status: "ok"`).
  - Executing `GET /members` showing public directory records without private registration numbers.
  - Executing `GET /members/kawaya-gueylord` returning approved profile.
  - Executing `GET /members/invalid-user` showing clean `404 Not Found`.
* **Speaker:** Tuyisingize Dieudonne (API Integration & Schema Validation Engineer)
* **Spoken Lines:**
  > *"My name is Tuyisingize Dieudonne. I built the FastAPI REST endpoints and Pydantic validation models. Our API enforces strict schemas across /health, /members, and /ask. Directory endpoints sanitize sensitive data by omitting registration numbers, and invalid queries safely return standardized 404 responses."*

---

### Scene 7: GitHub Release, Standalone APK & Verified Artifacts (02:33 – 02:58)
* **Visual on Screen:**
  - Browser showing GitHub repository: `https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05`.
  - Displaying Releases page: tag `v1.0.0`.
  - Showing release asset: `AgriSokoPocket_G05.apk`.
  - Showing signed contribution file `evidence/CONTRIBUTIONS.pdf` with all 6 member signatures.
  - Showing `evidence/TEST_LOG.pdf` and `evidence/FEEDBACK.pdf`.
* **Speaker:** Yaya Gouni Souleyman (QA, Accessibility & Android Build Specialist)
* **Spoken Lines:**
  > *"My name is Yaya Gouni Souleyman. I managed the EAS standalone APK build pipeline and automated testing. Here is our GitHub release v1.0.0 with the standalone APK binary, our 18 passing automated tests, our tester feedback log with four verified evaluators, and our signed contribution attestation."*

---

### Scene 8: Final Clock Verification & Sign-off (02:58 – 03:00)
* **Visual on Screen:**
  - Terminal showing updated live clock:
    ```bash
    $ date --iso-8601=seconds
    2026-10-23T07:14:42+02:00
    ```
* **Speaker:** All Members (Unison)
* **Spoken Lines:**
  > *"Thank you. AgriSoko Pocket G05 is complete, tested, and ready for evaluation."*

