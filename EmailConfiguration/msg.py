from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import smtplib
from django.utils import timezone
from EmailConfiguration.models import ToEmail, Setting, ClientMessage
from settings.models import CompanyDetails

def generate_pdf(name, email, company, contact_number, service_type, message):
    """Generate a nicely formatted PDF in memory"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(f"<b>New Website Enquiry – {company}</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Table Data
    data = [
        ["Field", "Details"],
        ["Name", name],
        ["Email", email],
        ["Phone", contact_number],
        ["Company", company],
        ["Service Type", service_type],
        ["Message", message],
        ["Received On", timezone.now().strftime('%d-%m-%Y %I:%M %p')]
    ]

    table = Table(data, colWidths=[120, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

def process(name, email, company, contact_number, service_type, message):
    """Save client message and send email to admins with PDF attachment"""
    try:
        ClientMessage.objects.create(
            client_name=name,
            client_mail=email,
            company_name=company,
            contact_number=contact_number,
            service_type=service_type,
            messages=message
        )
        print("✅ Client message saved")
    except Exception as e:
        print("❌ Failed to save client message:", e)
        return False

    # Email settings
    try:
        setting = Setting.objects.get()
        sender_email = setting.email
        email_password = setting.password
        smtp_host = setting.host
        smtp_port = setting.port
    except:
        print("❌ Email settings not configured")
        return False

    company_details = CompanyDetails.objects.first()
    company_display_name = company_details.companyname if company_details else "Capricorn Shipping"
    website_link = "https://www.capricornshippingqatar.com"

    recipients = ToEmail.objects.filter(active_status=True)
    if not recipients.exists():
        print("⚠ No active admin recipients found")
        return True

    mail_subject = f"New Website Enquiry – {company}"

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, email_password)

        for recipient in recipients:
            receiver_email = recipient.email
            team_name = recipient.position or "Team"

            # HTML body (message appears directly in email)
            body_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #000;">
                <p>Dear {team_name} Team,</p>
                <p>You have received a new enquiry through the website. The details are:</p>

                <table cellpadding="6" cellspacing="0" style="border-collapse: collapse; border: 1px solid #000;">
                    <tr><td><b>Name:</b></td><td>{name}</td></tr>
                    <tr><td><b>Email:</b></td><td>{email}</td></tr>
                    <tr><td><b>Phone:</b></td><td><a href="tel:{contact_number}" style="color:#000; text-decoration:none;">{contact_number}</a></td></tr>
                    <tr><td><b>Company:</b></td><td>{company}</td></tr>
                    <tr><td><b>Service Type:</b></td><td>{service_type}</td></tr>
                    <tr><td><b>Message:</b></td><td>{message}</td></tr>
                    <tr><td><b>Received On:</b></td><td>{timezone.now().strftime('%d-%m-%Y %I:%M %p')}</td></tr>
                </table>

                <p>Best regards,<br>
                <b>{company_display_name}</b><br>
                <a href="{website_link}" target="_blank">{website_link}</a></p>
            </body>
            </html>
            """

            msg = MIMEMultipart("alternative")
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = mail_subject
            msg.attach(MIMEText(body_html, "html"))

            # Attach PDF
            pdf_buffer = generate_pdf(name, email, company, contact_number, service_type, message)
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_buffer.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=Enquiry_{name}.pdf")
            msg.attach(part)

            try:
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print(f"✅ Mail with PDF sent to {receiver_email}")
            except Exception as e:
                print(f"❌ Mail failed to {receiver_email}: {e}")

    finally:
        server.quit()

    print("✅ Process completed successfully with PDF")
    return True
