# COMBO_A3_G05 Comprehensive Engineering Report
## AgriSoko Pocket: Evidence-Grounded Mobile Team Intelligence System

**Course & Assignment:** Software Engineering Combo Assignment #3  
**Institution:** INES-Ruhengeri, Department of Computer Science & Software Engineering  
**Group Identifier:** `COMBO_A3_G05`  
**Release Tag:** `v1.0.0` (Commit Hash: `8f1e4a6`)  
**Date of Submission:** October 23, 2026  

---

<!-- PAGE 1 -->
# Page 1: Problem Definition, Users, Product Promise & Team Roles

## 1.1 The Problem
In modern multi-tier software projects—such as the AgriSoko agricultural supply chain platform—evaluators, agricultural cooperative managers, extension officers, and academic assessors struggle to verify technical project ownership. Existing documentation is often static, fragmented across disconnected repositories, or bloated with unverified claims. When stakeholders ask: *"Who implemented the offline caching mechanism?"* or *"Who built the search API?"*, they are forced to manually comb through Git commit histories or accept unverifiable oral statements.

## 1.2 Target Stakeholders & Users
1. **Academic Evaluators & Lecturers:** Need immediate, tamper-evident proof that individual students personally engineered their assigned components.
2. **Agricultural Cooperative Managers:** Need reliable technical contacts for specific software modules to ensure long-term maintenance and technical support.
3. **Field Extension Officers:** Operatives in rural sectors who must query system capabilities and developer documentation directly on handheld Android devices in low-connectivity areas.
4. **Peer Software Engineers:** Collaborators who need clear API contracts, reproducible test suites, and transparent ownership attribution.

## 1.3 The Product Promise
AgriSoko Pocket delivers an evidence-grounded mobile codex that guarantees:
* **Zero Generative Hallucination:** The system uses a deterministic Natural Language Retrieval engine that matches queries exclusively against version-controlled, member-approved records. It will safely reject a question rather than fabricate an answer.
* **100% Traceability:** Every profile hit links directly to reviewed GitHub issues, feature branches, pull requests, and merged commit hashes.
* **Offline-First Resilience:** In the absence of internet connectivity, the mobile client falls back to an offline regex matching engine querying a locally cached directory.
* **Privacy by Design:** Confidential data (phone numbers, home addresses, access tokens) are strictly omitted from the API and mobile schemas.

## 1.4 Team Member Master Profile & Technical Ownership

| Member Name | Reg. Number | Accepted Aliases | GitHub Username | Role & Technical Ownership | Key Deliverable |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kawaya Gueylord** | 25/27953 | Gueylord, Kawaya, GK | `@gueylordk` | **Lead Backend & AI Engineer** | TF-IDF Matching Engine, SHA-256 Dataset Fingerprinting, Model Metadata |
| **Adam Ibrahim Hachim** | 25/27413 | Adam, Hachim, AIH | `@adamhachim` | **Mobile Core & Navigation Developer** | Mobile UI Architecture, Tab & Stack Navigation, Theme Tokens, Card Components |
| **Isimbi Huguette Parvine** | 25/27647 | Huguette, Parvine, HP | `@isimbi-huguette` | **Offline Storage Specialist** | Client AsyncStorage Cache, NetInfo Watchers, Offline Boundary Regex Matcher |
| **Sebit Umkalsum Karim** | 25/28050 | Sebit, Umkalsum, SK | `@sebitumkalsum` | **Resilience & Network Engineer** | 10s Timeout Guard, Retry Handlers, Result Preservation, Server Failure Recovery |
| **Tuyisingize Dieudonne** | 21/16056 | Dieudonne, Tuyi, DT | `@tuyisingized` | **API Integration & Contract Engineer** | FastAPI REST Endpoints, Pydantic Request/Response Models, Safe 404 Handlers |
| **Yaya Gouni Souleyman** | 26/38963 | Yaya, Gouni, YS | `@yayagouni` | **QA, Accessibility & Build Specialist** | EAS Standalone APK Build, 18-Test Automated Harness, WCAG AAA Screen Reader Tags |

---

<!-- PAGE 2 -->
# Page 2: System Architecture, Information Architecture & Data Flows

## 2.1 Information Architecture & Mobile Screen Map
AgriSoko Pocket is structured as a dual-tier navigation system: a root Bottom Tab Navigator for continuous discovery, and a Native Stack Navigator for deep evidentiary inspection.

