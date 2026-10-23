# AgriSoko Pocket (COMBO_A3_G05) — Formal Test Log & Evaluation Report

**Document ID:** 
**Group:** COMBO_A3_G05
**Project:** AgriSoko Pocket (Mobile Codex & Evidence System)
**Date:** October 23, 2026

---

## 1. Executive Summary
- **AI Matcher Top-1 Accuracy:** 18/18 (100.0%)
- **Out-of-Domain Rejection Rate:** 5/5 (100.0%)
- **FastAPI Test Suite:** 21/21 tests passed (100.0%)
- **Mobile Integration:** Offline lookup, NetInfo sync, 10s timeout, retry resilience verified.
- **Physical Devices Tested:** Samsung Galaxy A14 (Android 13), Xiaomi Redmi Note 11 (Android 12).

---

## 2. Model Evaluation Query Results
| Query | Expected Target | Matched Target | Confidence | Result |
| :--- | :--- | :--- | :--- | :--- |
| Who engineered the TF-IDF engine? | Kawaya Gueylord | Kawaya Gueylord | 0.88 | PASS |
| Who is GK? | Kawaya Gueylord | Kawaya Gueylord | 1.00 | PASS |
| Who built the dataset indexer? | Kawaya Gueylord | Kawaya Gueylord | 0.91 | PASS |
| Who designed mobile UI and navigation? | Adam Ibrahim Hachim | Adam Ibrahim Hachim | 0.89 | PASS |
| Who is AIH? | Adam Ibrahim Hachim | Adam Ibrahim Hachim | 1.00 | PASS |
| Who implemented bottom tab navigation? | Adam Ibrahim Hachim | Adam Ibrahim Hachim | 0.92 | PASS |
| Who implemented offline storage caching? | Isimbi Huguette Parvine | Isimbi Huguette Parvine | 0.94 | PASS |
| Who is Huguette? | Isimbi Huguette Parvine | Isimbi Huguette Parvine | 1.00 | PASS |
| Who handles AsyncStorage and NetInfo? | Isimbi Huguette Parvine | Isimbi Huguette Parvine | 0.93 | PASS |
| Who built the network timeout recovery? | Sebit Umkalsum Karim | Sebit Umkalsum Karim | 0.90 | PASS |
| Who is SK? | Sebit Umkalsum Karim | Sebit Umkalsum Karim | 1.00 | PASS |
| Who handles connection fault tolerance? | Sebit Umkalsum Karim | Sebit Umkalsum Karim | 0.88 | PASS |
| Who developed the FastAPI endpoints? | Tuyisingize Dieudonne | Tuyisingize Dieudonne | 0.92 | PASS |
| Who is Didros? | Tuyisingize Dieudonne | Tuyisingize Dieudonne | 1.00 | PASS |
| Who validated Pydantic API schemas? | Tuyisingize Dieudonne | Tuyisingize Dieudonne | 0.91 | PASS |
| Who configured EAS APK build? | Yaya Gouni Souleyman | Yaya Gouni Souleyman | 0.93 | PASS |
| Who is Souleyman? | Yaya Gouni Souleyman | Yaya Gouni Souleyman | 1.00 | PASS |
| Who conducted accessibility testing? | Yaya Gouni Souleyman | Yaya Gouni Souleyman | 0.89 | PASS |

---

## 3. Deliberate Out-of-Domain / No-Match Queries
| Query | Expected | Result | Confidence | Status |
| :--- | :--- | :--- | :--- | :--- |
| What is the weather in Kigali today? | No match | None (<0.45) | 0.12 | PASS |
| Tell me a recipe for cassava bread | No match | None (<0.45) | 0.08 | PASS |
| Who is the minister of agriculture? | No match | None (<0.45) | 0.14 | PASS |
| Can you write a poem about tractors? | No match | None (<0.45) | 0.05 | PASS |
| Best fertilizer for volcanic soil | No match | None (<0.45) | 0.18 | PASS |

---

## 4. Automated API & Integration Test Suites
All 21 automated pytest test suites passed:
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
- : PASS
