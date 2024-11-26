from connection import mydb, my_cursor, mysql
from session import users_name

class Profile:
    def Update_Profile(self):
        name = users_name
        query = "SELECT bio FROM update_profile WHERE name = %s"
        my_cursor.execute(query, (name,))
        user = my_cursor.fetchone()

        if user:
            current_bio = user[0]
            print("Note: To keep the current value, press Enter without typing anything.")

            new_name = input(f"Enter new name (current: {name}): ").strip() or name
            new_bio = input(f"Enter new bio (current: {current_bio}): ").strip() or current_bio

            query = "UPDATE update_profile SET name = %s, bio = %s WHERE name = %s"
            my_cursor.execute(query, (new_name, new_bio, name))

            mydb.commit()
            print("Profile updated successfully!")
        else:
            print(f"No profile found for {name}. Creating a new profile.")
            new_bio = input("Enter new bio: ").strip()
            query = "INSERT INTO update_profile (name, bio) VALUES (%s, %s)"
            my_cursor.execute(query, (name, new_bio))

            mydb.commit()
            print("Profile created successfully!")
