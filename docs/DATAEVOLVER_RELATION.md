# Relationship Between DataRSI and DataEvolver

This document clarifies the institutional, technical, and architectural relationship between **DataEvolver** and **DataRSI**.

---

## 1. Core Summary

> **"DataRSI is the research framework introduced in our ICASSP 2027 work. It builds on the synthetic-data construction infrastructure developed in DataEvolver and formalizes failure-driven dataset evolution as an auditable bounded revision process."**

- **DataEvolver Repository**: [https://github.com/PRIS-CV/DataEvolver](https://github.com/PRIS-CV/DataEvolver)
- **DataRSI Repository**: [https://github.com/PRIS-CV/DataRSI](https://github.com/PRIS-CV/DataRSI)

---

## 2. Technical Distinction

| Dimension | DataEvolver (Engineering Infrastructure) | DataRSI (Research Framework) |
|---|---|---|
| **Primary Identity** | Long-term engineering infrastructure & multi-modal dataset generation platform | ICASSP 2027 research paper methodology & audited testbed |
| **Chronology & Scope** | Developed earlier; encompasses broad synthetic-data construction tools | Built on DataEvolver's infrastructure; focuses on formal revision protocols |
| **Coverage** | T2I/T2V pipelines, 3D world models (HyWorld), multi-stage scene generation, web crawling, telemetry | Bounded supervision revision transactions, failure-to-data compilation, two-level admission gates |
| **Key Abstraction** | Procedural pipeline execution & asset asset staging pipelines | **Synthetic supervision as revision state** governed by immutable protocol $\Gamma$ |
| **Control Plane** | Multi-agent execution tools, cluster schedulers | Generation-time Data Self-Evolution Loop + Model Admission Loop |

---

## 3. Scope Boundaries & Non-Equivalence

To ensure technical and historical precision:

1. **Not a simple renaming**: DataRSI is not a rebranding or simple alias of DataEvolver. DataEvolver continues as an active open-source engineering platform.
2. **Not a reverse implementation**: DataEvolver is not an "implementation of DataRSI". DataEvolver originated earlier and supports many non-revision tasks.
3. **What DataRSI formalizes**: DataRSI isolates the scientific question of how downstream model failures can be compiled into registered 3D requests, repaired under deterministic contracts, and guarded against regressions.
4. **Codebase reuse**: DataRSI reuses Blender staging scripts, rendering worker utilities, and evaluation adapters developed within DataEvolver, packaging them into an auditable, reviewer-friendly research repository.
