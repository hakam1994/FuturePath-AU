# FuturePath AU &mdash; Frontend & Backend Prototype

FuturePath AU is an accessible, student-guided cybersecurity pathway planner designed to empower Australian students and career changers. Built strictly according to the university assessment brief and team workplan for team member **Hakm**, the platform provides transparent prerequisite analysis, verified opportunity navigation, and customizable career roadmaps without algorithmic bias or external framework bloat.

---

### Mandatory Ethical Safeguards

1. **No Autonomous Applications**: The system guides milestone planning; it never automatically submits job or course applications. All submissions remain student-initiated.
2. **No Identity Scoring**: Suitability is strictly evaluated against published entry criteria—never inferred or scored using Indigenous identity.
3. **Deterministic Fact-Grounded Data**: Opportunities, prerequisites, deadlines, and portal URLs are verified facts grounded in an SQLite registry.
4. **Human Oversight**: Students maintain full agency to edit, reorder, delete, and explicitly approve their sequential career pathways.

---

### Implemented Specifications (HAK-01 to HAK-06)

* **[HAK-01] Zero-Bloat React/Vite Architecture**: Built with Vite and lightweight semantic CSS (no Tailwind or extraneous dependencies) achieving fast sub-second bundle times.
* **[HAK-02] Goal & Profile Form**: Captures target cybersecurity specializations, qualifications, and skills via a categorized dropdown selector with interactive, removable tags and client-side validation.
* **[HAK-03] Verified Opportunity Explorer**: Connects via `fetch()` to FastAPI, displaying real-world cadetships, traineeships, apprenticeships, and scholarships with official source links.
* **[HAK-04] Deterministic Prerequisite Audit**: Evaluates profile data against published requirements using three unambiguous badges: **Satisfied** (green), **Unmet** (red), and **Uncertain (Verification Required)** (amber).
* **[HAK-05] Editable Pathway & Student Approval**: Automatically generates actionable sequential milestones with controls to move up/down, edit text, delete steps, and insert custom tasks. Clicking **"Approve Pathway"** locks the plan under a student timestamp.
* **[HAK-06] Deadline States & Resilient UX**: Computes deterministic deadline badges (**Upcoming**, **Passed / Closed**, **Rolling / Unknown**), with loading spinners and a graceful offline fallback banner.

---

### System Architecture

```
React (Vite :5173)  <-- HTTP GET /api/opportunities -->  FastAPI (:8000)  <-- sqlite3 -->  futurepath.db
```

---

### Verification & Compliance

The prototype is verified through automated production builds (`npm run build`), deterministic test cases covering prerequisite evaluation matrices, and CORS-validated endpoint responses. All data structures match the university marking rubric specifications.

---

### Getting Started

#### 1. Launch Backend (Python & SQLite)
```bash
# In project root:
py -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
*API Endpoint*: `http://127.0.0.1:8000/api/opportunities`

#### 2. Launch Frontend (React JS)
```bash
npm install
npm run dev
```
*Frontend Application*: `http://localhost:5173/`
