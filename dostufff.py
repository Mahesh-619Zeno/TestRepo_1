# Scenario 3: Vague function name 'doStuff' that modifies global state

counter = 0

def doStuff():
    global counter
    counter += 1
    print(f"Counter updated to {counter}")

doStuff()
doStuff()
