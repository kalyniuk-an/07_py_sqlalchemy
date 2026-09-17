import random
from datetime import date, timedelta

from faker import Faker

from database import SessionLocal
from models import Group, Teacher, Student, Subject, Grade


fake = Faker("uk_UA")


def seed_database():
    session = SessionLocal()

    try:
        groups = [
            Group(name="Group 1"),
            Group(name="Group 2"),
            Group(name="Group 3"),
        ]

        session.add_all(groups)
        session.flush()

        teachers = []

        for _ in range(4):
            teacher = Teacher(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            teachers.append(teacher)

        session.add_all(teachers)
        session.flush()

        subject_names = [
            "Python",
            "SQL",
            "JavaScript",
            "HTML and CSS",
            "React",
            "Algorithms",
        ]

        subjects = []

        for name in subject_names:
            subject = Subject(
                name=name,
                teacher=random.choice(teachers)
            )
            subjects.append(subject)

        session.add_all(subjects)
        session.flush()

        students = []

        for _ in range(40):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                group=random.choice(groups)
            )
            students.append(student)

        session.add_all(students)
        session.flush()

        grades = []

        start_date = date.today()-timedelta(days=365)

        for student in students:
            number_of_grades = random.randint(5,20)

            for _ in range(number_of_grades):
                grade = Grade(
                    grade=random.randint(1, 12),
                    grade_date=fake.date_between(
                        start_date=start_date,
                        end_date=date.today()
                    ),
                    student=student,
                    subject=random.choice(subjects)
                )

                grades.append(grade)

        session.add_all(grades)

        session.commit()

        print("Database seeded successfully!")
        print(f"Groups: {len(groups)}")
        print(f"Teachers: {len(teachers)}")
        print(f"Subjects: {len(subjects)}")
        print(f"Students: {len(students)}")
        print(f"Grades: {len(grades)}")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()