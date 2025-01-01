from app import db

def reset_database():
    # Drop all tables
    db.drop_all()
    print("Database dropped!")

    # Recreate all tables
    #db.create_all()
    #print("Database created!")

if __name__ == "__main__":
    reset_database()