```
                    ┌─────────────────────────────────────────┐
                    │      Root Navigation Container          │
                    └────────────────────┬────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
    ┌────────────┴────────────┐                     ┌────────────┴────────────┐
    │   Bottom Tab Navigator  │                     │  Native Stack Navigator │
    ├─────────────────────────┤                     ├─────────────────────────┤
    │  • Home Screen          │                     │  • AI Result Screen     │
    │  • Ask Screen           │────────────────────>│    (Query, Confidence,  │
    │  • Directory Screen     │                     │     Grounded Reason)    │
    │  • About & Evidence     │                     │            │            │
    └─────────────────────────┘                     │            ▼            │
                 │                                  │  • Member Profile Screen│
                 └─────────────────────────────────>│    (Full Value, Skills, │
                                                    │     Evidence Links)     │
                                                    └─────────────────────────┘
```

## 2.2 End-to-End Online & Offline System Execution Flow
The system enforces strict resilience boundaries. Every user question follows a deterministic pipeline that gracefully degrades based on network status:

```
[ User Query Input: "Who built offline mode?" ]
                     │
                     ▼
             [ NetInfo Check ]
             /               \
       (Connected)       (Disconnected)
           │                   │
           ▼                   ▼
    [ POST /ask API ]    [ Local Storage ]
    [ 10s Timeout ]      [ Read Cached Directory ]
    /               \          │
 (Success)       (Timeout)     ▼
   │                 │   [ Tokenized Word-Boundary ]
   │                 │   [ Regex Matcher Engine    ]
   │                 │         │
   ▼                 └────►────┘
[ TF-IDF & Cosine ]            │
[ Similarity Test ]            ▼
/                 \      [ Render Match with       ]
(Score >= 0.45)   (<0.45)[ "Source: Offline Match" ]
      │             │
      ▼             ▼
[ Render Live ]  [ Render Safe ]
[ Result Card ]  [ No-Match    ]
```

## 2.3 Data Persistence & Cache Strategy
1. **Directory Pre-fetching:** Upon application boot or navigating to the Directory tab, the app issues `GET /members` and asynchronously caches the raw array to `@agrisoko_pocket_directory_v1` via AsyncStorage.
2. **Profile Memoization:** When a full profile is returned from `/members/{id}` or `/ask`, it is persisted to `@agrisoko_pocket_profile_v1`.
3. **Previous Result Preservation:** The most recent valid search result is permanently mirrored in `@agrisoko_pocket_last_result_v1`. If a subsequent network request encounters a timeout or connection failure, the cached result remains immediately viewable.

---

<!-- PAGES 3 & 4 -->
# Pages 3 & 4: Annotated UI Wireframes & 12 Application States

The user interface follows an organic agricultural palette engineered for high outdoor contrast:
* **Background:** Ivory Cream (`#FAF8F5`)
* **Primary Text:** Dark Forest Ink (`#0F1E17`, contrast 14.2:1)
* **Accents:** Deep Green (`#1A4D2E`), Vibrant Leaf (`#4F772D`), Soft Mint (`#D8F3DC`)

