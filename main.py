from canvas import Canvas
from send_msg import Email

def main():
    canvas = Canvas()
    grades = canvas.grades()

    email = Email()
    email.convert_data(grades)
    email.send_email()

if __name__ == "__main__":
    main()