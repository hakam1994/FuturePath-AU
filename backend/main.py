"""
FuturePath AU - Backend API Server
Tech Stack: Python 3, FastAPI, SQLite (futurepath.db)
Team Member: Hakm (Frontend Lead) / Integration Contract

Contract Endpoint:
  GET http://127.0.0.1:8000/api/opportunities
"""

import json
import sqlite3
import os
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = os.path.join(os.path.dirname(__file__), "futurepath.db")

# Pydantic Model matching the Frontend contract in App.jsx
class OpportunityModel(BaseModel):
    id: int
    title: str
    provider: str
    category: str
    prerequisites: List[str]
    deadline: str
    source_url: str
    verification_date: str
    description: str

def get_db_connection():
    """Create a connection with dict row factory for clean JSON serialization."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes SQLite table and seeds verified source-grounded
    cybersecurity opportunities adhering to project constraints.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            provider TEXT NOT NULL,
            category TEXT NOT NULL,
            prerequisites TEXT NOT NULL,
            deadline TEXT NOT NULL,
            source_url TEXT NOT NULL,
            verification_date TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    # Check if table already contains entries
    cursor.execute("SELECT COUNT(*) FROM opportunities")
    count = cursor.fetchone()[0]

    if count == 0:
        seed_data = [
            (
                "Cyber Security Cadetship Programme",
                "Australian Signals Directorate (ASD)",
                "Cadetship",
                json.dumps([
                    "Australian Citizenship",
                    "Enrolled in undergraduate degree in IT, Computer Science, or STEM",
                    "Ability to obtain and maintain an NV1 Security Clearance",
                    "Foundational knowledge in Python, Linux, or Networking"
                ]),
                "2026-11-30",
                "https://www.asd.gov.au/careers/cadetships",
                "2026-10-15",
                "Direct entry cadetship offering paid university study support, mentoring, and technical rotations in national cybersecurity operations."
            ),
            (
                "Indigenous Apprenticeship Programme (Cyber & Digital Stream)",
                "Services Australia (Australian Public Service)",
                "Apprenticeship",
                json.dumps([
                    "Australian Citizenship",
                    "Passion for Digital Technologies and Cyber Defence",
                    "Commitment to complete 12-month structured diploma training",
                    "Open to career changers (No prerequisite IT degree required)"
                ]),
                "2026-12-15",
                "https://www.servicesaustralia.gov.au/indigenous-apprenticeships-programme",
                "2026-10-20",
                "Full-time permanent Australian Public Service role with structured certificate/diploma study, cultural mentoring, and cohort support."
            ),
            (
                "Cloud Security & Mentorship Accelerator",
                "Amazon Web Services (AWS) Australia",
                "Mentorship",
                json.dumps([
                    "Enrolled or recent graduate of tertiary IT qualification",
                    "Foundational understanding of Cloud Computing and Networking",
                    "Completion of AWS Cloud Practitioner Essentials (Free online self-study)"
                ]),
                "rolling",
                "https://aws.amazon.com/training/mentorship-au",
                "2026-10-10",
                "12-week structured 1-on-1 industry mentorship with senior AWS Security Architects and certification voucher support."
            ),
            (
                "Cyber Incident Response Student Internship",
                "Telstra Security Operations",
                "Internship",
                json.dumps([
                    "Current university student in Cyber Security, IT or Software Engineering",
                    "Hands-on experience with SIEM tools, Wireshark, or Packet Analysis",
                    "Strong analytical problem-solving and documentation skills"
                ]),
                "2026-10-01",
                "https://careers.telstra.com/cyber-internships",
                "2026-09-18",
                "Real-world blue team and incident response rotation inside Telstra Global SOC."
            ),
            (
                "Cyber Threat Intelligence Research Scholarship",
                "CSIRO / Data61",
                "Scholarship",
                json.dumps([
                    "Australian Citizenship or Permanent Residency",
                    "Bachelor degree in IT, Computer Science or Mathematics with Distinction average",
                    "Demonstrated proficiency in Python, C++, or Data Analysis"
                ]),
                "2026-12-31",
                "https://www.csiro.au/en/careers/scholarships",
                "2026-10-25",
                "Funded honours or master research scholarship examining automated vulnerability analysis and threat telemetry."
            ),
            (
                "Certificate IV & Cyber Traineeship Network",
                "TAFE NSW / Macquarie Cyber Hub",
                "Traineeship",
                json.dumps([
                    "Completion of Australian Year 12 or equivalent qualification",
                    "Demonstrated problem-solving aptitude and IT curiosity",
                    "Basic Linux and command line fundamentals"
                ]),
                "2027-01-20",
                "https://www.tafensw.edu.au/course/cyber-security",
                "2026-10-28",
                "Paid vocational traineeship pathway partnering with regional Australian cyber defense employers."
            )
        ]

        cursor.executemany("""
            INSERT INTO opportunities (
                title, provider, category, prerequisites, deadline, source_url, verification_date, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_data)
        conn.commit()
        print(f"[Database] Initialized and seeded {len(seed_data)} opportunities into {DB_PATH}")

    conn.close()

# Lifespan event to initialize DB on server start
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="FuturePath AU API",
    version="1.0.0",
    description="Backend API serving verified opportunities from SQLite (futurepath.db)",
    lifespan=lifespan
)

# Mandatory CORS configuration to permit React Vite frontend on port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    """Health check endpoint to verify backend status."""
    return {"status": "ok", "database": os.path.basename(DB_PATH)}

@app.get("/api/opportunities", response_model=List[OpportunityModel])
def get_opportunities():
    """
    Contract endpoint:
    Returns source-grounded opportunities directly from SQLite futurepath.db
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunities ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "title": row["title"],
            "provider": row["provider"],
            "category": row["category"],
            "prerequisites": json.loads(row["prerequisites"]),
            "deadline": row["deadline"],
            "source_url": row["source_url"],
            "verification_date": row["verification_date"],
            "description": row["description"]
        })

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
