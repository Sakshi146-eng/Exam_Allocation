import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    """Connect to MongoDB using Motor async driver."""
    global client, db
    client = AsyncIOMotorClient(MONGO_URI)
    # Extract database name from URI, fallback to "exam_allocation"
    db_name = MONGO_URI.rsplit("/", 1)[-1].split("?")[0] or "exam_allocation"
    db = client[db_name]
    # Ping to verify connection
    await client.admin.command("ping")
    print(f"MongoDB Connected: {client.address[0]}:{client.address[1]}")
    # Ensure unique index on student USN
    await db.students.create_index("usn", unique=True, sparse=True)
    print("Indexes ensured.")


async def close_db():
    """Close the MongoDB connection."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")


def get_db():
    """Return the database instance."""
    return db
