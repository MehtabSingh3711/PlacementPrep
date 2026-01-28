class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

class StudentList:
    def __init__(self):
        self.students = []

    def insert_student(self, student_id, name, grade):
        new_student = Student(student_id, name, grade)
        self.students.insert(0, new_student)
        print(f"Student {name} inserted successfully.")

    def insert_at_end(self, student_id, name, grade):
        new_student = Student(student_id, name, grade)
        self.students.append(new_student)
        print(f"Student {name} inserted successfully.")

    def delete_student(self, student_id):
        if not self.students:
            print("Student list is empty.")
            return False

        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                del self.students[i]
                print(f"Student with ID {student_id} deleted successfully.")
                return True
        
        print(f"Student with ID {student_id} not found.")
        return False

    def display_students(self):
        if not self.students:
            print("Student list is empty.")
            return

        print("\n--- Student List ---")
        for i, student in enumerate(self.students, 1):
            print(f"{i}. ID: {student.student_id}, Name: {student.name}, Grade: {student.grade}")
        print("--------------------\n")

    def search_student(self, student_id):
        for i, student in enumerate(self.students, 1):
            if student.student_id == student_id:
                print(f"Student found at position {i}: ID: {student.student_id}, Name: {student.name}, Grade: {student.grade}")
                return student
        print(f"Student with ID {student_id} not found.")
        return None

    def get_size(self):
        return len(self.students)

if __name__ == "__main__":
    students = StudentList()

    while True:
        print("\n--- Student Management System ---")
        print("1. Insert Student")
        print("2. Insert Student at End")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. Display Students")
        print("6. Exit")
        
        try:
            choice = input("Enter your choice (1-6): ")
        except EOFError:
            break

        if choice == '1':
            try:
                s_id = int(input("Enter Student ID: "))
                name = input("Enter Name: ")
                grade = input("Enter Grade: ")
                students.insert_student(s_id, name, grade)
            except ValueError:
                print("Invalid input. Student ID must be an integer.")

        elif choice == '2':
            try:
                s_id = int(input("Enter Student ID: "))
                name = input("Enter Name: ")
                grade = input("Enter Grade: ")
                students.insert_at_end(s_id, name, grade)
            except ValueError:
                print("Invalid input. Student ID must be an integer.")

        elif choice == '3':
            try:
                s_id = int(input("Enter Student ID to delete: "))
                students.delete_student(s_id)
            except ValueError:
                print("Invalid input. Student ID must be an integer.")

        elif choice == '4':
            try:
                s_id = int(input("Enter Student ID to search: "))
                students.search_student(s_id)
            except ValueError:
                print("Invalid input. Student ID must be an integer.")

        elif choice == '5':
            students.display_students()

        elif choice == '6':
            print("Exiting Student Management System.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")