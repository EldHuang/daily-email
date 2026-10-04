from grades.canvas import Canvas
from grades.database import Database
from grades.create_table import CreateTable
from send_msg import Email

"""
Add tokens and env variables every time program is run locally in a new window. New terminal environment does not store old variables.
Export: EMAIL (cuhsd)
        PASS (Python app password)
        TOKEN (Canvas token)
"""

# Name of classes on dashboard of canvas
period_map = {
    "音樂課 - Mr. C": "Per1",
    "英文課 - Mr. Gill": "Per2",
    "華語課 - 游老師": "Per3",
    "電腦課 - Caces": "Per4",
    "數學課 - Pantoja": "Per5",
    "生物學課 - Stephenson": "Per6",
    "PE - Andrade": "Per7"
}

def main():
    canvas = Canvas()
    grades = canvas.grades()

    database = Database()
    database.add_grades(grades, period_map)

    # Always run today's data second to ensure new stored data is today's
    createTable = CreateTable()
    yesterday = createTable.convert_data(period_map=period_map, days_to_offset=1)
    createTable.convert_data(period_map=period_map, days_to_offset=0)
    grades_table = createTable.create_grades_table(yesterday=yesterday)

    email = Email()
    email.send_email(grades_table)

if __name__ == "__main__":
    main()