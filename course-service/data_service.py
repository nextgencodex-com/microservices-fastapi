class CourseMockDataService:
    def __init__(self):
        self.courses = [
            {"id": 1, "name": "Computer Science", "code": "CS101"},
            {"id": 2, "name": "Software Engineering", "code": "SE202"},
            {"id": 3, "name": "Data Science", "code": "DS303"}
        ]

    def get_all_courses(self):
        return self.courses

    def get_course_by_id(self, course_id: int):
        return next((c for c in self.courses if c["id"] == course_id), None)