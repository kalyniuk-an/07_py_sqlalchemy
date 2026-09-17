from sqlalchemy import func, select

from database import SessionLocal
from models import Student, Grade, Group, Subject, Teacher


def select_1():
    session = SessionLocal()

    try:
        result = session.execute(
            select(
                Student,
                func.avg(Grade.grade).label("average_grade")
            )
            .join(Grade)
            .group_by(Student.id)
            .order_by(func.avg(Grade.grade).desc())
            .limit(5)
        )

        for student, average_grade in result:
            print(
                student.first_name,
                student.last_name,
                round(average_grade, 2)
            )
    finally:
        session.close()


def select_2(subject_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(
                Student,
                func.avg(Grade.grade).label("average_grade")
            )
            .join(Grade)
            .where(Grade.subject_id == subject_id)
            .group_by(Student.id)
            .order_by(func.avg(Grade.grade).desc())
            .limit(1)
        )

        result = result.first()

        if result:
            student, average_grade = result

            print(
                student.first_name,
                student.last_name,
                round(average_grade, 2)
            )
        else:
            print("No grades found.")

    finally:
        session.close()


def select_3(subject_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(
                Group.name,
                func.avg(Grade.grade).label("average_grade")
            )
            .select_from(Group)
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .where(Grade.subject_id == subject_id)
            .group_by(Group.id, Group.name)
            .order_by(Group.name)
        )

        for group_name, average_grade in result:
            print(
                group_name,
                round(average_grade, 2)
            )

    finally:
        session.close()


def select_4():
    session = SessionLocal()

    try:
        result = session.execute(
            select(func.avg(Grade.grade))
        )

        average_grade = result.scalar()

        print(round(average_grade, 2))

    finally:
        session.close()


def select_5(teacher_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(Subject)
            .where(Subject.teacher_id == teacher_id)
        )

        subjects = result.scalars().all()

        for subject in subjects:
            print(subject.name)

    finally: session.close()


def select_6(group_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(Student)
            .where(Student.group_id == group_id)
        )

        students = result.scalars().all()

        for student in students:
            print(
                student.first_name,
                student.last_name
            )

    finally:
        session.close()


def select_7(group_id, subject_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(
                Student.first_name,
                Student.last_name,
                Grade.grade,
                Grade.grade_date
            )
            .join(Grade, Grade.student_id == Student.id)
            .where(
                Student.group_id == group_id,
                Grade.subject_id == subject_id
            )
            .order_by(Student.last_name, Grade.grade_date)
        )

        for first_name, last_name, grade, grade_date in result:
            print(
                first_name,
                last_name,
                grade,
                grade_date
            )

    finally:
        session.close()


def select_8(teacher_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(
                Teacher.first_name,
                Teacher.last_name,
                func.avg(Grade.grade).label("average_grade")
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .join(Grade, Grade.subject_id == Subject.id)
            .where(Teacher.id == teacher_id)
            .group_by(Teacher.id)
        )

        result = result.first()

        if result:
            first_name, last_name, average_grade = result

            print(
                first_name,
                last_name,
                round(average_grade, 2)
            )
        else:
            print("No grades found.")

    finally:
        session.close()


def select_9(student_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(Subject)
            .join(Grade, Grade.subject_id == Subject.id)
            .where(Grade.student_id == student_id)
            .distinct()
            .order_by(Subject.name)
        )

        subjects = result.scalars().all()

        for subject in subjects:
            print(subject.name)

    finally:
        session.close()


def select_10(teacher_id, student_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(Subject)
            .join(Grade, Grade.subject_id == Subject.id)
            .where(
                Subject.teacher_id == teacher_id,
                Grade.student_id == student_id
            )
            .distinct()
            .order_by(Subject.name)
        )

        subjects = result.scalars().all()

        for subject in subjects:
            print(subject.name)

    finally:
        session.close()


def select_11(teacher_id, student_id):
    session = SessionLocal()

    try:
        result = session.execute(
            select(
                func.avg(Grade.grade).label("average_grade")
            )
            .join(Subject, Subject.id == Grade.subject_id)
            .where(
                Subject.teacher_id == teacher_id,
                Grade.student_id == student_id
            )
        )

        average_grade = result.scalar()

        if average_grade is not None:
            print(round(average_grade, 2))
        else:
            print("No grades found.")

    finally:
        session.close()


def select_12(group_id, subject_id):
    session = SessionLocal()

    try:
        latest_date = session.execute(
            select(func.max(Grade.grade_date))
            .join(Student, Student.id == Grade.student_id)
            .where(
                Student.group_id == group_id,
                Grade.subject_id == subject_id
            )
        ).scalar()

        if latest_date is None:
            print("No grades found.")
            return

        result = session.execute(
            select(
                Student.first_name,
                Student.last_name,
                Grade.grade,
                Grade.grade_date
            )
            .join(Grade, Grade.student_id == Student.id)
            .where(

              Student.group_id == group_id,
              Grade.subject_id == subject_id,
              Grade.grade_date == latest_date
            )
            .order_by(Student.last_name, Student.first_name)
        )

        for first_name, latest_name, grade, grade_date in result:
            print(
                first_name,
                latest_name,
                grade,
                grade_date
            )

    finally:
        session.close()

if __name__ == "__main__":
    select_12(1,2)