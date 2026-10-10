import sqlite3
from contextlib import asynccontextmanager
from datetime import date
from typing import Optional
from fastapi import FastAPI, HTTPException
from database import get_conn, init_db
from schemas import StudentCreate, StudentUpdate, StudentOut

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Students CRUD API", lifespan=lifespan)

def fetch_or_404(conn, student_id: int):
    row = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    if row is None:
        raise HTTPException(404, f"Student {student_id} not found")
    return row

@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(s: StudentCreate):
    data = s.model_dump(mode="json")
    cols = ", ".join(data)
    marks = ", ".join("?" for _ in data)
    try:
        with get_conn() as conn:
            cur = conn.execute(
                f"INSERT INTO students ({cols}) VALUES ({marks})", list(data.values()))
            row = fetch_or_404(conn, cur.lastrowid)
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Email already exists")
    return dict(row)

@app.get("/students", response_model=list[StudentOut])
def list_students(name: Optional[str] = None, course: Optional[str] = None,
                  born_after: Optional[date] = None):
    sql, params = "SELECT * FROM students WHERE 1=1", []
    if name:
        sql += " AND name LIKE ?"; params.append(f"%{name}%")
    if course:
        sql += " AND course = ?"; params.append(course)
    if born_after:
        sql += " AND date_of_birth > ?"; params.append(born_after.isoformat())
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int):
    with get_conn() as conn:
        return dict(fetch_or_404(conn, student_id))

@app.patch("/students/{student_id}", response_model=StudentOut)
def update_student(student_id: int, s: StudentUpdate):
    data = s.model_dump(mode="json", exclude_unset=True)
    if not data:
        raise HTTPException(400, "No fields to update")
    sets = ", ".join(f"{k}=?" for k in data)
    try:
        with get_conn() as conn:
            fetch_or_404(conn, student_id)
            conn.execute(f"UPDATE students SET {sets} WHERE id=?",
                         [*data.values(), student_id])
            return dict(fetch_or_404(conn, student_id))
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Email already exists")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_conn() as conn:
        fetch_or_404(conn, student_id)
        conn.execute("DELETE FROM students WHERE id=?", (student_id,))
    return {"message": f"Student {student_id} deleted"}