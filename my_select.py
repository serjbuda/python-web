from sqlalchemy import func
from seed import Student, Group, Teacher, Subject, Grade
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    query = session.query(Student).\
        join(Grade).\
        group_by(Student.id).\
        order_by(func.avg(Grade.grade).desc()).\
        limit(5)
    result = session.execute(query)
    return result.fetchall()

def select_2(subject_name):
    query = session.query(Student).\
        join(Grade).\
        join(Subject).\
        filter(Subject.name == subject_name).\
        group_by(Student.id).\
        order_by(func.avg(Grade.grade).desc()).\
        limit(1)
    result = session.execute(query)
    return result.fetchone()

def select_3(subject_name):
    query = session.query(Group.name, func.avg(Grade.grade)).\
        join(Student).\
        join(Grade).\
        join(Subject).\
        filter(Subject.name == subject_name).\
        group_by(Group.name)
    result = session.execute(query)
    return result.fetchall()

def select_4():
    query = session.query(func.avg(Grade.grade))
    result = session.execute(query)
    return result.scalar()

def select_5(teacher_name):
    query = session.query(Subject.name).\
        join(Teacher).\
        filter(Teacher.name == teacher_name)
    result = session.execute(query)
    return result.fetchall()

def select_6(group_name):
    query = session.query(Student).\
        join(Group).\
        filter(Group.name == group_name)
    result = session.execute(query)
    return result.fetchall()

def select_7(group_name, subject_name):
    query = session.query(Student, Grade).\
        join(Group).\
        join(Grade).\
        join(Subject).\
        filter(Group.name == group_name, Subject.name == subject_name)
    result = session.execute(query)
    return result.fetchall()

def select_8(teacher_name):
    query = session.query(func.avg(Grade.grade)).\
        join(Subject).\
        join(Teacher).\
        filter(Teacher.name == teacher_name)
    result = session.execute(query)
    return result.scalar()

def select_9(student_name):
    query = session.query(Subject.name).\
        join(Grade).\
        join(Student).\
        filter(Student.name == student_name)
    result = session.execute(query)
    return result.fetchall()

def select_10(student_name, teacher_name):
    query = session.query(Subject.name).\
        join(Grade).\
        join(Student).\
        join(Teacher).\
        filter(Student.name == student_name, Teacher.name == teacher_name)
    result = session.execute(query)
    return result.fetchall()
