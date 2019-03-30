def say(param):
    pass


say("hi")


def awesome():
    pass


class Person(object):
    def __init__(self, name, height):
        """
        Person class
        """
        self.height = height
        self.name = name

    @awesome()
    def dance(self):
        return "dancing"


person = Person(name='fan chang', height='6ft7in')
print person.name
print person.height
print person.dance()
