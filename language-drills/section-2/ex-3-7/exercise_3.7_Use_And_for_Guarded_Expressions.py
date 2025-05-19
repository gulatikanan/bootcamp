"""
Use And for Guarded Expressions


"""
def delete_user(user_id):
    print(f"User {user_id} deleted.")

is_admin = True
user_id = 123

# Only delete if admin
is_admin and delete_user(user_id)
