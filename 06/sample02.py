from pprint import pprint


class Base(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return "{}, name={}, age={}".format(self, self.name, self.age)


class Human(Base):
    def __init__(self, name, age, job):
        super().__init__(name, age)
        # self.job = job


if __name__ == "__main__":
    print("yes")
    taro = Human('taro', 10, 'student')
    pprint(vars(taro))
