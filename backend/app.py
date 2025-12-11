from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from datetime import datetime, timezone
import json
import os
import sqlite3
from pathlib import Path


ROOT = os.path.dirname(__file__)
DATA_FILE = os.path.join(ROOT, "data.json")
DB_PATH = os.path.join(ROOT, "data.db")


def get_db_connection():
    conn = sqlite3.connect(
        DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            problem TEXT NOT NULL,
            priority TEXT NOT NULL,
            arrivalTime TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    conn.commit()

    cur.execute("SELECT COUNT(*) as c FROM patients")
    row = cur.fetchone()
    if row and row["c"] == 0 and os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for p in data:
                cur.execute(
                    "INSERT INTO patients (id, name, problem, priority, arrivalTime, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        p.get("id"),
                        p.get("name"),
                        p.get("problem"),
                        p.get("priority"),
                        p.get("arrivalTime"),
                        p.get("status"),
                    ),
                )
            conn.commit()
        except Exception:
            pass
    conn.close()


init_db()


class Priority(str, Enum):
    Normal = "Normal"
    Emergency = "Emergency"


class PatientIn(BaseModel):
    name: str = Field(..., min_length=1)
    problem: str = Field(..., min_length=1)
    priority: Priority = Priority.Normal


class Patient(BaseModel):
    id: int
    name: str
    problem: str
    priority: Priority
    arrivalTime: str
    status: str


def _row_to_patient(r: sqlite3.Row) -> dict:
    return {
        "id": r["id"],
        "name": r["name"],
        "problem": r["problem"],
        "priority": r["priority"],
        "arrivalTime": r["arrivalTime"],
        "status": r["status"],
    }


app = FastAPI(title="Clinic Patient Queue")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
