from app import app
if __name__ == "__main__":
    print("Checking if databse exists.")
    if not os.path.exists('database/db.sqlite'):
        print("-------------------------->>No database.")
        InitializeDB(db)
    app.run()
