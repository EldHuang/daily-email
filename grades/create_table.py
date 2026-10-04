import pandas as pd
from grades.database import Database, db
from sqlalchemy import select, desc


class CreateTable:
    def __init__(self):
        self.compiledData = {
            "Subject": [],
            "Letter": [],
            "Percent": [],
        }
        self.grades_table = None

    def convert_data(self, period_map, days_to_offset):
        self.compiledData = {
            "Subject": [],
            "Letter": [],
            "Percent": [],
        }

        period_map = list(period_map)
        database = Database()

        with database.app.app_context():
            reverse_list = select(database.Grades).order_by(desc(database.Grades.id))
            last_entry = db.session.scalar(reverse_list.offset(days_to_offset))

        for period in range(1, 8):
            period_data = getattr(last_entry, f"Per{period}")

            self.compiledData["Subject"].append(period_map[period-1])
            self.compiledData["Letter"].append(period_data.split(",")[0])
            self.compiledData["Percent"].append(period_data.split(",")[1])

        pd.set_option('display.unicode.east_asian_width', True)
        self.grades_table = pd.DataFrame(self.compiledData)

        return self.grades_table


    def change(self, val, yesterday):
        red = "background-color: #ffb0b0;"
        green = "background-color: #affac9;"
        white = "background-color: #ffffff;"

        val = float(val)
        yesterday = float(yesterday)
        difference = f"{val - yesterday:.3f}"

        # Adds + to beginning if positive
        if float(difference) >= 0:
            difference = f"+{difference}"

        if val < yesterday:
            return red, difference
        elif val > yesterday:
            return green, difference
        else:
           return white, difference


    # Use raw html to create table because Gmail is finicky on what CSS can be passed
    def create_grades_table(self, yesterday):
        html = """
        <table>
            <thead>
                <tr>
                    <th>Subject</th>
                    <th>Letter</th>
                    <th>Percent</th>
                    <th>Change</th>
                </tr>
            </thead>
            <tbody>
        """

        for class_index, row in self.grades_table.iterrows():
            yesterday_same_cell = yesterday.iloc[class_index, 2]

            color, difference = self.change(row["Percent"], yesterday=yesterday_same_cell)

            html += f"""
                <tr>
                    <td>{row["Subject"]}</td>
                    <td>{row["Letter"]}</td>
                    <td style="{color}">{row["Percent"]}</td>
                    <td style="{color}">{difference}</td>
                </tr>
            """

        html += """
            </tbody>
        </table>
        """

        return html

