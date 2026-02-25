"""
Seed script — populates the exam_allocation database with sample data.

Usage:
    python -m seed.seed_data
"""

import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


# ── Sample Staff Data ────────────────────────────────────────
staff_data = [
    {"name": "Dr. Anil Kumar", "department": "CSE", "designation": "Professor", "isAvailable": True},
    {"name": "Prof. Sneha Rao", "department": "CSE", "designation": "Asst. Professor", "isAvailable": True},
    {"name": "Dr. Rajesh Patil", "department": "ECE", "designation": "Professor", "isAvailable": True},
    {"name": "Prof. Meena Sharma", "department": "ECE", "designation": "Asst. Professor", "isAvailable": True},
    {"name": "Dr. Vikram Desai", "department": "MECH", "designation": "Professor", "isAvailable": True},
    {"name": "Prof. Priya Joshi", "department": "MECH", "designation": "Asst. Professor", "isAvailable": True},
    {"name": "Dr. Suresh Nair", "department": "CIVIL", "designation": "Professor", "isAvailable": True},
    {"name": "Prof. Kavita Iyer", "department": "CIVIL", "designation": "Asst. Professor", "isAvailable": True},
    {"name": "Dr. Ramesh Gupta", "department": "CSE", "designation": "HOD", "isAvailable": True},
    {"name": "Prof. Anita Kulkarni", "department": "ECE", "designation": "Asst. Professor", "isAvailable": True},
]

# ── Sample Classroom Data ────────────────────────────────────
classroom_data = [
    {"roomNumber": "A-101", "block": "BB", "capacity": 30},
    {"roomNumber": "A-102", "block": "BB", "capacity": 40},
    {"roomNumber": "A-103", "block": "BB", "capacity": 50},
    {"roomNumber": "B-201", "block": "IS", "capacity": 35},
    {"roomNumber": "B-202", "block": "IS", "capacity": 45},
    {"roomNumber": "B-203", "block": "IS", "capacity": 30},
    {"roomNumber": "C-301", "block": "EC", "capacity": 60},
    {"roomNumber": "C-302", "block": "EC", "capacity": 40},
]

# ── Student generation ───────────────────────────────────────
DEPARTMENTS = ["CSE", "ISE", "AIML", "ECE"]
DEPT_CODES = {"CSE": "CS", "ISE": "IS", "AIML": "AI", "ECE": "EC"}


def generate_students():
    """Generate sample students with 10-digit USNs."""
    students = []
    counter = 1
    for dept in DEPARTMENTS:
        dept_code = DEPT_CODES[dept]
        for sem in range(1, 7):  # semesters 1-6
            for i in range(1, 16):  # 15 students per dept per semester
                # Format: 1MS26CS001  (college-year-dept-number)
                usn = f"1DS21{dept_code}{str(counter).zfill(3)}0"
                students.append(
                    {
                        "usn": usn,
                        "name": f"Student {dept}-{sem}-{i}",
                        "semester": sem,
                        "department": dept,
                    }
                )
                counter += 1
    return students


# ── Sample Exam Data ─────────────────────────────────────────
exam_data = [
    {"examName": "CIA-1 Feb 2026", "date": datetime(2026, 2, 28), "semester": 3},
    {"examName": "CIA-1 Feb 2026", "date": datetime(2026, 2, 28), "semester": 5},
]


async def seed_database():
    """Seed the MongoDB database with sample data."""
    client = AsyncIOMotorClient(MONGO_URI)
    db_name = MONGO_URI.rsplit("/", 1)[-1].split("?")[0] or "exam_allocation"
    db = client[db_name]

    print("MongoDB connected for seeding...")

    # Clear existing data
    await db.staffs.delete_many({})
    await db.classrooms.delete_many({})
    await db.students.delete_many({})
    await db.ciaexams.delete_many({})
    await db.allocations.delete_many({})
    print("Cleared existing data.")

    now = datetime.utcnow()

    # Insert staff
    staff_docs = [{**s, "createdAt": now, "updatedAt": now} for s in staff_data]
    staff_result = await db.staffs.insert_many(staff_docs)
    print(f"Inserted {len(staff_result.inserted_ids)} staff members.")

    # Insert classrooms
    classroom_docs = [{**c, "createdAt": now, "updatedAt": now} for c in classroom_data]
    classroom_result = await db.classrooms.insert_many(classroom_docs)
    print(f"Inserted {len(classroom_result.inserted_ids)} classrooms.")

    # Insert students
    student_data = generate_students()
    student_docs = [{**s, "createdAt": now, "updatedAt": now} for s in student_data]
    student_result = await db.students.insert_many(student_docs)
    print(f"Inserted {len(student_result.inserted_ids)} students.")

    # Insert exams
    exam_docs = [{**e, "createdAt": now, "updatedAt": now} for e in exam_data]
    exam_result = await db.ciaexams.insert_many(exam_docs)
    print(f"Inserted {len(exam_result.inserted_ids)} exams.")

    print(f"\n✅ Database seeded successfully!")
    print(f"   Staff:      {len(staff_result.inserted_ids)}")
    print(f"   Classrooms: {len(classroom_result.inserted_ids)}")
    print(f"   Students:   {len(student_result.inserted_ids)}")
    print(f"   Exams:      {len(exam_result.inserted_ids)}")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