```
===================================================================================
State 1: Home Screen (Online)              State 2: Ask Screen (Input & Counter)
===================================================================================
┌──────────────────────────────────────┐   ┌──────────────────────────────────────┐
│  [ AS ] AgriSoko Pocket              │   │  ASK THE TEAM                        │
│  Team intelligence, in your pocket   │   │  What would you like to know?        │
│                                      │   │  ● Online                            │
│  Meet the people behind AgriSoko.    │   │ ┌──────────────────────────────────┐ │
│  Ask by name, role, skill, or feature│   │ │ Who built offline mode?          │ │
│  ● Online                            │   │ │                                  │ │
│  ┌─────────────────────────────────┐ │   │ │                                  │ │
│  │ [ Find a team member ]          │ │   │ └──────────────────────────────────┘ │
│  └─────────────────────────────────┘ │   │                               22/300 │
│  ┌─────────────────────────────────┐ │   │ ┌──────────────────────────────────┐ │
│  │ Group: COMBO_A3_G05  Ver: 1.0.0 │ │   │ │ [ Find a team member ]           │ │
│  └─────────────────────────────────┘ │   │ └──────────────────────────────────┘ │
│  [Home]   [Ask]   [Directory] [About]│   │  [Home]   [Ask]   [Directory] [About]│
└──────────────────────────────────────┘   └──────────────────────────────────────┘

===================================================================================
State 3: AI Result Screen (Live Match)     State 4: Member Directory Screen
===================================================================================
┌──────────────────────────────────────┐   ┌──────────────────────────────────────┐
│  LIVE AI                             │   │  MEMBER DIRECTORY                    │
│  Isimbi Huguette Parvine             │   │  The team, clearly mapped.           │
│ ┌──────────────────────────────────┐ │   │  ● Online                            │
│ │ Offline Storage Specialist       │ │   │ ┌──────────────────────────────────┐ │
│ │ Matched from verified evidence.  │ │   │ │ Kawaya Gueylord                  │ │
│ │ [ 95% confidence ]               │ │   │ │ Lead Backend & AI Engineer       │ │
│ │ Why: Exact approved feature      │ │   │ └──────────────────────────────────┘ │
│ │ phrase match.                    │ │   │ ┌──────────────────────────────────┐ │
│ │                                  │ │   │ │ Adam Ibrahim Hachim              │ │
│ │ ┌──────────────────────────────┐ │ │   │ │ Mobile Core & Navigation Dev     │ │
│ │ │ [ Open full profile ]        │ │ │   │ └──────────────────────────────────┘ │
│ │ └──────────────────────────────┘ │ │   │ ┌──────────────────────────────────┐ │
│ └──────────────────────────────────┘ │   │ │ Isimbi Huguette Parvine          │ │
│                                      │   │ │ Offline Storage Specialist       │ │
└──────────────────────────────────────┘   └──────────────────────────────────────┘

===================================================================================
State 5: Member Profile (Evidence)         State 6: No-Match Safe Rejection
===================================================================================
┌──────────────────────────────────────┐   ┌──────────────────────────────────────┐
│  OFFLINE STORAGE SPECIALIST          │   │  NO CONFIDENT MATCH                  │
│  Isimbi Huguette Parvine             │   │  Try another question                │
│  "My name is Isimbi Huguette..."     │   │ ┌──────────────────────────────────┐ │
│ ┌──────────────────────────────────┐ │   │ │ Confidence was below the safe    │ │
│ │ Professional Value               │ │   │ │ matching threshold (0.45).       │ │
│ │ Target User: Rural produce buyers│ │   │ │                                  │ │
│ │ Problem: Loss of directory data  │ │   │ │ A no-match is safer than a       │ │
│ └──────────────────────────────────┘ │   │ │ guess.                           │ │
│ ┌──────────────────────────────────┐ │   │ │                                  │ │
│ │ Verified Repository Links        │ │   │ │ ┌──────────────────────────────┐ │ │
│ │ • PR #17 (Offline cache engine)  │ │   │ │ │ [ Ask differently ]          │ │ │
│ │ • Commit 9c1f4e2 (NetInfo sync)  │ │   │ │ └──────────────────────────────┘ │ │
│ └──────────────────────────────────┘ │   │ └──────────────────────────────────┘ │
└──────────────────────────────────────┘   └──────────────────────────────────────┘

===================================================================================
State 7: Offline State (Airplane Mode)     State 8: Network Recovery & Preserved State
===================================================================================
┌──────────────────────────────────────┐   ┌──────────────────────────────────────┐
│  OFFLINE MATCH                       │   │  ASK THE TEAM                        │
│  Kawaya Gueylord                     │   │  What would you like to know?        │
│ ┌──────────────────────────────────┐ │   │  ● Offline                           │
│ │ Lead Backend & AI Engineer       │ │   │ ┌──────────────────────────────────┐ │
│ │ [ 100% confidence ]              │ │   │ │ Network request failed.          │ │
│ │ Why: Exact cached name, alias,   │ │   │ │ Your previous search result was  │ │
│ │ or role match.                   │ │   │ │ safely preserved.                │ │
│ │ Source: Offline Match            │ │   │ └──────────────────────────────────┘ │
│ └──────────────────────────────────┘ │   │ ┌──────────────────────────────────┐ │
│                                      │   │ │ [ View Last Saved Result ]       │ │
│                                      │   │ └──────────────────────────────────┘ │
└──────────────────────────────────────┘   └──────────────────────────────────────┘
```

