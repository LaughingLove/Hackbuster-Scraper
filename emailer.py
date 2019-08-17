import smtplib
# import email.message as msg

from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes


class HackbusterEmail:
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    def __init__(self, email_id, password):
        self.email_id = email_id
        self.password = password
        self.m = EmailMessage()
    
    # TODO: If there's a connection error, send a message to the dev. saying that the applicaton stopped

    def send_message(self, articles):
        self.smtp.starttls()
        self.smtp.login(self.email_id, self.password)

        final_body = ""

        for article in articles:
            title = article['title']
            author = article['author']
            message = article['content']
            url = article['url']
            format_string = """\
                <div class="news" style="padding: 1em;margin: 1em;border: 2px solid black">
                    <h3>{}</h3>
                    <i><h4>{}</h4></i>
                    <p style="white-space: pre; font-size: 15px">{}</p>
                    <a href={}><button>View article</button></a>
                </div>
                """.format(title, author, message, url)
            final_body+=format_string


        self.m['Subject'] = "[Hackbusters Update Feed] New articles!"
        self.m['From'] = self.email_id
        self.m['To'] = self.email_id
        
        

        self.m.add_alternative("""\
            <html>
                <body>
                    <div class="main" style="padding: 1em">
                        {}
                    </div>
                </body>
            </html>
            """.format(final_body), subtype='html')

        self.smtp.sendmail(self.email_id, self.email_id, (self.m.as_string().encode('utf8')))

        self.smtp.quit()
        print("Message sent!")








