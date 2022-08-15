import smtplib
from .pswrd import gmail, pswrd

def send_email(data):
    sent_from = gmail
    to = [data['to_user']]
    subject = data['subject']
    body = data['body']

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail, pswrd)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")

    except Exception as ex:
        print ("Something went wrong….",ex)