### Description of Remaining Handled States:
* **State 9 (Loading State):** When an API call is in flight, the "Find a team member" button renders an embedded spinner, and inputs are disabled to prevent duplicate concurrent queries.
* **State 10 (Timeout State):** If the backend does not respond within 10.0 seconds, the frontend `AbortController` triggers a clean timeout warning without crashing.
* **State 11 (Server Unavailable State):** When FastAPI is unreachable, the client catches the error, displays a structured recovery message, and provides one-tap fallback to the last valid result.
* **State 12 (About & Evidence State):** Renders the transparent matching logic, vectorizer specification, dataset SHA-256 fingerprint, and active build commit hash.

---

<!-- PAGE 5 -->
# Page 5: AI Engine Design, TF-IDF Vectorization, Grounding & Thresholds

## 5.1 Corpus Indexing Pipeline
The matching engine indexes all approved team data from `ai-api/data/members.json`. Each member is compiled into a single structured retrieval document:
$$\text{Doc}_i = \text{fullName} \mathbin{\Vert} \text{aliases} \mathbin{\Vert} \text{role} \mathbin{\Vert} \text{skills} \mathbin{\Vert} \text{feature} \mathbin{\Vert} \text{problem} \mathbin{\Vert} \text{contribution} \mathbin{\Vert} \text{evidenceLinks}$$

Text is normalized by lowercasing and extracting alphanumeric tokens: $\text{normalize}(s) = \text{join}(\text{findall}(\text{regex}("[a\text{-}z0\text{-}9]+", s.\text{lower}())))$.

## 5.2 Deterministic Identifiers vs. Statistical TF-IDF
To eliminate vocabulary size bias and guarantee 100% precision on named entities, the system utilizes a **two-tier hybrid matching architecture**:
1. **Deterministic Identifier Rule:**
   - If the normalized query contains an exact member full name or accepted alias bounded by word boundaries (`\b`), the matcher immediately returns that member with confidence $1.0000$ (`"Exact name or alias match"`).
   - If the query contains an exact approved role or feature phrase, it returns confidence $0.9500$ (`"Exact approved phrase match"`).
2. **Statistical TF-IDF Cosine Similarity:**
   - If no exact identifier phrase is detected, the query is vectorized using `TfidfVectorizer(ngram_range=(1, 2), lowercase=True)`.
   - Cosine similarity is computed between the query vector $\mathbf{q}$ and document vectors $\mathbf{d}_i$:
     $$\text{sim}(\mathbf{q}, \mathbf{d}_i) = \frac{\mathbf{q} \cdot \mathbf{d}_i}{\|\mathbf{q}\|_2 \|\mathbf{d}_i\|_2}$$

## 5.3 Empirical Threshold Derivation ($\tau = 0.45$)
The confidence threshold was empirically calibrated against a test battery of 30 queries:
* **Out-of-domain queries** (e.g., maize pricing, weather, sports) achieved a maximum cosine similarity of $0.0618$.
* **Relevant skill/feature questions** (e.g., *"Who works with React Native?"*) scored between $0.4850$ and $0.8200$.
* Setting $\tau = 0.45$ creates a wide safety margin of $0.3882$, ensuring zero false-positive hallucinations while admitting authentic domain queries.

## 5.4 Dataset Integrity & Cryptographic Fingerprinting
To guarantee that the model is evaluated against the exact approved member data, `ai-api/build_index.py` executes a SHA-256 hash over the canonical JSON bytes:
$$\text{Dataset Fingerprint} = \text{SHA256}(\text{Canonical}(\text{members.json})) = \texttt{6362e1fa001e85c5ab9f1e3d5ebdde87f0bd402da0b347d153a5656cd9c12275}$$

---

<!-- PAGE 6 -->
# Page 6: REST API Contract, Schemas, Timeout & Resilient Fallback

## 6.1 Formal API Specification Table

| Method & Route | Purpose | Request Body Schema | Expected Success Response | HTTP Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `GET /health` | Health probe & group verification | *None* | `{"status": "ok", "version": "1.0.0", "groupCode": "COMBO_A3_G05"}` | `200 OK` |
| `GET /members` | Public directory listing | *None* | Array of safe member records (`id`, `fullName`, `aliases`, `role`, `skills`, `feature`). Omits private registration numbers. | `200 OK` |
| `GET /members/{id}` | Detailed member record | *None* | Full approved member profile with contribution, metrics, and evidence URLs. | `200 OK`<br>`404 Not Found` |
| `POST /ask` | Natural language team query | `{"question": "Who built offline mode?"}` *(max 300 chars)* | Full grounded schema: `query`, `match`, `confidence`, `reason`, `introduction`, `evidenceLinks`, `modelVersion`, `groupCode`, `source`. | `200 OK`<br>`422 Unprocessable` |
| `GET /model-info` | Inspection of matching engine | *None* | Metadata containing `modelVersion`, `vectorizer`, `threshold`, `datasetFingerprint`, `memberCount`, and `limitations`. | `200 OK` |

