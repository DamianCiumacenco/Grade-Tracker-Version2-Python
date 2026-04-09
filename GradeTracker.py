# STUDENT GRADE TRACKER v2.0
# By: Damian Ciumacenco
# Date: Jul 2025 — Updated 2026

import json
import os

class GradeTracker:
    def __init__(self):
        self.students = {}
        self.load_data()

    # ── Add student ──
    def add_student(self, name):
        if name in self.students:
            print(f"  ⚠  Student '{name}' already exists!")
        else:
            self.students[name] = []
            print(f"  ✅ Student '{name}' added!")
            self.save_data()

    # ── Remove student ──
    def remove_student(self, name):
        if name not in self.students:
            print(f"  ⚠  Student '{name}' not found!")
            return
        confirm = input(f"  Are you sure you want to remove '{name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.students[name]
            self.save_data()
            print(f"  ✅ Student '{name}' removed.")
        else:
            print("  Cancelled.")

    # ── Add grade ──
    def add_grade(self, name, grade):
        if name not in self.students:
            print(f"  ⚠  Student '{name}' not found!")
            return
        try:
            grade = float(grade)
            if 0 <= grade <= 100:
                self.students[name].append(grade)
                print(f"  ✅ Added grade {grade} for {name}")
                self.save_data()
            else:
                print("  ⚠  Grade must be between 0 and 100")
        except ValueError:
            print("  ⚠  Please enter a valid number")

    # ── Edit a grade ──
    def edit_grade(self, name):
        if name not in self.students:
            print(f"  ⚠  Student '{name}' not found!"); return
        grades = self.students[name]
        if not grades:
            print(f"  ⚠  No grades to edit for {name}."); return
        print(f"\n  Grades for {name}:")
        for i, g in enumerate(grades):
            print(f"    {i+1}. {g}")
        try:
            idx = int(input("  Enter grade number to edit: ")) - 1
            if idx < 0 or idx >= len(grades):
                print("  ⚠  Invalid selection."); return
            new_grade = float(input("  Enter new grade (0-100): "))
            if 0 <= new_grade <= 100:
                old = grades[idx]
                grades[idx] = new_grade
                self.save_data()
                print(f"  ✅ Updated grade {old} → {new_grade} for {name}")
            else:
                print("  ⚠  Grade must be between 0 and 100.")
        except (ValueError, IndexError):
            print("  ⚠  Invalid input.")

    # ── Remove a grade ──
    def remove_grade(self, name):
        if name not in self.students:
            print(f"  ⚠  Student '{name}' not found!"); return
        grades = self.students[name]
        if not grades:
            print(f"  ⚠  No grades to remove for {name}."); return
        print(f"\n  Grades for {name}:")
        for i, g in enumerate(grades):
            print(f"    {i+1}. {g}")
        try:
            idx = int(input("  Enter grade number to remove: ")) - 1
            if idx < 0 or idx >= len(grades):
                print("  ⚠  Invalid selection."); return
            removed = grades.pop(idx)
            self.save_data()
            print(f"  ✅ Removed grade {removed} from {name}")
        except (ValueError, IndexError):
            print("  ⚠  Invalid input.")

    # ── Calculate average ──
    def calculate_average(self, name):
        if name not in self.students: return None
        grades = self.students[name]
        if not grades: return 0
        total = 0
        for g in grades:
            total += g
        return total / len(grades)

    # ── Letter grade ──
    def get_letter_grade(self, average):
        if average >= 90: return 'A'
        elif average >= 80: return 'B'
        elif average >= 70: return 'C'
        elif average >= 60: return 'D'
        else: return 'F'

    # ── Student summary ──
    def show_student_summary(self, name):
        if name not in self.students:
            print(f"  ⚠  Student '{name}' not found!"); return
        grades = self.students[name]
        print("\n" + "="*52)
        print(f"  STUDENT SUMMARY: {name}")
        print("="*52)
        if not grades:
            print("  No grades recorded yet.")
        else:
            total = 0
            for g in grades: total += g
            avg = total / len(grades)
            letter = self.get_letter_grade(avg)

            highest = grades[0]
            for g in grades:
                if g > highest: highest = g
            lowest = grades[0]
            for g in grades:
                if g < lowest: lowest = g

            print(f"  Grades:        {grades}")
            print(f"  Average:       {avg:.1f}%")
            print(f"  Letter Grade:  {letter}")
            print(f"  Highest:       {highest}")
            print(f"  Lowest:        {lowest}")
            print(f"  Total Grades:  {len(grades)}")
        print("="*52)

    # ── All students ──
    def show_all_students(self):
        if not self.students:
            print("  No students in the system yet."); return
        print("\n" + "="*52)
        print("  ALL STUDENTS")
        print("="*52)
        for name in self.students:
            grades = self.students[name]
            if not grades:
                print(f"  {name}: No grades yet")
            else:
                total = 0
                for g in grades: total += g
                avg = total / len(grades)
                letter = self.get_letter_grade(avg)
                print(f"  {name:<20} {avg:.1f}% ({letter})  —  {len(grades)} grades")
        print("="*52)

    # ── Class statistics ──
    def class_statistics(self):
        if not self.students:
            print("  No students yet."); return
        all_grades = []
        for name in self.students:
            for g in self.students[name]:
                all_grades.append(g)
        if not all_grades:
            print("  No grades recorded yet."); return

        total_sum = 0
        for g in all_grades: total_sum += g
        class_avg = total_sum / len(all_grades)

        highest = all_grades[0]
        for g in all_grades:
            if g > highest: highest = g
        lowest = all_grades[0]
        for g in all_grades:
            if g < lowest: lowest = g

        print("\n" + "="*52)
        print("  CLASS STATISTICS")
        print("="*52)
        print(f"  Total Students:   {len(self.students)}")
        print(f"  Total Grades:     {len(all_grades)}")
        print(f"  Class Average:    {class_avg:.1f}%")
        print(f"  Highest Grade:    {highest}")
        print(f"  Lowest Grade:     {lowest}")

        # Grade distribution
        dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for g in all_grades:
            dist[self.get_letter_grade(g)] += 1
        print("\n  Grade Distribution:")
        for letter, count in dist.items():
            bar = '█' * count
            print(f"    {letter}: {bar} ({count})")

        # Top performer
        best_name, best_avg = None, -1
        for name in self.students:
            avg = self.calculate_average(name)
            if avg > best_avg:
                best_avg = avg
                best_name = name
        if best_name:
            print(f"\n  🏆 Top Performer: {best_name} ({best_avg:.1f}%)")
        print("="*52)

    # ── Export report to text file ──
    def export_report(self):
        filename = "grade_report.txt"
        with open(filename, 'w') as f:
            f.write("STUDENT GRADE REPORT\n")
            f.write("="*52 + "\n\n")
            for name in self.students:
                grades = self.students[name]
                f.write(f"Student: {name}\n")
                if not grades:
                    f.write("  No grades recorded.\n")
                else:
                    total = 0
                    for g in grades: total += g
                    avg = total / len(grades)
                    letter = self.get_letter_grade(avg)
                    f.write(f"  Grades:  {grades}\n")
                    f.write(f"  Average: {avg:.1f}% ({letter})\n")
                f.write("\n")
        print(f"  ✅ Report exported to '{filename}'")

    # ── Delete student ──
    def delete_student(self, name):
        if name in self.students:
            del self.students[name]
            print(f"  ✅ Student '{name}' deleted!")
            self.save_data()
        else:
            print(f"  ⚠  Student '{name}' not found!")

    # ── Save / Load ──
    def save_data(self):
        with open('grades_data.json', 'w') as f:
            json.dump(self.students, f)

    def load_data(self):
        if os.path.exists('grades_data.json'):
            with open('grades_data.json', 'r') as f:
                self.students = json.load(f)
            print(f"  ✅ Data loaded — {len(self.students)} student(s) found.")


def main():
    tracker = GradeTracker()

    print("\n" + "="*52)
    print("       STUDENT GRADE TRACKER  v2.0")
    print("="*52)

    while True:
        print("\n  MAIN MENU:")
        print("  1.  Add Student")
        print("  2.  Remove Student")
        print("  3.  Add Grade")
        print("  4.  Edit Grade")
        print("  5.  Remove a Grade")
        print("  6.  View Student Summary")
        print("  7.  View All Students")
        print("  8.  Class Statistics")
        print("  9.  Export Report to File")
        print("  10. Exit")
        print("  " + "-"*48)

        choice = input("  Enter your choice (1-10): ").strip()

        if choice == '1':
            name = input("  Enter student name: ").strip()
            tracker.add_student(name)
        elif choice == '2':
            name = input("  Enter student name: ").strip()
            tracker.remove_student(name)
        elif choice == '3':
            name = input("  Enter student name: ").strip()
            grade = input("  Enter grade (0-100): ").strip()
            tracker.add_grade(name, grade)
        elif choice == '4':
            name = input("  Enter student name: ").strip()
            tracker.edit_grade(name)
        elif choice == '5':
            name = input("  Enter student name: ").strip()
            tracker.remove_grade(name)
        elif choice == '6':
            name = input("  Enter student name: ").strip()
            tracker.show_student_summary(name)
        elif choice == '7':
            tracker.show_all_students()
        elif choice == '8':
            tracker.class_statistics()
        elif choice == '9':
            tracker.export_report()
        elif choice == '10':
            print("\n  Goodbye! Data saved. 👋")
            print("="*52)
            break
        else:
            print("  ⚠  Invalid choice. Please enter 1-10.")

if __name__ == "__main__":
    main()
