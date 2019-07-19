import smtplib

class HackbusterScraper:
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    def __init__(self, email_id, password):
        self.email_id = email_id
        self.password = password
        
    def send_message(self, message):
        self.smtp.starttls()
        self.smtp.login(self.email_id, self.password)

        self.smtp.sendmail(self.email_id, self.email_id, message)

        self.smtp.quit()
        print("Message sent!")
