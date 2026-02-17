from data_service import CourseMockDataService

class CourseService:
    def __init__(self):
        self.data_service = CourseMockDataService()

    def get_all(self):
        return self.data_service.get_all_courses()

    def get_by_id(self, course_id: int):
        return self.data_service.get_course_by_id(course_id)