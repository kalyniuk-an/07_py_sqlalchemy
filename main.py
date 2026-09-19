import argparse
from datetime import date

from database import SessionLocal
from models import Teacher, Student, Group, Subject, Grade


def list_records(model):
    session = SessionLocal()

    try:
        records = session.query(model).all()

        for record in records:
            if isinstance(record, Teacher):
                print(
                    record.id,
                    record.first_name,
                    record.last_name
                )
            elif isinstance(record, Student):
                print(
                    record.id,
                    record.first_name,
                    record.last_name,
                    "Gropu:",
                    record.group_id
                )
            elif isinstance(record, Group):
                print(
                    record.id,
                    record.name
                    )
            elif isinstance(record, Subject):
                print(
                    record.id,
                    record.name,
                    "Teacher:",
                    record.teacher_id
                )
            elif isinstance(record, Grade):
                print(
                    record.id,
                    record.grade,
                    record.grade_date,
                    "Student:",
                    record.student_id,
                    "Subject:",
                    record.subject_id
                )

    finally:
        session.close()


def create_group(name):
    session = SessionLocal()

    try:
        group = Group(name=name)

        session.add(group)
        session.commit()

        print(
            f"Group created: {group.id} - {group.name}"
        )

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def create_teacher(name):
    session = SessionLocal()

    try:
        parts = name.split()

        if len(parts) < 2:
            print("Please provide first name and last name.")
            return

        teacher = Teacher(
            first_name=parts[0],
            last_name=parts[1]
        )

        session.add(teacher)
        session.commit()

        print(
            f"Teacher created: {teacher.id} - {teacher.first_name} - {teacher.last_name}"
        )

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def create_student(name, group_id):
    session = SessionLocal()

    try:
        parts = name.split()

        if len(parts) < 2:
            print("Please provide first name and last name.")
            return

        student = Student(
            first_name=parts[0],
            last_name=parts[1],
            group_id=group_id
        )

        session.add(student)
        session.commit()

        print(
            f"Student created: "
            f"{student.id} - "
            f"{student.first_name} "
            f"{student.last_name}, "
            f"Group: {student.group_id}"
        )

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()

def create_subject(name, teacher_id):
    session = SessionLocal()

    try:
        subject = Subject(
            name=name,
            teacher_id=teacher_id
        )

        session.add(subject)
        session.commit()

        print(
            f"Subject created: "
            f"{subject.id} - {subject.name},"
            f"Teacher: {subject.teacher_id}"
        )

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def create_grade(student_id, subject_id, grade_value, grade_date):
    session = SessionLocal()

    try:
        grade = Grade(
            student_id=student_id,
            subject_id=subject_id,
            grade=grade_value,
            grade_date=date.fromisoformat(grade_date)
        )

        session.add(grade)
        session.commit()

        print(
            f"Grade created: "
            f"{grade.id} - "
            f"Grade: {grade.grade}, "
            f"Student: {grade.student_id}, "
            f"Subject: {grade.subject_id}, "
            f"Date: {grade.grade_date}"
        )

    except ValueError:
        session.rollback()
        print("Date must be in YYYY-MM-DD format.")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()

def update_group(group_id, name):
    session = SessionLocal()

    try:
        group = session.query(Group).filter(Group.id == group_id).first()

        if not group:
            print("Group not found.")
            return

        group.name = name

        session.commit()

        print(f"Group updated: {group.id} - {group.name}")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def update_teacher(teacher_id, name):
    session = SessionLocal()

    try:
        teacher = session.query(Teacher).filter(
            Teacher.id == teacher_id
        ).first()

        if not teacher:
            print("Teacher not found.")
            return

        parts = name.split()

        if len(parts) < 2:
            print("Please provide first name and last name.")
            return

        teacher.first_name = parts[0]
        teacher.last_name = parts[1]

        session.commit()

        print(
            f"Teacher updated: "
            f"{teacher.id} - "
            f"{teacher.first_name} "
            f"{teacher.last_name}"
        )

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def update_student(student_id, name, group_id):
    session = SessionLocal()

    try:
        student = session.query(Student).filter(
            Student.id == student_id
        ).first()

        if not student:
            print("Student not found.")
            return

        parts = name.split()

        if len(parts) < 2:
            print("Please provide first name and last name.")
            return

        student.first_name = parts[0]
        student.last_name = parts[1]
        student.group_id = group_id

        session.commit()

        print(
            f"Student updated: "
            f"{student.id} - "
            f"{student.first_name} "
            f"{student.last_name}, "
            f"Group: {student.group_id}"
        )

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()

def update_subject(subject_id, name, teacher_id):
    session = SessionLocal()

    try:
        subject = session.query(Subject).filter(
            Subject.id == subject_id
        ).first()

        if not subject:
            print("Subject not found.")
            return

        subject.name = name
        subject.teacher_id = teacher_id

        session.commit()

        print(
            f"Subject updated: "
            f"{subject.id} - "
            f"{subject.name}, "
            f"Teacher: {subject.teacher_id}"
        )

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def update_grade(grade_id, grade_value, grade_date, student_id, subject_id):
    session = SessionLocal()

    try:
        grade = session.query(Grade).filter(
            Grade.id == grade_id
        ).first()

        if not grade:
            print("Grade not found.")
            return

        grade.grade = grade_value
        grade.grade_date = date.fromisoformat(grade_date)
        grade.student_id = student_id
        grade.subject_id = subject_id

        session.commit()

        print(
            f"Grade updated: "
            f"{grade.id} - "
            f"Grade: {grade.grade}, "
            f"Student: {grade.student_id}, "
            f"Subject: {grade.subject_id}, "
            f"Date: {grade.grade_date}"
        )

    except ValueError:
        session.rollback()
        print("Date must be in YYYY-MM-DD format.")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()

