# 🎓 CIA Test Duty Allocation — Backend API

Automated **CIA (Continuous Internal Assessment)** test seating and staff duty allocation system built with **FastAPI** and **MongoDB**.

The system takes a list of students, classrooms, and available staff — then automatically generates a seating arrangement that mixes departments and assigns invigilators to each room.

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| Database | [MongoDB Atlas](https://www.mongodb.com/atlas) |
| Async Driver | [Motor](https://motor.readthedocs.io/) |
| Validation | [Pydantic v2](https://docs.pydantic.dev/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |

---

## 📁 Project Structure

```
Exam_Allocation/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config/
│   │   └── database.py          # MongoDB connection & indexes
│   ├── models/
│   │   ├── student.py           # Student schemas
│   │   ├── staff.py             # Staff schemas
│   │   ├── exam.py              # Exam schemas
│   │   ├── classroom.py         # Classroom schemas
│   │   └── allocation.py        # Allocation response schema
│   ├── routes/
│   │   ├── students.py          # /api/students endpoints
│   │   ├── staff.py             # /api/staff endpoints
│   │   ├── exams.py             # /api/exams endpoints
│   │   ├── classrooms.py        # /api/classrooms endpoints
│   │   └── allocations.py       # /api/allocations endpoints
│   └── services/
│       └── allocation_engine.py # Core allocation algorithm
├── seed/
│   └── seed_data.py             # Seed script for sample data
├── requirements.txt
├── .env
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **MongoDB Atlas** account (or a local MongoDB instance)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Exam_Allocation.git
cd Exam_Allocation
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
PORT=3000
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<db_name>
```

### 5. Seed the database (optional)

Populates the database with sample students, staff, classrooms, and exams:

```bash
cd app
python -m seed.seed_data
```

### 6. Run the server

```bash
cd app
uvicorn main:app --reload
```

The API will be available at **http://127.0.0.1:8000**  
Interactive docs (Swagger UI) at **http://127.0.0.1:8000/docs**

---

## 📡 API Endpoints

### Health Check

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API health check & endpoint listing |

---

### 👨‍🎓 Students — `/api/students`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | List all students (filter by `?semester=` and `?department=`) |
| `GET` | `/usn/{usn}` | Get a student by their USN |
| `GET` | `/{id}` | Get a student by MongoDB ID |
| `POST` | `/` | Create a new student |
| `POST` | `/bulk` | Bulk create students |
| `PUT` | `/{id}` | Update a student |
| `DELETE` | `/{id}` | Delete a student |

**Student fields:** `usn` (unique, 10-char), `name`, `semester` (1–8), `department`

---

### 👨‍🏫 Staff — `/api/staff`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | List all staff |
| `GET` | `/available` | List only available staff |
| `GET` | `/{id}` | Get a staff member by ID |
| `POST` | `/` | Create a staff member |
| `PUT` | `/{id}` | Update a staff member |
| `DELETE` | `/{id}` | Delete a staff member |

**Staff fields:** `name`, `department`, `designation`, `isAvailable`

---

### 🏫 Classrooms — `/api/classrooms`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | List all classrooms |
| `GET` | `/{id}` | Get a classroom by ID |
| `POST` | `/` | Create a classroom |
| `PUT` | `/{id}` | Update a classroom |
| `DELETE` | `/{id}` | Delete a classroom |

**Classroom fields:** `roomNumber`, `block`, `capacity`

---

### 📝 Exams — `/api/exams`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | List all exams (sorted by date, newest first) |
| `GET` | `/{id}` | Get an exam by ID |
| `POST` | `/` | Create an exam |
| `PUT` | `/{id}` | Update an exam |
| `DELETE` | `/{id}` | Delete an exam |

**Exam fields:** `examName`, `date`, `semester` (1–8)

---

### 📋 Allocations — `/api/allocations`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | List all allocations |
| `POST` | `/generate/{exam_id}` | **Generate** a new seating allocation for an exam |
| `GET` | `/exam/{exam_id}` | Get allocation for an exam (fully populated with names) |
| `DELETE` | `/{id}` | Delete an allocation |

---

## 🧠 Allocation Algorithm

The core engine (`services/allocation_engine.py`) works as follows:

```
1. Fetch all students for the exam's semester
2. Shuffle students (Fisher-Yates) to mix departments
3. Fetch all classrooms sorted by capacity (largest first)
4. Fill rooms sequentially without exceeding capacity
5. Assign invigilators:
   └─ 1 staff per room (2 if capacity > 40)
6. Return allocation with summary stats
```

**Output includes:**
- Room-wise student assignments (departments mixed)
- Staff assigned to each room
- Summary: total students, allocated count, unallocated count, rooms used

---

## 📦 Data Models

### Student
```json
{
  "usn": "1DS21CS0010",
  "name": "Student Name",
  "semester": 3,
  "department": "CSE"
}
```

### Staff
```json
{
  "name": "Dr. Anil Kumar",
  "department": "CSE",
  "designation": "Professor",
  "isAvailable": true
}
```

### Classroom
```json
{
  "roomNumber": "A-101",
  "block": "BB",
  "capacity": 30
}
```

### Exam
```json
{
  "examName": "CIA-1 Feb 2026",
  "date": "2026-02-28T00:00:00",
  "semester": 3
}
```

---

## 📄 License

This project is for educational purposes.
