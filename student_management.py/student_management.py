import json
import os

class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(data):
        return Student(data["id"], data["name"], data["grade"])


class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.students = [Student.from_dict(item) for item in data]
            except Exception as e:
                print(f"Error loading file: {e}")
                self.students = []

    def save_data(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump([s.to_dict() for s in self.students], file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_student(self, student_id, name, grade):
        if any(s.student_id == student_id for s in self.students):
            print("\n❌ Error: Student ID already exists!")
            return False
        
        new_student = Student(student_id, name, grade)
        self.students.append(new_student)
        self.save_data()
        print("\n✅ Student added successfully!")
        return True

    def list_students(self):
        if not self.students:
            print("\n⚠️ No student records found.")
            return

        print("\n" + "=" * 45)
        print(f"{'ID':<10} | {'Name':<20} | {'Grade':<10}")
        print("=" * 45)
        for s in self.students:
            print(f"{s.student_id:<10} | {s.name:<20} | {s.grade:<10}")
        print("=" * 45)

    def update_student(self, student_id, new_name=None, new_grade=None):
        for s in self.students:
            if s.student_id == student_id:
                if new_name:
                    s.name = new_name
                if new_grade:
                    s.grade = new_grade
                self.save_data()
                print("\n✅ Student details updated!")
                return
        print("\n❌ Student ID not found.")

    def delete_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                self.students.remove(s)
                self.save_data()
                print("\n✅ Student removed successfully!")
                return
        print("\n❌ Student ID not found.")


def main():
    manager = StudentManager()

    while True:
        print("\n--- STUDENT MANAGEMENT SYSTEM ---")
        print("1. Add Student")
        print("2. List Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ").strip()

        if choice == '1':
            sid = input("Enter Student ID: ").strip()
            name = input("Enter Name: ").strip()
            grade = input("Enter Grade: ").strip()
            if sid and name and grade:
                manager.add_student(sid, name, grade)
            else:
                print("❌ Input fields cannot be empty.")

        elif choice == '2':
            manager.list_students()

        elif choice == '3':
            sid = input("Enter Student ID to update: ").strip()
            name = input("Enter New Name (leave blank to keep current): ").strip()
            grade = input("Enter New Grade (leave blank to keep current): ").strip()
            manager.update_student(sid, name if name else None, grade if grade else None)

        elif choice == '4':
            sid = input("Enter Student ID to delete: ").strip()
            manager.delete_student(sid)

        elif choice == '5':
            print("Exiting application...")
            break
        else:
            print("❌ Invalid option! Please try again.")

if __name__ == "__main__":
    main()