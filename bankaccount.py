#!/usr/bin/python


class BankAccount(object):
    """
    Bank account base class
    """
    type = 'Normal Account'

    def __init__(self, name):
        self.name = name
        self.balance = 0

    def showName(self):
        print self.name

    def showBalance(self):
        print self.balance

    def depositMoney(self, amount):
        self.balance += amount

    def withdrawMoney(self, amount):
        self.balance -= amount


class ExecutiveAccount(BankAccount):
    """
    Executive bank account
    """
    type = 'Executive Account'

    def requestCredit(self, amount):
        self.balance += amount


class SpecialExecutiveAccount(ExecutiveAccount):
    def requestCredit(self, amount):
        self.balance += ExecutiveAccount.requestCredit(self, amount)
        return


# class IterableAccount(BankAccount):



executive = ExecutiveAccount('fan')

print executive.name
print isinstance(executive, ExecutiveAccount)
print isinstance(executive, SpecialExecutiveAccount)
print isinstance(executive, BankAccount)

# executive
