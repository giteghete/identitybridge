# Project IdentityBridge

An API-first, Machine-to-Machine (M2M) Identity Governance and Administration (IGA) engine built to simulate automated lifecycle provisioning and directory synchronization.

## 🛠️ Architecture Overview
Project IdentityBridge serves as a code-driven middleware layer designed to govern down-funnel cloud target applications via RESTful endpoints. The platform enforces automated identity management workflows under the strict security principle of least privilege.

## 🚀 Core JML Lifecycle Modules
The project architecture is decoupled into three primary execution modules to mimic real-world enterprise Joiner-Mover-Leaver (JML) provisioning tracks:

### 1. Joiner Track (`test_run_provision.py`)
* **Behavior:** Handles automatic inbound onboarding flows.
* **Mechanism:** Programmatically constructs target directory account schemas, maps functional organizational departments, handles runtime password parameters, and pushes secure database writes using transactional `HTTP 201 Created` operations.

### 2. Mover Track (`test_run_mover.py`)
* **Behavior:** Orchestrates dynamic role cross-referencing and state detection.
* **Mechanism:** Actively targets active identities, extracts current user profile context, and evaluates changes. It executes a scoped `HTTP 200 OK` PATCH payload *only* when a state delta is identified—protecting downstream API targets from redundant calls and resource throttling.

### 3. Leaver Track (`test_run_deprov.py`)
* **Behavior:** Enforces instant risk mitigation and access revocation.
* **Mechanism:** Leverages dynamic search queries to hunt down internal cloud resource IDs, triggers corporate deprovisioning policies, and updates security flags (`blocked: True`) to isolate and lock stale accounts immediately upon separation.

## ⚙️ Technical Blueprint
* **Language Environment:** Python 3.x
* **Core Library Dependences:** `requests`, `json`
* **Protocol Target:** REST Authentication Layer (OAuth 2.0 Client Credentials Architecture)

---
*Developed as a technical show-and-tell portfolio to demonstrate production-grade API implementation capabilities, idempotent script design, and identity lifecycle optimization.*