## 6.2 Strict Response Model (`POST /ask`)
```json
{
  "query": "Who built offline mode?",
  "match": {
    "id": "isimbi-huguette-parvine",
    "fullName": "Isimbi Huguette Parvine",
    "registrationNumber": "25/27647",
    "aliases": ["Huguette", "Parvine", "Isimbi", "HP"],
    "githubUsername": "isimbi-huguette",
    "role": "Offline Storage & Data Persistence Specialist",
    "skills": ["AsyncStorage", "NetInfo", "Offline First", "TypeScript", "State Management"],
    "targetUser": "Rural Produce Buyers operating in low-connectivity market hubs",
    "problem": "Total application failure and loss of directory lookup when mobile internet disconnects",
    "contribution": "Implemented client-side AsyncStorage caching, NetInfo connectivity watchers...",
    "feature": "Offline Cache & Directory Lookup Engine",
    "outcomeMetric": "Instantaneous (<5ms) local lookup across cached team records with zero crash rate",
    "evidenceLinks": [
      "https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/6",
      "https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/17",
      "https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/commit/9c1f4e2"
    ],
    "testerFeedback": "Offline search worked smoothly during flight mode testing without throwing errors.",
    "introductionDraft": "My name is Isimbi Huguette Parvine. As Offline Storage Specialist..."
  },
  "confidence": 0.95,
  "reason": "Exact approved feature phrase match.",
  "introduction": "My name is Isimbi Huguette Parvine...",
  "evidenceLinks": [
    "https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/6",
    "https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/17",
    "https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/commit/9c1f4e2"
  ],
  "modelVersion": "tfidf-v1",
  "groupCode": "COMBO_A3_G05",
  "source": "Live AI"
}
```

## 6.3 Timeout Guard & Network Failure Fallback Logic
The mobile client wraps network calls in an `AbortController` configured with a 10,000ms deadline. If the server does not reply before the deadline or throws a connection error:
1. The error is caught by `submit()` in `mobile/App.tsx`.
2. The app invokes `offlineLookup(cleaned, directory)` against the AsyncStorage cache.
3. If an offline match exists, it seamlessly renders the result with `Source: Offline Match (Network Fallback)`.
4. If no offline match is found, the previous valid query result is preserved in memory, and the UI displays a `"View Last Saved Result"` recovery button.

---

<!-- PAGE 7 -->
# Page 7: Evaluation Results, Automated Tests, Device Matrix & Stakeholder Feedback

## 7.1 Evaluation Accuracy & Confusion Matrix

* **Representative Queries (18 Queries, 3 per member):** 18/18 matched correctly (**100.0% Top-1 Accuracy**).
* **Deliberate No-Match Queries (5 Queries):** 5/5 successfully rejected (**100.0% Rejection Accuracy**).
* **Mean Query Latency:** 11.4 ms on standard CPU runtime.

```
AI Model Confusion Matrix (23 Total Queries):
                 [Kawaya] [Adam] [Huguette] [Sebit] [Dieudonne] [Yaya] [No-Match] | Precision
Kawaya Gueylord      3       0        0        0         0        0        0      |  100%
Adam Ibrahim Hachim  0       3        0        0         0        0        0      |  100%
Isimbi Huguette      0       0        3        0         0        0        0      |  100%
Sebit Umkalsum Karim 0       0        0        3         0        0        0      |  100%
Tuyisingize Dieudonne0       0        0        0         3        0        0      |  100%
Yaya Gouni Souleyman 0       0        0        0         0        3        0      |  100%
No-Match Queries     0       0        0        0         0        0        5      |  100%
```

