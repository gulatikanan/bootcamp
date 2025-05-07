"""
Access Control Decorator

Instructions:
Complete the exercise according to the requirements.
"""
def role_required(role):
    def decorator(func):
        def wrapper(user_role, *args, **kwargs):
            if user_role != role:
                print(f"Access denied for role: {user_role}")
                return None
            return func(user_role, *args, **kwargs)
        return wrapper
    return decorator

# Example usage
@role_required("admin")
def delete_user(user_role, user_id):
    print(f"Deleting user {user_id}...")

delete_user("admin", 123)  # Allowed
delete_user("user", 123)   # Denied