def remove_group(group_id):
    session = SessionLocal()

    try:
        group = session.query(Group).filter(
            Group.id == group_id
        ).first()

        if not group:
            print("Group not found.")
            return

        session.delete(group)
        session.commit()

        print(f"Group removed: {group_id}")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()

def remove_teacher(teacher_id):
    session = SessionLocal()

    try:
        teacher = session.query(Teacher).filter(
            Teacher.id == teacher_id
        ).first()

        if not teacher:
            print("Teacher not found.")
            return

        session.delete(teacher)
        session.commit()

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def remove_student(student_id):
    session = SessionLocal()

    try:
        student = session.query(Student).filter(
            Student.id == student_id
        ).first()

        if not student:
            print("Student not found.")
            return

        session.query(Grade).filter(
            Grade.student_id == student_id
        ).delete(
            synchronize_session=False
        )

        session.delete(student)
        session.commit()

        print(f"Student removed: {student_id}")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def remove_subject(subject_id):
    session = SessionLocal()

    try:
        subject = session.query(Subject).filter(
            Subject.id == subject_id
        ).first()

        if not subject:
            print("Subject not found.")
            return

        session.query(Grade).filter(
            Grade.subject_id == subject_id
        ).delete(
            synchronize_session=False
        )

        session.delete(subject)
        session.commit()

        print(f"Subject removed: {subject_id}")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()


def remove_grade(student_id, subject_id, grade_date):
    session = SessionLocal()

    try:
        grade = session.query(Grade).filter(
            Grade.student_id == student_id,
            Grade.subject_id == subject_id,
            Grade.grade_date == date.fromisoformat(grade_date)
        ).first()

        if not grade:
            print("Grade not found.")
            return

        session.delete(grade)
        session.commit()

        print(
            f"Grade removed: "
            f"Student: {student_id}, "
            f"Subject: {subject_id}, "
            f"Date: {grade_date}"
        )

    except ValueError:
        session.rollback()
        print("Date must be in YYYY-MM-DD format.")

    except Exception as error:
        session.rollback()
        print(f"Error: {error}")

    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser(
        description="Student database CLI"
    )

    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
        help="Action to perform"
    )

    parser.add_argument(
        "-m",
        "--model",
        required=True,
        choices=[
            "Teacher",
            "Student",
            "Group",
            "Subject",
            "Grade"
        ],
        help="Model to work with"
    )

    parser.add_argument(
        "--id",
        type=int,
        help="ID of the record"
    )

    parser.add_argument(
        "-n",
        "--name",
        help="Name"
    )

    parser.add_argument(
        "--group-id",
        type=int,
        help="Group ID"
    )

    parser.add_argument(
        "--teacher-id",
        type=int,
        help="Teacher ID"
    )

    parser.add_argument(
        "--student-id",
        type=int,
        help="Student ID"
    )

    parser.add_argument(
        "--subject-id",
        type=int,
        help="Subject ID"
    )

    parser.add_argument(
        "--grade",
        type=int,
        help="Grade value"
    )

    parser.add_argument(
        "--grade-date",
        help="Grade date YYYY-MM-DD"
    )
    
    args = parser.parse_args()

    models = {
        "Teacher": Teacher,
        "Student": Student,
        "Group": Group,
        "Subject": Subject,
        "Grade": Grade,
    }

    if args.action == "list":
        list_records(models[args.model])

    if args.action == "create" and args.model == "Group":
        create_group(args.name)

    if args.action == "create" and args.model == "Teacher":
        create_teacher(args.name)

    if args.action == "create" and args.model == "Student":
        create_student(args.name, args.group_id)

    if args.action == "create" and args.model == "Subject":
      create_subject(args.name, args.teacher_id)

    if args.action == "create" and args.model == "Grade":
      create_grade(args.student_id, args.subject_id, args.grade, args.grade_date)

    if args.action == "update" and args.model == "Group":
       update_group(args.id, args.name)

    if args.action == "update" and args.model == "Teacher":
        update_teacher(args.id, args.name)

    if args.action == "update" and args.model == "Student":
        update_student(args.id, args.name, args.group_id)

    if args.action == "update" and args.model == "Subject":
        update_subject(args.id, args.name, args.teacher_id)

    if args.action == "update" and args.model == "Grade":
        update_grade(args.id, args.grade, args.grade_date, args.student_id, args.subject_id)

    if args.action == "remove" and args.model == "Group":
        remove_group(args.id)

    if args.action == "remove" and args.model == "Teacher":
        remove_teacher(args.id)

    if args.action == "remove" and args.model == "Student":
        remove_student(args.id)

    if args.action == "remove" and args.model == "Subject":
        remove_subject(args.id)

    if args.action == "remove" and args.model == "Grade":
        remove_grade(args.student_id, args.subject_id, args.grade_date)

if __name__ == "__main__":
    main()