# # print("hi")
# print(__name__)


# def greet():
#     print("hi")


# def add(a, b):
#     return a+b


# greet()
# print(add(2, 3))

# # if __name__ == "__main__":
# #     greet()
# #     print(add(2, 3))


class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"""
          name is {self.name}
          age is {self.age}
       """


# abc = Employee("sai", 23)
print(Employee("sai", 23))
# print(abc.name)
# print(abc.age)
