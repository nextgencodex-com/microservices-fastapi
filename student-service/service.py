# student-service/service.py
from data_service import StudentMockDataService

class StudentService:
    def __init__(self):
        # Indentation (හිස්තැන්) හරියටම Tab එකක් ඇතුළට තිබිය යුතුය
        self.data_service = StudentMockDataService()

    def get_all(self):
        """සියලුම සිසුන් ලබා ගැනීම"""
        return self.data_service.get_all_students()

    def get_by_id(self, student_id: int):
        """ID එක අනුව ශිෂ්‍යයෙකු ලබා ගැනීම"""
        return self.data_service.get_student_by_id(student_id)

    def create(self, student_data):
        """අලුත් ශිෂ්‍යයෙකු ඇතුළත් කිරීම"""
        return self.data_service.add_student(student_data)

    def update(self, student_id: int, student_data):
        """ශිෂ්‍ය තොරතුරු යාවත්කාලීන කිරීම"""
        return self.data_service.update_student(student_id, student_data)

    def delete(self, student_id: int):
        """ශිෂ්‍යයෙකු ඉවත් කිරීම"""
        return self.data_service.delete_student(student_id)