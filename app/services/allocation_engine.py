import random
from bson import ObjectId
from config.database import get_db


def shuffle(lst):
    """Fisher-Yates shuffle — returns a new shuffled list."""
    arr = list(lst)
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


async def generate_allocation(semester: int):
    """
    Core allocation algorithm (port of allocationEngine.js):

    1. Fetch all students for the given semester
    2. Shuffle them so students from different departments are mixed
    3. Fetch all classrooms sorted by capacity (descending)
    4. Distribute students across rooms without exceeding capacity
    5. Assign available staff (1 per room; 2 if capacity > 40)
    6. Return the allocation result

    Returns dict with: roomAllocations, totalStudentsAllocated,
                       totalRoomsUsed, totalStudents, unallocatedCount
    """
    db = get_db()

    # 1. Fetch students
    students = []
    async for s in db.students.find({"semester": semester}):
        students.append(s)
    if not students:
        raise ValueError(f"No students found for semester {semester}")

    # 2. Shuffle to mix departments
    shuffled_students = shuffle(students)

    # 3. Fetch classrooms (largest first)
    classrooms = []
    async for c in db.classrooms.find().sort("capacity", -1):
        classrooms.append(c)
    if not classrooms:
        raise ValueError("No classrooms available")

    # 4. Fetch available staff
    available_staff = []
    async for s in db.staffs.find({"isAvailable": True}):
        available_staff.append(s)
    if not available_staff:
        raise ValueError("No staff available for duty")
    shuffled_staff = shuffle(available_staff)

    # 5. Distribute students across rooms
    room_allocations = []
    student_index = 0
    staff_index = 0
    total_students_allocated = 0

    for room in classrooms:
        if student_index >= len(shuffled_students):
            break  # all students allocated

        students_for_room = []
        seats_to_fill = room["capacity"]

        while (
            len(students_for_room) < seats_to_fill
            and student_index < len(shuffled_students)
        ):
            students_for_room.append(shuffled_students[student_index]["_id"])
            student_index += 1

        # 6. Assign staff
        staff_for_room = []
        staff_needed = 2 if room["capacity"] > 40 else 1

        for _ in range(staff_needed):
            if staff_index < len(shuffled_staff):
                staff_for_room.append(shuffled_staff[staff_index]["_id"])
                staff_index += 1

        room_allocations.append(
            {
                "room": room["_id"],
                "roomNumber": room["roomNumber"],
                "block": room["block"],
                "capacity": room["capacity"],
                "staffAssigned": staff_for_room,
                "studentsAssigned": students_for_room,
            }
        )

        total_students_allocated += len(students_for_room)

    unallocated_count = len(shuffled_students) - total_students_allocated

    return {
        "roomAllocations": room_allocations,
        "totalStudentsAllocated": total_students_allocated,
        "totalRoomsUsed": len(room_allocations),
        "totalStudents": len(shuffled_students),
        "unallocatedCount": unallocated_count,
    }
