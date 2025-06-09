from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float, Table,inspect
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///students.db')
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    """
    Tworzy bazę danych SQLite oraz tabele na podstawie modeli.

    Wykorzystuje SQLAlchemy do wygenerowania struktur w bazie danych
    zgodnych z zdefiniowanymi klasami modelu.
    """
    Base.metadata.create_all(engine)


class User(Base):
    """
    Bazowa klasa użytkownika.

    Zawiera wspólne pola dla wszystkich typów użytkowników (student, nauczyciel, admin).

    :cvar __tablename__: Nazwa tabeli w bazie danych.
    :ivar id: Unikalny identyfikator użytkownika.
    :vartype id: int
    :ivar type: Typ użytkownika wykorzystywany do polimorfizmu.
    :vartype type: str
    :ivar first_name: Imię użytkownika.
    :vartype first_name: str
    :ivar last_name: Nazwisko użytkownika.
    :vartype last_name: str
    :ivar username: Unikalna nazwa użytkownika.
    :vartype username: str
    :ivar password_hash: Hasło w postaci zahashowanej.
    :vartype password_hash: str
    :ivar role: Rola użytkownika (np. "student").
    :vartype role: str
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    type = Column(String)  # potrzebne do dziedziczenia
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String, default="student")

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Student(User):
    """
    Klasa reprezentująca studenta.

    Dziedziczy po klasie User.

    :ivar id: Unikalny identyfikator studenta (ForeignKey do User.id).
    :vartype id: int
    :ivar grades: Lista ocen przypisanych do studenta.
    :vartype grades: list[Grade]
    :ivar schedules: Lista zajęć (harmonogram) studenta.
    :vartype schedules: list[Schedule]
    :ivar group_id: Identyfikator grupy, do której należy student.
    :vartype group_id: int
    :ivar group: Obiekt grupy, do której należy student.
    :vartype group: Group
    """
    __tablename__ = 'student'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    grades = relationship("Grade", back_populates="student")
    schedules = relationship("Schedule", back_populates="student")
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="students")

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }


class Teacher(User):
    """
    Klasa reprezentująca nauczyciela.

    Dziedziczy po klasie User.

    :ivar id: Unikalny identyfikator nauczyciela (ForeignKey do User.id).
    :vartype id: int
    :ivar subjects: Lista przedmiotów nauczanych przez nauczyciela.
    :vartype subjects: list[Subject]
    :ivar grades: Lista ocen wystawionych przez nauczyciela.
    :vartype grades: list[Grade]
    :ivar schedules: Lista zajęć nauczyciela.
    :vartype schedules: list[Schedule]
    """
    __tablename__ = 'teacher'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    subjects = relationship("Subject", secondary="teacher_subject_link", back_populates="teachers")
    grades = relationship("Grade", back_populates="teacher")
    schedules = relationship("Schedule", back_populates="teacher")

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }


class Admin(User):
    """
    Klasa reprezentująca administratora.

    Dziedziczy po klasie User.

    :ivar id: Unikalny identyfikator administratora (ForeignKey do User.id).
    :vartype id: int
    """
    __tablename__ = 'admin'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class Group(Base):
    """
    Klasa reprezentująca grupę studentów.

    :ivar id: Unikalny identyfikator grupy.
    :vartype id: int
    :ivar name: Nazwa grupy.
    :vartype name: str
    :ivar students: Lista studentów należących do grupy.
    :vartype students: list[Student]
    :ivar max_students: Maksymalna liczba studentów w grupie.
    :vartype max_students: int
    """
    __tablename__ = 'groups'  # group często jest zarezerwowana nazwa w SQL
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Student", back_populates="group")
    max_students = Column(Integer)


class Subject(Base):
    """
    Klasa reprezentująca przedmiot.

    :ivar id: Unikalny identyfikator przedmiotu.
    :vartype id: int
    :ivar name: Nazwa przedmiotu.
    :vartype name: str
    :ivar nick: Skrót nazwy przedmiotu.
    :vartype nick: str
    :ivar color: Kolor przypisany do przedmiotu (np. dla wykresów).
    :vartype color: str
    :ivar teachers: Lista nauczycieli prowadzących ten przedmiot.
    :vartype teachers: list[Teacher]
    :ivar grades: Lista ocen z tego przedmiotu.
    :vartype grades: list[Grade]
    :ivar schedules: Lista zajęć tego przedmiotu.
    :vartype schedules: list[Schedule]
    """
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nick = Column(String)
    color = Column(String, default="#FFFFFF")
    teachers = relationship("Teacher", secondary="teacher_subject_link", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")
    schedules = relationship("Schedule", back_populates="subject")


teacher_subject_link = Table(
    'teacher_subject_link',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teacher.id')),
    Column('subject_id', Integer, ForeignKey('subject.id'))
)
"""
Tabela łącząca relację wiele-do-wielu między nauczycielami i przedmiotami.
"""


class Time(Base):
    """
    Klasa reprezentująca godzinę (okno czasowe zajęć).

    :ivar id: Unikalny identyfikator wpisu czasu.
    :vartype id: int
    :ivar time: Opis czasu (np. "10:15 - 11:45").
    :vartype time: str
    :ivar schedules: Lista zajęć przypisanych do tego czasu.
    :vartype schedules: list[Schedule]
    """
    __tablename__ = 'time'
    id = Column(Integer, primary_key=True)
    time = Column(String)  # np. "10:15 - 11:45"
    schedules = relationship("Schedule", back_populates="time")


class Schedule(Base):
    """
    Klasa reprezentująca harmonogram zajęć.

    :ivar id: Unikalny identyfikator zajęcia.
    :vartype id: int
    :ivar day: Dzień tygodnia (np. "Poniedziałek").
    :vartype day: str
    :ivar time_id: Identyfikator czasu zajęć.
    :vartype time_id: int
    :ivar time: Obiekt czasu zajęć.
    :vartype time: Time
    :ivar student_id: Identyfikator studenta przypisanego do zajęć.
    :vartype student_id: int
    :ivar student: Obiekt studenta.
    :vartype student: Student
    :ivar teacher_id: Identyfikator nauczyciela prowadzącego zajęcia.
    :vartype teacher_id: int
    :ivar teacher: Obiekt nauczyciela.
    :vartype teacher: Teacher
    :ivar subject_id: Identyfikator przedmiotu zajęć.
    :vartype subject_id: int
    :ivar subject: Obiekt przedmiotu.
    :vartype subject: Subject
    """
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    day = Column(String)

    time_id = Column(Integer, ForeignKey('time.id'))
    time = relationship("Time", back_populates="schedules")

    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", back_populates="schedules")

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship("Teacher", back_populates="schedules")

    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship("Subject", back_populates="schedules")


class Grade(Base):
    """
    Klasa reprezentująca ocenę.

    :ivar id: Unikalny identyfikator oceny.
    :vartype id: int
    :ivar grade: Wartość oceny (np. 4.5).
    :vartype grade: float
    :ivar date: Data wystawienia oceny.
    :vartype date: datetime.date
    :ivar student_id: Identyfikator studenta, któremu wystawiono ocenę.
    :vartype student_id: int
    :ivar student: Obiekt studenta.
    :vartype student: Student
    :ivar teacher_id: Identyfikator nauczyciela wystawiającego ocenę.
    :vartype teacher_id: int
    :ivar teacher: Obiekt nauczyciela.
    :vartype teacher: Teacher
    :ivar subject_id: Identyfikator przedmiotu, którego dotyczy ocena.
    :vartype subject_id: int
    :ivar subject: Obiekt przedmiotu.
    :vartype subject: Subject
    """
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True)
    grade = Column(Float)
    date = Column(Date)

    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship("Student", back_populates="grades")

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship("Teacher", back_populates="grades")

    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship("Subject", back_populates="grades")