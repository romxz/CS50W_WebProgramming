import os
import dbConnect

db = dbConnect.getDatabase()

def main():
    # Check table users exist, if not create it
    touch_users()

def touch_users():
    with open('usersExist.sql') as f:
        users_exist = db.execute(f.read()).fetchall()
    for user in users_exist:
        if not user[0]: 
            with open('createUsers.sql') as g:
                sqlFile = g.read()
                print("Creating users table")
                db.execute(sqlFile)
                db.commit()
            return
        else:
            print('Table users already exists')
            return
    raise Exception('Touch table users error')


if __name__ == "__main__":
    main()
