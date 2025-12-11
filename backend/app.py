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


class Priority(str, Enum):
    Normal = "Normal"
    Emergency = "Emergency"


class PatientIn(BaseModel):
    name: str = Field(..., min_length=3)
    problem: str = Field(..., min_length=3)
    priority: Priority = Priority.Normal


class Patient(BaseModel):
    id: int
    name: str
    problem: str
    priority: Priority
    arrivalTime: str
    status: str


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
