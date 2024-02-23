import smtplib

MY_EMAIL = "your-email"
MY_PASSWORD = "your-password"


class NotificationManager:
    """Sends email to users regarding lowest price flight deals."""

    def send_mail(self, emails, message):
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        for email in emails:
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email,
                msg=f"Subject: New Low Price Flight!\n\n{message}".encode('utf-8')
            )
