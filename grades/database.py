from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

class Database:
    class Grades(db.Model):
        id: Mapped[int] = mapped_column(primary_key=True)
        timestamp: Mapped[datetime] = mapped_column(unique=True)
        Per1: Mapped[str] = mapped_column()
        Per2: Mapped[str] = mapped_column()
        Per3: Mapped[str] = mapped_column()
        Per4: Mapped[str] = mapped_column()
        Per5: Mapped[str] = mapped_column()
        Per6: Mapped[str] = mapped_column()
        Per7: Mapped[str] = mapped_column()

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grades.db"
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def add_grades(self, grades, period_map):
        final_scores = {
            "Per1": "N/A", "Per2": "N/A", "Per3": "N/A",
            "Per4": "N/A", "Per5": "N/A", "Per6": "N/A", "Per7": "N/A"
        }

        for course_name, data in grades.items():
            if course_name in period_map:
                assigned_period = period_map[course_name]
                final_scores[assigned_period] = f"{data["overall"]}, {data["score"]}"

        new_grades = self.Grades(
            timestamp=datetime.now(),
            Per1=final_scores["Per1"],
            Per2=final_scores["Per2"],
            Per3=final_scores["Per3"],
            Per4=final_scores["Per4"],
            Per5=final_scores["Per5"],
            Per6=final_scores["Per6"],
            Per7=final_scores["Per7"]
        )

        with self.app.app_context():
            db.session.add(new_grades)
            db.session.commit()