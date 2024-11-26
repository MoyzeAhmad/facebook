from connection import mydb, my_cursor, mysql
from session import users_name


class Feed:
    def View_Posts(self,user_name):
        name = user_name
        query = "SELECT id, name, content FROM posts ORDER BY created_at DESC LIMIT 5"

        try:
            my_cursor.execute(query)
            posts = my_cursor.fetchall()

            if posts:
                for post in posts:
                    post_id = post[0]
                    user_name = post[1]
                    content = post[2]
                    print(f"Post ID: {post_id}")
                    print(f"User: {user_name}")
                    print(f"Post: {content}")

                    like_query = "SELECT COUNT(*) FROM likes WHERE post_id = %s"
                    my_cursor.execute(like_query, (post_id,))
                    likes_count = my_cursor.fetchone()[0]
                    print(f"Likes: {likes_count}")

                    comment_query = "SELECT name, content FROM comments WHERE post_id = %s"
                    my_cursor.execute(comment_query, (post_id,))
                    comments = my_cursor.fetchall()

                    if comments:
                        print("Comments:")
                        for idx, comment in enumerate(comments, start=1):
                            print(f"{idx}. {comment[1]} (by {comment[0]})")
                    else:
                        print("No comments yet.")
                    print("\n")

                self.Interact_With_Posts()

            else:
                print(f"No posts yet by {name}")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def Interact_With_Posts(self):
        while True:
            print("\nOptions:")
            print("1. Comment on a Post")
            print("2. Like a Post")
            print("3. Unlike a Post")
            print("4. Create a New Post")
            print("5. Return to Feed")
            choice = input("Enter your choice: ")

            if choice == "1":
                post_id = input("Enter the Post ID you want to comment on: ")
                comment_content = input("Enter your comment: ")
                self.Comment_On_Post(post_id, comment_content)

            elif choice == "2":
                post_id = input("Enter the Post ID you want to like: ")
                self.Like_Post(post_id)

            elif choice == "3":
                post_id = input("Enter the Post ID you want to unlike: ")
                self.Unlike_Post(post_id)

            elif choice == "4":
                obj = Post
                obj.Create_Post()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def get_user_posts(self, user_name):
        query = "SELECT id, content FROM posts WHERE name = %s"
        user_posts = []

        try:
            my_cursor.execute(query, (user_name,))
            posts = my_cursor.fetchall()

            # Process posts
            for post in posts:
                post_id = post[0]
                content = post[1]

                # Fetch the number of likes for this post
                like_query = "SELECT COUNT(*) FROM likes WHERE post_id = %s"
                my_cursor.execute(like_query, (post_id,))
                likes_count = my_cursor.fetchone()[0]

                # Fetch comments for this post
                comment_query = "SELECT name, content FROM comments WHERE post_id = %s"
                my_cursor.execute(comment_query, (post_id,))
                comments = my_cursor.fetchall()

                formatted_comments = [{"name": comment[0], "content": comment[1]} for comment in comments]

                user_posts.append({
                    "post_id": post_id,
                    "content": content,
                    "likes": likes_count,
                    "comments": formatted_comments
                })
            return user_posts
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        while True:
            print("\nOptions:")
            print("1. Edit Post")
            print("2. Delete Post")
            print("3. Logout")
            choice = input("Enter your choice: ")
            if choice == '1':
                obj = Post
                obj.Edit_Posts()
            if choice == '2':
                obj = Post
                obj.Delete_Post()
            elif choice == "3":
                print("Exiting!")
                break
            else:
                print("Invalid choice!")

    def Comment_On_Post(self, post_id, comment_content):
        query = "INSERT INTO comments (post_id, name, content) VALUES (%s, %s, %s)"
        try:
            my_cursor.execute(query, (post_id, users_name, comment_content))
            mydb.commit()
            print("Comment added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def Like_Post(self, post_id):
        query = "INSERT INTO likes (post_id, name) VALUES (%s, %s)"
        try:
            # Check if the user has already liked the post
            my_cursor.execute("SELECT * FROM likes WHERE post_id = %s AND name = %s", (post_id, users_name))
            existing_like = my_cursor.fetchone()

            if existing_like:
                print("You have already liked this post.")
            else:
                my_cursor.execute(query, (post_id, users_name))
                mydb.commit()
                print("Post liked successfully!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def Unlike_Post(self, post_id):
        query = "DELETE FROM likes WHERE post_id = %s AND name = %s"
        try:
            my_cursor.execute(query, (post_id, users_name))
            mydb.commit()
            print("Post unliked successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


class Post:
    def Create_Post(self):
        name = users_name
        content = input("Enter the Content for the Post: ")
        my_cursor.execute("INSERT INTO posts (name,content) VALUES (%s, %s)",(name, content))

        mydb.commit()
        print("Post Created successfully!")
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