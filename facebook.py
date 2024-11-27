from connection import mydb, my_cursor, mysql
from session import users_name
from feed import Post, Feed
from profile import Profile

class Register_User:
        def register(self):
            user_name = input("Enter user name: ")
            password = input("Enter password: ")

            my_cursor.execute("SELECT user_name FROM users WHERE user_name = %s", (user_name,))
            existing_user = my_cursor.fetchone()

            if existing_user:
                print("User already exists!")
            else:
                my_cursor.execute(
                    "INSERT INTO users (user_name, password) VALUES (%s, %s)",
                    (user_name, password)
                )
                mydb.commit()
                print("User registered successfully!")

class Authentication:
    def login(self):
        global users_name
        user_name = input("Enter your username: ")
        password = input("Enter your password: ")

        query = "SELECT * FROM users WHERE user_name = %s AND password = %s"
        my_cursor.execute(query, (user_name, password))

        user = my_cursor.fetchone()

        if user:
            users_name = user_name
            print("--------------------------------------")
            print(f"   Login successful! Welcome {users_name}")
            print("--------------------------------------")
            while True:
                print("\nOptions:")
                print("1. View Feed")
                print("2. Create Post")
                print("3. My Profile")
                print("4. Logout")
                choice = input("Enter your choice: ")
                if choice == "1":
                    print("-------------------")
                    print("Welcome to Feed")
                    print("-------------------")
                    obj = Feed()
                    obj.View_Posts(users_name)

                elif choice == "2":
                    print("---------------------")
                    print("Let's create a Post")
                    print("---------------------")
                    obj = Post()
                    obj.Create_Post(users_name)

                elif choice == "3":
                    print("---------------------")
                    print("Welcome To Your Profile")
                    print("---------------------")
                    obj = Feed()
                    obj.get_user_posts(users_name)

                elif choice == "4":
                    print("Logging out!")
                    break
                else:
                    print("Invalid choice.")
        else:
            print("Invalid username or password.")

    def View_All_Posts(self):
        query = "SELECT id, name, content FROM posts"
        try:
            my_cursor.execute(query)
            posts = my_cursor.fetchall()

            if posts:
                for idx, post in enumerate(posts, start=1):
                    post_id = post[0]
                    post_user_name = post[1]
                    post_content = post[2]

                    like_query = "SELECT COUNT(*) FROM likes WHERE post_id = %s"
                    my_cursor.execute(like_query, (post_id,))
                    like_count = my_cursor.fetchone()[0]
                    comment_query = "SELECT COUNT(*) FROM comments WHERE post_id = %s"
                    my_cursor.execute(comment_query, (post_id,))
                    comment_count = my_cursor.fetchone()[0]
                    print(f"{idx}. {post_user_name}: {post_content} ({like_count} likes, {comment_count} comments)")
            else:
                print("No posts yet.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

class Application:
    def __init__(self):
        self.register_user = Register_User()
        self.login_user = Authentication()
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