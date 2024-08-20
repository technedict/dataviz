import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_mail(subject, sender, recipients, text_body, html_body):
    port = 587
    smtp_server = "smtp.gmail.com"
    login = "efeeloobenedict@gmail.com"
    password = "oqil cjge rlxa siam" 


    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipients[0]

    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text_body, "plain")
    part2 = MIMEText(html_body, "html")
    message.attach(part1)
    message.attach(part2)

    # send your email
    with smtplib.SMTP(smtp_server, port) as server:
        server.connect(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(login, password)
        server.sendmail(
            sender, recipients, message.as_string()
        )

    print('Sent')
