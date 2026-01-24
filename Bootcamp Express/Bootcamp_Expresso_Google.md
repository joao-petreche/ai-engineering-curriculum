# Google Express Bootcamp: Preparation for Scientific AI Engineering

**Author:** Scientific AI Engineering (Building Energy Modeling & Vertex AI)
**Focus:** Technical Onboarding and Phase 0 Infrastructure
**Date:** January 2026

---

## 1. Overview and Objective

This document consolidates the infrastructure requirements and the technical leveling plan ("Express Bootcamp") necessary to initiate the **Scientific AI Engineering** curriculum. The objective is to ensure that the researcher possesses the environment (hardware/software) and competencies (Python/Cloud) to support intensive workloads involving **EnergyPlus** and **Google Cloud Vertex AI**.

Phase 0 is not merely bureaucracy; it is an **engineering filter**. Failure to configure this environment indicates technical blockers that will prevent the execution of complex simulations and ML pipelines in the future.

---

## 2. Infrastructure Audit (Hard Constraints)

Below are the non-negotiable requirements. Failure to meet any of these items will result in incompatibility with the course's automation scripts and Docker containers.

### 2.1 Hardware and Operating System
*   **Operating System:** Windows 10 or 11 (64-bit).
    *   *Technical Note:* The curriculum utilizes PowerShell scripts (`.ps1`) for local orchestration. Linux/Mac users assume the responsibility of porting scripts.
*   **Processor (CPU):** Minimum 4 physical cores. (Recommended: 8+ cores for EnergyPlus simulation parallelization).
*   **Memory (RAM):**
    *   **Minimum:** 8 GB (Viable, but limiting).
    *   **Recommended:** 16 GB+ (Necessary to run VS Code + EnergyPlus + Docker simultaneously).
*   **Storage:** Minimum **20 GB** free (SSD mandatory for efficient dataset I/O).
*   **Permissions:** Local **Administrator** access is mandatory for environment variable manipulation (PATH).

### 2.2 Software Stack (Strict Versions)
Scientific reproducibility requires rigorous version control. Do not update beyond these versions without prior validation.

*   **Python:** **3.10.x** (Recommended: 3.10.11).
    *   *Warning:* Versions 3.11/3.12 still present instabilities with certain *Scientific ML* libraries and legacy bindings.
*   **EnergyPlus:** **24.1.0**.
    *   *Integration:* We will use the native Python API (`pyenergyplus`) preferentially over CLI subprocesses.
*   **IDE:** Visual Studio Code (Microsoft).
    *   *Essential Extensions:* Python, Jupyter, **GitHub Copilot**, **Google Cloud Code**, Ruff/Black.

### 2.3 Accounts and Access
We utilize a hybrid model to maximize free resources (*Free Tier*).

*   **Institutional Identity (USP/FAPESP):**
    *   Required for the **GitHub Student Developer Pack** (Free Copilot) and access to **Coursera for USP**.
*   **Cloud Identity (Personal Google Account):**
    *   Use a personal `@gmail.com` email for **Google Cloud Platform (GCP)**.
    *   *Reason:* Institutional accounts (G-Suite/Workspace) often have restrictive IAM policies that block Vertex AI.
    *   **Financial:** Credit card required to activate the *Free Trial* ($300 USD), but we will configure *Budget Alerts* for zero cost.

---

## 3. Leveling Plan: The "Express Bootcamp" (Google Stack)

We have identified common gaps in Python, Git, and Terminal skills. To bridge them in **1 week**, we will utilize official resources from the Google ecosystem and partners.

### 3.1 Python for Data Science (Kaggle)
*Google platform focused on applied Data Science.*

*   **Resource:** [Kaggle Learn](https://www.kaggle.com/learn)
*   **Methodology:** Practical micro-courses (focused on "doing" rather than just "watching").
*   **Mandatory Courses:**
    1.  **Python:** Focus on syntax, list/dictionary manipulation, and functions.
    2.  **Pandas:** Directly covers *Exercise 0.2.E* (ETL of CSV/JSON files).

### 3.2 Version Control and Automation (Coursera/Google)
*Gold standard for code operations.*

*   **Resource:** Google IT Automation with Python (Coursera).
*   **Access:** Via **Coursera for USP** (free for students).
*   **Focus Module:** "Introduction to Git and GitHub".
    *   Teaches from `git init` to *Pull Requests*.
    *   Covers basic terminal automation (Bash/Linux skills).

### 3.3 Terminal and Cloud Fluency (Google Cloud Skills Boost)
*To lose the fear of the "black screen".*

*   **Resource:** [Google Cloud Skills Boost](https://www.cloudskillsboost.google/)
*   **Recommended Labs:** "Linux Fundamentals" or "Cloud Engineering Basics".
*   **Advantage:** Real *sandbox* environment in the browser. No risk of damaging your local machine.

---

## 4. Execution Schedule (1 Week)

If you answered "NO" to any item in the infrastructure or competency audit, follow this schedule rigorously before Month 1.

| Days | Focus | Critical Tasks | Platform |
| :--- | :--- | :--- | :--- |
| **1-2** | **Python Core** | Complete *Python* and *Pandas* courses. Ensure understanding of `venv`. | Kaggle Learn |
| **3-4** | **Git & Terminal** | "Intro to Git/GitHub" module. Configure local SSH keys. | Coursera (Google) |
| **5** | **Validation** | Execute **Exercise 0.2.E** (ETL Script) without consulting basic tutorials. | Local (VS Code) |

---

## 5. Next Steps

After completing this bootcamp:
1.  Configure your local environment (`venv`, EnergyPlus 24.1.0).
2.  Clone the curriculum repository.
3.  Execute the environment validation script (if available) or report status in the communication channel.

> **Engineer's Note:** The quality of your infrastructure in Phase 0 dictates the pace of your innovation in Phase 3. Do not skip steps.
