import pickle
from org import Manager, Employee

# Create manager and employee
manager = Manager("Alice")
emp1 = Employee("Kanan")
emp2 = Employee("Anurag")

manager.add_employee(emp1)
manager.add_employee(emp2)

# Serialize to file
with open("org.pkl", "wb") as f:
    pickle.dump(manager, f)

print("✅ Organization serialized with cyclic references.")
