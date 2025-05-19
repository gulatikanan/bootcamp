class Manager:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, emp):
        self.employees.append(emp)
        emp.manager = self  # create back reference


class Employee:
    def __init__(self, name):
        self.name = name
        self.manager = None  # will be set by Manager
