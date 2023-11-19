"""Main file for object and classes homework."""
from __future__ import annotations

import typing


class Person:
    """Base class for Student and Mentor classes."""

    def __init__(self, name: str, surname: str) -> None:
        """Initialize a student object with the given name and surname."""
        self.name = name
        self.surname = surname
        self.grades: dict[str, list[int]] = {"": [0]}

    def avg_grade(self) -> float:
        """Calculate average of all grades from all courses for the student."""
        if self.grades:
            total_sum: float = 0
            total_count = 0
            for grades in self.grades.values():
                if len(grades) > 0:
                    total_sum += round(sum(grades) / len(grades), 6)
                    total_count += 1
            if total_count > 0:
                return round(total_sum / total_count, 6)
            return 0
        return 0

    def __lt__(self, other: object) -> bool:
        """Compare two student objects based on their average grades."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.avg_grade() < other.avg_grade()

    def __le__(self, other: object) -> bool:
        """Compare two student objects based on their average grades."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.avg_grade() <= other.avg_grade()

    def __eq__(self, other: object) -> bool:
        """Compare two student objects based on their average grades."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.avg_grade() == other.avg_grade()

    def __ne__(self, other: object) -> bool:
        """Compare two student objects based on their average grades."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.avg_grade() != other.avg_grade()

    def __gt__(self, other: object) -> bool:
        """Compare two student objects based on their average grades."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.avg_grade() > other.avg_grade()

    def __ge__(self, other: object) -> bool:
        """Compare two student objects based on their average grades."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.avg_grade() >= other.avg_grade()


class Student(Person):
    """Student class implementation."""

    def __init__(self, name: str, surname: str, grades: dict[str, list[int]]) -> None:
        """Initialize a student object with the given name, surname and grades."""
        super().__init__(name, surname)
        self.finished_courses: set[str] = set()
        self.courses_in_progress: set[str] = set()
        self.grades: dict[str, list[int]] = grades

    def __str__(self) -> str:
        """Return a string representation of the Student object."""
        # fmt: off
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за Домашние задания: {self.avg_grade()}\n"
            f"Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n"
            f"Завершенные курсы: {", ".join(self.finished_courses)}\n"
        )
        # fmt: off

    def rate_lecture(
        self,
        lecturer: Lecturer,
        course: str,
        grade: int,
    ) -> str | None:
        """Rate a lecture given by a lecturer for a specific course and update the grades."""
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
        ):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
            return None
        return "Ошибка"


class Mentor(Person):
    """Common class for Lecturer and Reviewer classes."""

    def __init__(self, name: str, surname: str) -> None:
        """Initialize a Mentor object with the given name and surname."""
        super().__init__(name, surname)
        self.courses_attached: set[str] = set()


class Lecturer(Mentor):
    """Lecturer class implementation."""

    def __init__(self, name: str, surname: str, grades: dict[str, list[int]]) -> None:
        """Initialize a Mentor object with the given name, surname and grades."""
        super().__init__(name, surname)
        self.grades = grades

    def __str__(self) -> str:
        """Return a string representation of the Lecturer object."""
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self.avg_grade()}"
        )


class Reviewer(Mentor):
    """Reviewer class implementation."""

    def rate_hw(
        self,
        student: str,
        course: str,
        grade: int,
    ) -> str | None:
        """Rate a homework submitted by a student for a specific course and update the grades."""
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
            return None
        return "Ошибка"

    def __str__(self) -> str:
        """Return a string representation of the Reviewer object."""
        return f"Имя: {self.name}\nФамилия: {self.surname}"  # noqa: RUF001


def calculate_avg_work_grade(
    persons: typing.Sequence[Student | Lecturer],
    course: str,
) -> float:
    """Calculate the average grade for a specific course across all students and lecturers."""
    total_sum = 0
    total_count = 0

    for person in persons:
        if course in person.grades:
            work = person.grades[course]
            total_sum += sum(work)
            total_count += len(work)

    if total_count > 0:
        return round(total_sum / total_count, 6)
    return 0


# ruff: noqa: T201, COM812
if __name__ == "__main__":
    students = [
        Student("Student1", "Student1", {"Math": [5, 5, 5], "English": [2, 3, 4]}),
        Student("Student2", "Student2", {"Math": [5, 5, 5], "Physics": [5, 5, 5]}),
        Student("Student3", "Student3", {"Math": [5, 5, 5], "English": [4, 4, 4]}),
    ]

    lecturers = [
        Lecturer("Lecturer1", "Lecturer1", {"Math": [6, 7, 8], "Physics": [9, 9, 10]}),
        Lecturer("Lecturer2", "Lecturer2", {"Math": [9, 10, 8], "English": [7, 8, 9]}),
        Lecturer("Lecturer3", "Lecturer3", {"Math": [5, 4, 6], "English": [1, 5, 3]}),
    ]

    for course in ["Math", "Physics", "English"]:
        average_grade_students = calculate_avg_work_grade(students, course)
        average_grade_lecturers = calculate_avg_work_grade(lecturers, course)
        print(
            f"Средняя оценка за домашние задания по курсу {course} (студенты): {average_grade_students}"
        )
        print(
            f"Средняя оценка за лекции по курсу {course} (лекторы): {average_grade_lecturers}"
        )
        print("*" * 100)

    print("=" * 100)
    st1 = Student("Student1", "Student1", {"Math": [5, 5, 5], "English": [5, 5, 5]})
    st2 = Student("Student2", "Student2", {"Math": [5, 5, 5], "Physics": [5, 5, 4]})

    print(st2 < st1)

    lect1 = Lecturer(
        "Lecturer1", "Lecturer1", {"Math": [10, 10, 10], "Physics": [10, 10, 10]}
    )
    lect2 = Lecturer(
        "Lecturer2", "Lecturer2", {"Math": [10, 10, 10], "English": [10, 10, 10]}
    )

    print(lect1 == lect2)
