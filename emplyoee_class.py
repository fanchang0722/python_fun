#!/usr/bin/python


class Employee(object):
    """common base class for all employee"""
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def display_count(self):
        print "total employee %d" % Employee.empCount

    def display_employee(self):
        print "Name :", self.name, ", Salary :", self.salary

"This would create first object of Employee class"
emp1 = Employee("Zara", 2000)
"This would create second object of Employee class"
emp2 = Employee("Manni", 5000)
emp1.display_employee()
emp2.display_employee()
print "Total Employee %d" % Employee.empCount
print hasattr(emp1, 'name')
emp1.age = 7
emp1.age = 8
print getattr(emp1, 'age')
print Employee.__doc__
print Employee.__name__

