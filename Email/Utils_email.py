import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Config.config import SENDER, PASSWORD, SMTP, PORT


def send_email(to_addr, subject, message):
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP_SSL(SMTP, PORT)
    server.ehlo(SENDER)

    try:
        server.login(SENDER, PASSWORD)
        server.auth_plain()
        server.send_message(msg)
        server.quit()

        return "Success!"
    except Exception as _ex:
        return f"{_ex} Wrong"


def send_email_pdf(to_addr, subject, message, pdf_str):
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    pdf = MIMEApplication(open(f"Attachments/{pdf_str}.pdf", 'rb').read())
    pdf.add_header('Content-Disposition', 'attachment', filename=f"{pdf_str}.pdf")
    msg.attach(pdf)

    server = smtplib.SMTP_SSL(SMTP, PORT)
    server.ehlo(SENDER)

    try:
        server.login(SENDER, PASSWORD)
        server.auth_plain()
        server.send_message(msg)
        server.quit()

        return "Success!"
    except Exception as _ex:
        return f"{_ex} Wrong"