import os
import requests

class Canvas:
    def __init__(self):
        self.token = os.environ["TOKEN"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.base_url = "https://cuhsd.instructure.com/api/v1"

    def grades(self):
        response = requests.get(
            f"{self.base_url}/users/self/enrollments",
            headers=self.headers
        )
        response.raise_for_status()

        classList = {}

        for enrollment in response.json():
            course_id = enrollment["course_id"]
            grades = enrollment.get("grades", {})

            course_response = requests.get(
                f"{self.base_url}/courses/{course_id}",
                headers=self.headers
            )
            course_response.raise_for_status()

            course = course_response.json()
            name = course["name"]

            try:
                score = round(grades.get("current_score"), 2)
            except TypeError:
                score = None

            classList[name] = {
                "href": course.get("html_url"),
                "overall": grades.get("current_grade"),
                "current_score": grades.get("current_score"),
                "score": score
            }

        classList.pop("Class of 2030 Counseling", None)

        return classList

canvas = Canvas()
canvas.grades()
