from canvas import Canvas
from send_msg import Email

def main():
    canvas = Canvas()
    grades = canvas.grades()

    email = Email()
    email.send_email(grades)

if __name__ == "__main__":
    main()