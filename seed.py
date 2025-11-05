"""
Database seeding script to create initial admin user.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from sqlalchemy.orm import Session
from configs.database import SessionLocal, engine, Base
from components.users.models import User
from utils.auth import get_password_hash


def seed_admin_user(db: Session):
    """Create admin user if it doesn't exist."""
    admin_email = "admin@example.com"

    # Check if admin user already exists
    existing_user = db.query(User).filter(User.email == admin_email).first()
    if existing_user:
        print(f"✓ Admin user already exists: {admin_email}")
        return existing_user

    # Create admin user
    admin_user = User(
        email=admin_email,
        name="Admin User",
        password=get_password_hash(admin_email),  # Password is same as email
        is_active=True
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    print(f"✓ Admin user created successfully!")
    print(f"  Email: {admin_email}")
    print(f"  Password: {admin_email}")
    print(f"  User ID: {admin_user.id}")

    return admin_user


def main():
    """Main seeding function."""
    print("=" * 50)
    print("Database Seeding Script")
    print("=" * 50)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create database session
    db = SessionLocal()

    try:
        # Seed admin user
        seed_admin_user(db)

        print("\n" + "=" * 50)
        print("Seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

