import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


async def sendEmail():

    sender = 'housebudgetapplication@gmail.com'
    password = 'mir97beo'
    send_to = 'ptrajkovic997@gmail.com'
    subject = 'Testiranje'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = send_to
    msg['Subject'] = subject

    html = """
    <html>
    <head></head>
      <body>
        <p style='color:blue;'>Link:</p>
        <a href="http://localhost:4200/joingroup">Korisnik vas poziva u grupu</a>
      </body>
    </html>
    """

    body = ''
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    msg.attach(MIMEText(body, 'plain'))

    filename = 'data/images/abstract.jpg'

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    server.sendmail(sender, send_to, text)
    server.quit()

#from tortoise.queryset import Q
#from tortoise.queryset import Q
#from tortoise.queryset import Q
