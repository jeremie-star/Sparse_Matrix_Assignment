
class InvalidMatrixFormat(Exception):
    pass


class SparseMatrix:
    def __init__(self, rows=0, cols=0):
        self.rows = rows
        self.cols = cols
        self.data = {}  # key: (row, col), value: int

    @staticmethod
    def from_file(path):
        matrix = SparseMatrix()
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
                if not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
                    raise InvalidMatrixFormat("Missing rows/cols headers")

                matrix.rows = int(lines[0].split('=')[1].strip())
                matrix.cols = int(lines[1].split('=')[1].strip())

                for line in lines[2:]:
                    line = line.strip()
                    if not line:
                        continue
                    if not (line.startswith("(") and line.endswith(")")):
                        raise InvalidMatrixFormat("Invalid line format: " + line)
                    parts = line[1:-1].split(',')
                    if len(parts) != 3:
                        raise InvalidMatrixFormat("Expected 3 elements per entry.")
                    r, c, v = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())
                    matrix.set_element(r, c, v)
        except ValueError:
            raise InvalidMatrixFormat("Input file has wrong format")
        return matrix

    def set_element(self, row, col, value):
        if value != 0:
            self.data[(row, col)] = value

    def get_element(self, row, col):
        return self.data.get((row, col), 0)

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition.")
        result = SparseMatrix(self.rows, self.cols)
        for (r, c), v in self.data.items():
            result.set_element(r, c, v)
        for (r, c), v in other.data.items():
            result.set_element(r, c, result.get_element(r, c) + v)
        return result

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        result = SparseMatrix(self.rows, self.cols)
        for (r, c), v in self.data.items():
            result.set_element(r, c, v)
        for (r, c), v in other.data.items():
            result.set_element(r, c, result.get_element(r, c) - v)
        return result

    def __matmul__(self, other):  # matrix multiplication using @
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions mismatch for multiplication.")
        result = SparseMatrix(self.rows, other.cols)
        for (i, k1), v1 in self.data.items():
            for j in range(other.cols):
                v2 = other.get_element(k1, j)
                if v2 != 0:
                    result.set_element(i, j, result.get_element(i, j) + v1 * v2)
        return result

    def display(self):
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(str(self.get_element(r, c)))
            print(" ".join(row))


# CLI for interaction
def main():
    while True:
        print("\nChoose matrix operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Exit")
        choice = input("Enter choice (1/2/3/4): ")

        if choice == '4':
            print("Goodbye!")
            break

        try:
            A = SparseMatrix.from_file('../../sample_input/matrixfile1.txt')
            B = SparseMatrix.from_file('../../sample_input/matrixfile3.txt')

            # Debugging: Show matrix dimensions
            print(f"\nLoaded matrices:")
            print(f"Matrix A: {A.rows} x {A.cols}")
            print(f"Matrix B: {B.rows} x {B.cols}")

            if choice == '1':
                C = A + B
                print("Result of A + B:")
                C.display()
            elif choice == '2':
                C = A - B
                print("Result of A - B:")
                C.display()
            elif choice == '3':
                C = A @ B
                print("Result of A * B:")
                C.display()
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
