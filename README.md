# Clinic Patient Queue

---
## Quick Start

### 1. Clone the repository

```powershell
git clone https://github.com/101rror/myClinic.git
cd myClinic
```

### 1. Start Backend
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate

pip install fastapi uvicorn
uvicorn app.main:app --reload --port 8000
```

### 2. Start Frontend

```powershell
cd frontend
npm install
npm run dev
```