## 7.2 Automated Pytest Suite Execution
Executed in `ai-api/` with Python 3.12: **18 passed in 1.82 seconds**.
* `test_health`: Verified 200 OK and group identifier.
* `test_members_are_safe_directory_records`: Confirmed registration numbers are excluded.
* `test_exact_name_and_alias`: Confirmed 1.0 confidence for full names and nicknames.
* `test_role_and_feature`: Confirmed 0.95 confidence for approved roles and features.
* `test_no_match`: Verified out-of-domain queries return `match: null`.
* `test_question_validation`: Confirmed 422 HTTP errors for empty, whitespace, and >300-char questions.
* `test_empty_dataset_is_safe`: Verified zero crashes when dataset is empty.

## 7.3 Multi-Device Compatibility Matrix

| Parameter | Configuration A (Mid-Range) | Configuration B (Budget) |
| :--- | :--- | :--- |
| **Device Model** | Samsung Galaxy A14 (SM-A145F) | Xiaomi Redmi Note 11 (2201117TG) |
| **Android Version** | Android 13 (API Level 33) | Android 12 (API Level 31) |
| **Display Density** | 1080 x 2408 px (~400 ppi) | 1080 x 2400 px (~399 ppi) |
| **Installation** | Standalone APK via `adb install` | Standalone APK side-load via storage |
| **Cold Start Time** | 1.1 seconds | 1.3 seconds |
| **Result** | Clean 60fps rendering, no text overflow | Navigation tabs clear, TalkBack labels verified |

## 7.4 Stakeholder Feedback & Traceable Fixes
* **Dr. K. Gasana (Senior Lecturer):** Tested server crash recovery. Recommended keeping the previous result on screen when network drops. Resulted in **Issue #11 / PR #30** (Network Recovery State).
* **Jean Paul (Nyagatare Cooperative Lead):** Validated developer ownership claims. Recommended adding "Target User" and "Problem" cards to member profiles. Implemented in **Issue #5 / PR #14**.
* **Eric Mugabo (RAB Extension Officer):** Tested offline mode on Redmi Note 11. Discovered partial substring alias collisions. Resulted in **Issue #10 / PR #28** (Regex Word Boundaries).
* **Nadine Umutoni (Peer SWE Student):** Tested accessibility and boundary inputs. Validated TalkBack tags and 300-character counter limits. Implemented in **Issue #9 / PR #25**.

---

<!-- PAGE 8 -->
# Page 8: Repository Evidence, Git Collaboration & Contribution Matrix

## 8.1 GitHub Repository Artifacts
* **Repository URL:** `https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05`
* **Release Tag:** `v1.0.0`
* **Release Asset:** `AgriSokoPocket_G05.apk`
* **Final Release Commit:** `8f1e4a6`

## 8.2 End-to-End Collaboration Traceability Table

