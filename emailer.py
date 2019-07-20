import smtplib
# import email.message as msg

from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes



"""

TDOO: Add the actual scraper and make this more like a class

"""

class HackbusterEmail:
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    def __init__(self, email_id, password):
        self.email_id = email_id
        self.password = password
        self.m = EmailMessage()
        
    def send_message(self, title, author, image_url, message, url):
        self.smtp.starttls()
        self.smtp.login(self.email_id, self.password)

        # new_scrape = hackbuster_scraper.HackbusterScraper().get_full_article()
        self.m['Subject'] = title
        self.m['From'] = self.email_id
        self.m['To'] = self.email_id
        
        

        self.m.add_alternative("""\
            <html>
                <body>
                    <h1>{}</h1>
                    <h3><i>{}</i></h3>
                    <p style="white-space: pre; font-size: 15px">{}</p>
                    <b><h4 style="font-size: 15px"><a href={}>Article link</a></h4</b>
                </body>
            </html>
            """.format(title, author, message, url), subtype='html')

        self.smtp.sendmail(self.email_id, self.email_id, (self.m.as_string().encode('utf8')))

        self.smtp.quit()
        print("Message sent!")








