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
        global user_name
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
                            self.Update_Profile()
                        elif choice == "2":
                            self.Create_Post()
                        elif choice == "3":
                            self.View_Posts()
                        elif choice == "4":
                            self.Edit_Posts()
                        elif choice == "5":
                            self.Delete_Post()
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
                            self.View_All_Posts()
                        elif choice == "2":
                            self.Like_Post()
                        elif choice == "3":
                            self.Unlike_Post()
                        elif choice == "4":
                            self.Comment_On_Post()
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

    def Update_Profile(self):
        name = user_name
        query = "SELECT update_profile.bio FROM update_profile WHERE name = %s"
        my_cursor.execute(query, (name,))
        user = my_cursor.fetchone()
        if user:
            print(f"Current Bio = {user}")
            bio = input("Enter New Bio = ")
            my_cursor.execute("INSERT INTO update_profile (name,bio) VALUES (%s, %s)",(name, bio))

            mydb.commit()
            print("Bio updated successfully successfully!")
        else:
            print(f"No Bio found for {name}")
            bio = input("Enter New Bio = ")
            my_cursor.execute("INSERT INTO update_profile (name,bio) VALUES (%s, %s)",(name, bio))

            mydb.commit()
            print("Bio updated successfully successfully!")
    def Create_Post(self):
        name = user_name
        content = input("Enter the Content for the Post: ")
        my_cursor.execute("INSERT INTO posts (name,content) VALUES (%s, %s)",(name, content))

        mydb.commit()
        print("Post Created successfully!")

    def View_Posts(self):
        name = user_name
        query = "SELECT id,content FROM posts WHERE name = %s"

        try:
            # Execute the query to fetch posts of the user
            my_cursor.execute(query, (name,))
            posts = my_cursor.fetchall()

            # Check if there are posts
            if posts:
                for post in posts:
                    post_id = post[0]  # Assuming the first column is the post ID
                    content = post[1]  # Assuming the second column is the post content
                    print(f"Post: {content}")

                    # Fetch the number of likes for this post
                    like_query = "SELECT COUNT(*) FROM likes WHERE post_id = %s"
                    my_cursor.execute(like_query, (post_id,))
                    likes_count = my_cursor.fetchone()[0]  # Get the count of likes
                    print(f"Likes: {likes_count}")

                    # Fetch comments for this post
                    comment_query = "SELECT name, content FROM comments WHERE post_id = %s"
                    my_cursor.execute(comment_query, (post_id,))
                    comments = my_cursor.fetchall()

                    # Display comments
                    if comments:
                        print("Comments:")
                        for idx, comment in enumerate(comments, start=1):
                            print(f"{idx}. {comment[1]} (by {comment[0]})")
                    else:
                        print("No comments yet.")
                    print("\n")  # Add a line break between posts
            else:
                print(f"No Post Yet by {name}")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def Edit_Posts(self):
        post_id = int(input("Enter the Post ID you want to edit: "))
        new_content = input("Enter the new content for the post: ")

        # Update query
        query = "UPDATE posts SET content = %s WHERE id = %s"

        try:
            # Execute the query
            my_cursor.execute(query, (new_content, post_id))

            mydb.commit()

            if my_cursor.rowcount > 0:
                print(f"Post with ID {post_id} has been updated successfully.")
            else:
                print(f"No post found with ID {post_id}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    def Delete_Post(self):
        post_id = int(input("Enter the Post id: "))
        query = "DELETE FROM posts WHERE id = %s"
        my_cursor.execute(query, (post_id,))

        mydb.commit()

        if my_cursor.rowcount > 0:
            print(f"Post with ID {post_id} has been deleted successfully.")
        else:
            print(f"No post found with ID {post_id}.")

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

    def Like_Post(self):
        name = user_name
        try:
            post_id = int(input("Enter the Post ID you want to like: "))

            query = "INSERT INTO likes (name, post_id) VALUES (%s, %s)"
            my_cursor.execute(query, (name, post_id))

            mydb.commit()

            print(f"Post with ID {post_id} has been liked successfully!")
        except mysql.connector.IntegrityError as err:
            if "Duplicate entry" in str(err):
                print(f"You have already liked the post with ID {post_id}.")
            else:
                print(f"Error: {err}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    def Unlike_Post(self):
        name = user_name
        try:
            post_id = int(input("Enter the Post ID you want to unlike: "))

            query = "DELETE FROM likes WHERE name = %s AND post_id = %s"
            my_cursor.execute(query, (name, post_id))
            mydb.commit()

            if my_cursor.rowcount > 0:
                print(f"You have successfully unliked the post with ID {post_id}.")
            else:
                print(f"You have not liked the post with ID {post_id}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    def Comment_On_Post(self):
        name = user_name  # Get the current logged-in username
        try:
            # Ask the user for the post ID and the comment content
            post_id = int(input("Enter the Post ID you want to comment on: "))
            content = input("Enter your comment: ")

            # Insert the comment into the comments table
            query = "INSERT INTO comments (post_id, name, content) VALUES (%s, %s, %s)"
            my_cursor.execute(query, (post_id, name, content))
            mydb.commit()  # Save changes

            print(f"Your comment has been added to post ID {post_id}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")


class Application:
    def __init__(self):
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