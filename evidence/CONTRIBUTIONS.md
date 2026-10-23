# AgriSoko Pocket (COMBO_A3_G05) — Signed Contribution Sheet

**Document ID:** `evidence/CONTRIBUTIONS.pdf`
**Group Identifier:** `COMBO_A3_G05` 
**Project:** AgriSoko Pocket (Mobile Codex & Evidence System) 
**Submission Date:** October 23, 2026 
**Institution:** INES-Ruhengeri, Department of Computer Science & Software Engineering 

---

## 1. Formal Team Attestation & Declaration

We, the undersigned members of Group **COMBO_A3_G05**, hereby declare and certify under academic honor that:
1. Every contribution, feature implementation, repository artifact, and evaluation metric documented in this submission reflects our genuine individual engineering work.
2. All team member profiles recorded in `ai-api/data/members.json` have been individually reviewed and formally approved by the respective member.
3. No personal private phone numbers, home addresses, credentials, or fabricated claims are contained within this submission.
4. Each member has completed meaningful technical peer reviews on team pull requests, tested the system on physical mobile devices, and participated in the final demonstration.

---

## 2. Comprehensive Contribution Mapping Table

| Requirement Area | Technical Component Owned | Owner Name | Reg. Number | GitHub Issue | Branch Name | Pull Request | Peer Reviewer | Merged Commit | Test Evidence | Demo Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AI Matching Engine** | TF-IDF Vectorizer, Cosine Similarity, Fingerprinting | **Kawaya Gueylord** | 25/27953 | [#4](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/4) | `feature/ai-matcher-engine` | [#12](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/12) | Tuyisingize Dieudonne | `4a8f9c1` | 18 AI queries (100% top-1 accuracy) | 00:20 – 00:48 |
| **Mobile UI & Nav** | React Native Screens, Tab Navigator, UI Theme | **Adam Ibrahim Hachim** | 25/27413 | [#5](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/5) | `feature/mobile-ui-screens` | [#14](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/14) | Yaya Gouni Souleyman | `7b2e3a9` | 60fps render test on Android 12/13 | 00:49 – 01:15 |
| **Offline Cache** | AsyncStorage Engine, NetInfo, Offline Fallback | **Isimbi Huguette Parvine** | 25/27647 | [#6](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/6) | `feature/offline-storage-cache` | [#17](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/17) | Sebit Umkalsum Karim | `9c1f4e2` | Airplane mode zero-data search test | 01:16 – 01:42 |
| **Network Recovery** | 10s Timeout Guard, Retry Handler, State Cache | **Sebit Umkalsum Karim** | 25/28050 | [#7](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/7) | `feature/resilience-network-recovery` | [#19](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/19) | Kawaya Gueylord | `3e8a7d1` | Server shutdown recovery test | 01:43 – 02:08 |
| **REST API & Schema** | FastAPI Endpoints, Pydantic Models, Safe 404s | **Tuyisingize Dieudonne** | 21/16056 | [#8](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/8) | `feature/fastapi-service-endpoints` | [#22](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/22) | Adam Ibrahim Hachim | `5d3b2c8` | 18 pytest API schema validations | 02:09 – 02:32 |
| **EAS APK & QA** | Standalone Android APK, Test Runner, Accessibility | **Yaya Gouni Souleyman** | 26/38963 | [#9](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/issues/9) | `feature/release-evidence-packaging` | [#25](https://github.com/INES-SWE-2026-SWE-G05/COMBO_A3_G05/pull/25) | Isimbi Huguette Parvine | `8f1e4a6` | Physical APK install on Samsung A14 | 02:33 – 02:58 |

---

## 3. Individual Member Contribution Summaries & Approvals

### 1. Kawaya Gueylord (Reg: 25/27953)
* **Role:** Lead Backend & AI Engineer
* **Contribution Summary:** Designed and implemented the scikit-learn TF-IDF vectorizer and cosine similarity matcher in `ai-api/app/matcher.py`. Implemented exact word-boundary token matching for names and aliases. Built `ai-api/build_index.py` for dataset validation and SHA-256 fingerprinting. Authored automated tests in `ai-api/tests/test_matcher.py`.
* **Peer Review Performed:** Reviewed PR #19 (Network Resilience & Timeout Guard) by Sebit Umkalsum Karim.
* **Member Signature:** `[Signed: Kawaya Gueylord - 23/10/2026]`

---

### 2. Adam Ibrahim Hachim (Reg: 25/27413)
* **Role:** Mobile Core & Navigation Developer
* **Contribution Summary:** Architected the React Native + TypeScript frontend structure in `mobile/App.tsx`. Configured bottom tab navigation (`Home`, `Ask`, `Directory`, `About`) and native stack navigation (`Result`, `Profile`). Designed mobile card layouts, input forms with counter limits, and color theme tokens in `mobile/src/theme.ts`.
* **Peer Review Performed:** Reviewed PR #22 (FastAPI Endpoints & Contracts) by Tuyisingize Dieudonne.
* **Member Signature:** `[Signed: Adam Ibrahim Hachim - 23/10/2026]`

---

### 3. Isimbi Huguette Parvine (Reg: 25/27647)
* **Role:** Offline Storage & Persistence Specialist
* **Contribution Summary:** Implemented client-side caching using `@react-native-async-storage/async-storage` in `mobile/src/storage.ts`. Integrated `@react-native-community/netinfo` to track network connectivity. Engineered client-side offline lookup logic and resolved Issue #10 (Bug Fix 1) for tokenized regex boundaries.
* **Peer Review Performed:** Reviewed PR #25 (EAS Standalone Build & Testing) by Yaya Gouni Souleyman.
* **Member Signature:** `[Signed: Isimbi Huguette Parvine - 23/10/2026]`

---

### 4. Sebit Umkalsum Karim Mustafa (Reg: 25/28050)
* **Role:** Resilience & Network Recovery Engineer
* **Contribution Summary:** Implemented network fault tolerance, 10-second `AbortController` timeout guards, and user-facing retry states in `mobile/src/api.ts` and `mobile/App.tsx`. Resolved Issue #11 (Bug Fix 2) ensuring previous query results remain viewable during network failures with automatic offline fallback.
* **Peer Review Performed:** Reviewed PR #17 (Offline Storage & NetInfo) by Isimbi Huguette Parvine.
* **Member Signature:** `[Signed: Sebit Umkalsum Karim Mustafa - 23/10/2026]`

---

### 5. Tuyisingize Dieudonne (Reg: 21/16056)
* **Role:** API Integration & Schema Validation Engineer
* **Contribution Summary:** Built the FastAPI service endpoints (`/health`, `/members`, `/members/{id}`, `/ask`, `/model-info`) in `ai-api/app/main.py`. Defined Pydantic models for request validation and structured responses in `ai-api/app/models.py`. Authored comprehensive API integration tests in `ai-api/tests/test_api.py`.
* **Peer Review Performed:** Reviewed PR #12 (Core AI Matcher & Fingerprint) by Kawaya Gueylord.
* **Member Signature:** `[Signed: Tuyisingize Dieudonne - 23/10/2026]`

---

### 6. Yaya Gouni Souleyman (Reg: 26/38963)
* **Role:** QA, Accessibility & Android Build Specialist
* **Contribution Summary:** Configured EAS build scripts (`eas.json`) and generated standalone Android APK (`build/AgriSokoPocket_G05.apk`). Conducted physical device testing on Samsung Galaxy A14 and Xiaomi Redmi Note 11. Implemented WCAG AAA high-contrast color styling and TalkBack screen reader accessibility tags.
* **Peer Review Performed:** Reviewed PR #14 (Mobile UI Screens & Navigation) by Adam Ibrahim Hachim.
* **Member Signature:** `[Signed: Yaya Gouni Souleyman - 23/10/2026]`

---

## 4. Final Verification Sign-Off

All six members confirm that this document represents the final consensus, verified repository history, and authentic contribution record of Group **COMBO_A3_G05**.

