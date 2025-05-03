import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# SMTP configuration (example using Gmail; you can also use Amazon SES or Mailtrap)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  
RECEIVER_EMAIL = "employee@example.com"
msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = "Exciting Job Opportunity & Diwali Surprise Gift from Amazon Careers!"
body = """
Dear Candidate,
Congratulations! You have been shortlisted for a position at Amazon Careers.
Click the link below to view your offer letter and claim your exclusive Diwali surprise gift.
http://<IP address>/download-offer
Best Regards,
Ammmazon Careers Recruitment Team
"""
msg.attach(MIMEText(body, "plain"))
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("Phishing email sent successfully!")
except Exception as e:
    print("Error sending email:", e)