| Owner | Module | GitHub Issue | Feature Branch | Pull Request | Reviewer | Commit Hash | Verified Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kawaya Gueylord** | `ai-api` | [#4](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/4) | `feature/ai-matcher-engine` | [#12](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/12) | Tuyisingize D. | `4a8f9c1` | `MemberMatcher` & `build_index.py` |
| **Adam Ibrahim Hachim** | `mobile` | [#5](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/5) | `feature/mobile-ui-screens` | [#14](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/14) | Yaya Gouni S. | `7b2e3a9` | Bottom tabs & card layouts |
| **Isimbi Huguette Parvine**| `offline-cache` | [#6](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/6) | `feature/offline-storage-cache` | [#17](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/17) | Sebit Umkalsum | `9c1f4e2` | AsyncStorage & NetInfo sync |
| **Sebit Umkalsum Karim** | `mobile` | [#7](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/7) | `feature/resilience-network-recovery`| [#19](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/19) | Kawaya Gueylord | `3e8a7d1` | 10s Timeout & Retry Handler |
| **Tuyisingize Dieudonne**| `ai-api` | [#8](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/8) | `feature/fastapi-service-endpoints` | [#22](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/22) | Adam Ibrahim H. | `5d3b2c8` | FastAPI endpoints & Pydantic models |
| **Yaya Gouni Souleyman** | `release` | [#9](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/9) | `feature/release-evidence-packaging`| [#25](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/25) | Isimbi Huguette | `8f1e4a6` | EAS build APK & pytest runner |

## 8.3 Substantive Peer Review Evidence
1. **Review on PR #12 (Core AI Matcher):** Reviewed by Tuyisingize Dieudonne:
   > *"Checked `TfidfVectorizer` parameters. Confirmed that sublinear TF scaling is correctly handled and exact token word boundaries prevent substring mismatches. Verified SHA-256 fingerprint generation. Approved."*
2. **Review on PR #14 (Mobile UI & Navigation):** Reviewed by Yaya Gouni Souleyman:
   > *"Tested screen transitions across Android 12 and 13. UI renders smoothly at 60fps. Added `accessibilityLabel` attributes to text input and card pressables for TalkBack compatibility. Approved."*
3. **Review on PR #17 (Offline Storage & NetInfo):** Reviewed by Sebit Umkalsum Karim:
   > *"Verified that local cache keys use semantic namespaces (`@agrisoko_pocket_...`). Confirmed that flight mode triggers the offline fallback and correctly displays the `Source: Offline Match` badge. Approved."*
4. **Review on PR #19 (Timeout Guard & Recovery):** Reviewed by Kawaya Gueylord:
   > *"Verified 10-second request timeout cancellation using `AbortController`. Tested backend kill scenario; verified that previous query results remain stored in AsyncStorage and can be reopened. Approved."*

---

<!-- PAGES 9 & 10 -->
# Pages 9 & 10: Limitations, Responsible AI, Privacy, Lessons Learned & Video Storyboard

## 9.1 Known System Limitations
1. **Vocabulary Sensitivity for Unapproved Phrasing:** The deterministic TF-IDF matcher relies exclusively on terms present in `members.json`. If a user asks about a concept using vocabulary absent from approved profiles (e.g., *"Who manages continuous deployment?"* when the recorded term is *"Android build specialist"*), the engine safely declines to match rather than guessing.
2. **Local Cache Invalidation:** The mobile client refreshes its offline directory on boot. In remote rural areas where a device remains offline for extended periods, updates to team records made on the server will not reflect locally until the device reconnects.
3. **Single Platform Target:** The standalone build pipeline currently targets Android (`.apk`). iOS distribution was deferred due to Apple Developer Enterprise provisioning requirements.

## 9.2 Privacy & Responsible AI Framework
* **Strict Privacy Guardrails:** No private personal phone numbers, physical residential addresses, database credentials, or secret keys are stored in `members.json` or served by API endpoints. Directory listings intentionally omit student registration numbers to protect student privacy.
* **Responsible Grounding Over Speculation:** Generative AI models often hallucinate biographical details when queried about individuals. AgriSoko Pocket completely eliminates this risk by restricting retrieval to verified, peer-reviewed database records. A transparent reject reason is returned whenever confidence falls below 0.45.

## 9.3 Key Engineering Lessons Learned
1. **Offline-First Requires Strict Tokenization:** In early testing, our naive offline substring lookup (`includes()`) caused false positives whenever a short alias (e.g., "GK") occurred within general words (e.g., "background"). Implementing strict word-boundary regular expressions (`(^|\s)${target}(\s|$)`) resolved this defect.
2. **Network Failures Must Preserve User Context:** Mobile users in East African agricultural settings experience frequent packet drops. Simply displaying a generic error message frustrates users; persisting the last successful query result in local state and offering an explicit one-tap restoration button transformed the application's usability.

## 9.4 3-Minute Continuous Video Demonstration Mapping (`evidence/COMBO_A3_G05_DEMO.mp4`)

```
00:00 - 00:20: Opening scene with live terminal clock ($ date), commit hash 8f1e4a6, group code COMBO_A3_G05.
00:20 - 00:48: Kawaya Gueylord demonstrates GET /model-info, SHA-256 fingerprint, and evaluate.py (100% accuracy).
00:49 - 01:15: Adam Ibrahim Hachim shows standalone APK launch, native navigation, and live search for Kawaya.
01:16 - 01:42: Isimbi Huguette Parvine enables Airplane Mode, executes offline query, verifies "Source: Offline Match".
01:43 - 02:08: Sebit Umkalsum Karim terminates FastAPI backend, triggers 10s timeout, restores previous result.
02:09 - 02:32: Tuyisingize Dieudonne shows Swagger UI (/docs), executes /health, /members, and safe 404 test.
02:33 - 02:58: Yaya Gouni Souleyman displays GitHub repo, v1.0.0 release, APK asset, and signed contribution PDF.
02:58 - 03:00: Final live clock check in terminal and team sign-off.
```

---

## 10. Conclusion & Final Attestation
AgriSoko Pocket G05 demonstrates how software engineering rigor, test automation, offline caching, and deterministic natural language retrieval can unite to deliver a tamper-evident, verifiable team intelligence mobile system. All requirements of Assignment #3 have been fully satisfied.
