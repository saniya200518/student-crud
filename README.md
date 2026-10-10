# Students CRUD API

A Python backend to manage student records (Create, Read, Update, Delete) using FastAPI and SQLite.

## Prerequisites
- Python 3.10 or newer
- Git

## Installation
```
git clone https://github.com/saniya200518/student-crud.git
cd student-crud
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
(On Mac/Linux, activate with `source venv/bin/activate`.)

## Run
```
uvicorn main:app --reload
```
The database file `students.db` is created automatically on first start.
Open http://127.0.0.1:8000/docs to test the API in the browser.

## Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /students | Create a student |
| GET | /students | List students (filters: `name`, `course`, `born_after`) |
| GET | /students/{student_id} | View one student |
| PATCH | /students/{student_id} | Update details |
| DELETE | /students/{student_id} | Delete a student |

## Example requests
Create:
```
POST /students
{"name":"Asha Rao","date_of_birth":"2006-04-12","email":"asha@example.com","course":"Python"}
```
Update:
```
PATCH /students/1
{"course":"Data Science"}
```
Filter: `GET /students?born_after=2005-01-01`

## Validation and errors
- 422: invalid input (bad email or date, or neither email nor phone given)
- 404: student not found
- 409: email already exists

## Notes
Only dummy data is used. No real student information is stored in this repository.