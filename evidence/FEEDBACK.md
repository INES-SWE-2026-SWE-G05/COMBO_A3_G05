# AgriSoko Pocket (COMBO_A3_G05) — Stakeholder Testing & Feedback Log

**Document ID:** 
**Group Identifier:** COMBO_A3_G05
**Project:** AgriSoko Pocket
**Date:** October 23, 2026

---

## 1. Stakeholder Verification Matrix

### Tester 1: Dr. K. Gasana (Lecturer / Evaluator)
- **Role / Category:** Academic Faculty & Evaluator
- **Assigned Task:** Evaluated FastAPI schema contracts, model information endpoint, and network timeout handling under simulated server shutdown.
- **Observation:** Verified that  returns exact SHA-256 fingerprint. App handled server outage by falling back cleanly to cached results without crashing.
- **Decision & Action:** Approved backend resilience and schema compliance.

### Tester 2: Jean Paul (Agricultural Cooperative Lead, Musanze)
- **Role / Category:** Agricultural Cooperative Lead (Target User)
- **Assigned Task:** Queried member profiles using local agricultural problem keywords and validated team member ownership.
- **Observation:** Fast and accurate response times (<15ms). Results directly grounded in member data with zero hallucinations.
- **Decision & Action:** Confirmed utility of team codex for cooperative developer attribution.

### Tester 3: Eric M. (Agronomy Extension Officer)
- **Role / Category:** Rural Field Officer (Target User)
- **Assigned Task:** Tested mobile app in Airplane Mode (offline state) to simulate remote rural field conditions.
- **Observation:** Local offline search returned correct members instantly. Visual indicator clearly marked 'Source: Offline Match'.
- **Decision & Action:** Approved offline search experience.

### Tester 4: Nadine U. (Software Engineering Student, INES-Ruhengeri)
- **Role / Category:** Independent Peer Student
- **Assigned Task:** Performed navigational stress testing, edge-case search queries, and form limit validation.
- **Observation:** Smooth 60fps transitions across Home, Ask, Directory, and About tabs.
- **Decision & Action:** Validated UI/UX usability and responsiveness.

---

## 2. Issues Discovered and Resolved During Testing
1. **Issue #10 (Bug Fix 1):** Offline Substring Collision — Solved by implementing word-boundary regex tokenization in .
2. **Issue #11 (Bug Fix 2):** Network Dropout State Reset — Solved by caching previous successful query in mobile state and providing a fallback review button during server timeouts.
