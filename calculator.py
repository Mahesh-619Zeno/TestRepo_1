def add(x, y): return x + y
def subtract(x, y): return x - y
def multiply(x, y): return x * y
def divide(x, y): return x / y if y != 0 else "Undefined"

print("Select operation: 1.Add 2.Subtract 3.Multiply 4.Divide")
choice = input("Enter choice (1/2/3/4): ")
x = float(input("Enter first number: "))
y = float(input("Enter second number: "))

if choice == '1':
    print(f"Result: {add(x, y)}")
elif choice == '2':
    print(f"Result: {subtract(x, y)}")
elif choice == '3':
    print(f"Result: {multiply(x, y)}")
elif choice == '4':
    print(f"Result: {divide(x, y)}")
else:
    print("Invalid input")
