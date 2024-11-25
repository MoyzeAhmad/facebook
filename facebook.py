import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'earntodie1',
    port = 3306,
    database = 'python_db'
)

my_cursor = mydb.cursor()

class Register_User:
        def register(self):
            user_name = input("Enter user name: ")
            password = input("Enter password: ")

            # Check if user already exists
            my_cursor.execute("SELECT user_name FROM users WHERE user_name = %s", (user_name,))
            existing_user = my_cursor.fetchone()  # Fetch one result

            if existing_user:
                print("User already exists!")
            else:
                # Insert new user into the database
                my_cursor.execute(
                    "INSERT INTO users (user_name, password) VALUES (%s, %s)",
                    (user_name, password)
                )
                mydb.commit()  # Save the changes
                print("User registered successfully!")


class Login_User:
    def login(self):
        user_name = input("Enter your username: ")
        password = input("Enter your password: ")

        # Assuming `my_cursor` is the database cursor and the `users` table has columns `user_name` and `password`
        query = "SELECT * FROM users WHERE user_name = %s AND password = %s"
        my_cursor.execute(query, (user_name, password))

        # Fetch the result
        user = my_cursor.fetchone()  # Returns one record or None if no match is found

        if user:
            print("--------------------------------------")
            print(f"   Login successful! Welcome {user_name}")
            print("--------------------------------------")
            while True:
                print("\nOptions:")
                print("1. My Profile")
                print("2. View My Feed")
                print("3. Logout")
                choice = input("Enter your choice: ")
                if choice == "1":
                    while True:
                        print("-------------------")
                        print("Welcome to Profile")
                        print("-------------------")
                        print("1. Update Profile")
                        print("2. Create Post")
                        print("3. View My Posts")
                        print("4. Edit Posts")
                        print("5. Delete Post")
                        print("6. Go Back")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            pass
                        elif choice == "2":
                            pass
                        elif choice == "3":
                            pass
                        elif choice == "4":
                            pass
                        elif choice == "5":
                            pass
                        elif choice == "6":
                            break
                        else:
                            print("Invalid choice")

                elif choice == "2":
                    while True:
                        print("---------------------")
                        print("Welcome to Your Feed")
                        print("---------------------")
                        print("1. View Posts")
                        print("2. Like Posts")
                        print("3. Unlike Posts")
                        print("4. Comment on Posts")
                        print("5. Go Back")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            pass
                        elif choice == "2":
                            pass
                        elif choice == "3":
                            pass
                        elif choice == "4":
                            pass
                        elif choice == "5":
                            break
                        else:
                            print("Invalid choice")

                elif choice == "3":
                    print("Exiting!")
                    break
                else:
                    print("Invalid choice")

        else:
            print("Invalid username or password.")


class Application:
    def __init__(self):
        # Pass dependencies between components
        self.register_user = Register_User()
        self.login_user = Login_User()
    def run(self):
        # Runs the main application through loop
        while True:
            print("\nOptions:")
            print("1. Register User")
            print("2. login User")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.register_user.register()
            elif choice == "2":
                self.login_user.login()
            elif choice == "3":
                print("Exiting!")
                break
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    app = Application()
    app.run()
#PR