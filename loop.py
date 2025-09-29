# Scenario 4: Using loop variables like i, j, x – acceptable in local loops

def print_numbers():
    for i in range(5):
        print(f"Index: {i}")

def sum_matrix(matrix):
    total = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            total += matrix[i][j]
    return total

print_numbers()
print(sum_matrix([[1, 2], [3, 4]]))
