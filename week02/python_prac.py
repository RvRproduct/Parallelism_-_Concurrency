import random

print("\n --- PASS BY REFERENCE or PASS BY VALUE or PASS BY OBJECT REFERENCE? ---")


def assign_new_value(a):
    print(f"INSIDE FUNCTION: before id = {id(a)}")
    a = "new value"
    print(f"INSIDE FUNCTION: after id = {id(a)}")


my_string = "old value"
assign_new_value(my_string)
print(f"OUTSIDE FUNCTION: after id = {id(my_string)}")


def my_list(a):
    print(f"INSIDE FUNCTION, before adding, id= {id(a)}")
    a[0] = "Nothing"
    print(f"INSIDE FUNCTION, after adding, id = {id(a)}")
    print(f"INSIDE FUNCTION, a = {a}")


b = ["A", "B", "C", "D"]
my_list(b)
print(f"OUTSIDE FUNCTION, b id = {id(b)}")
print(b)


# def overwrite_foo_list(a):
#     print("\n\nIn overwrite function, before adding, id=", id(a))

#     # this assigns the variable "a" a new memory address
#     # but does not change the object that was passed in
#     a = ["E", "F", "G"]

#     print("In overwrite function, before adding, id =")
