import random
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailConfiguration.models import ToEmail, Setting,ClientMessage
from settings.models import CompanyDetails  # Import the CompanyInfo model
import smtplib


def process(name, email, subject, message):
    """
    1. Save client message (NO UPDATE allowed)
    2. Send email notification to all active ToEmail users
    """

    # -------------------------
    # Save Client Message FIRST
    # -------------------------
    try:
        ClientMessage.objects.create(
            client_name=name,
            client_mail=email,
            subject=subject,
            messages=message
        )
        print("✅ Client message saved")
    except Exception as e:
        print("❌ Failed to save client message:", e)
        return False

    # -------------------------
    # Fetch Email Settings
    # -------------------------
    try:
        setting = Setting.objects.get()
        sender_email = setting.email
        email_password = setting.password
        smtp_host = setting.host
        smtp_port = setting.port
    except ObjectDoesNotExist:
        print("❌ Email settings not configured")
        return False

    # -------------------------
    # Company Name
    # -------------------------
    company = CompanyDetails.objects.first()
    company_name = company.companyname if company else "Capricorn Shipping"

    # -------------------------
    # Active Admin Recipients
    # -------------------------
    recipients = ToEmail.objects.filter(active_status=True)

    if not recipients.exists():
        print("⚠ No active ToEmail users found")
        return True  # Message is saved, mail skipped

    # -------------------------
    # SMTP Connection
    # -------------------------
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, email_password)

        for recipient in recipients:
            receiver_email = recipient.email

            mail_subject = f"📩 New Contact Message - {company_name}"

            body_html = f"""
            <html>
            <body style="font-family: Arial; color: black;">
                <h2>{company_name}</h2>
                <p><strong>New enquiry received:</strong></p>

                <table cellpadding="6">
                    <tr><td><b>Name</b></td><td>{name}</td></tr>
                    <tr><td><b>Email</b></td><td>{email}</td></tr>
                    <tr><td><b>Subject</b></td><td>{subject}</td></tr>
                    <tr><td><b>Message</b></td><td>{message}</td></tr>
                    <tr>
                        <td><b>Received</b></td>
                        <td>{timezone.now().strftime('%d-%m-%Y %I:%M %p')}</td>
                    </tr>
                </table>

                <br>
                <p>— {company_name} Website</p>
            </body>
            </html>
            """

            msg = MIMEMultipart("alternative")
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = mail_subject
            msg.attach(MIMEText(body_html, "html"))

            try:
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print(f"✅ Mail sent to {receiver_email}")
            except Exception as e:
                print(f"❌ Mail failed to {receiver_email}: {e}")

    finally:
        server.quit()

    print("✅ Process completed")
    return True
