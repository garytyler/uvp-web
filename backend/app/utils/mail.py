import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader, Template
from pydantic import EmailStr

from app.core.config import get_settings


def get_template(file_name: str) -> Template:
    loader = PackageLoader("app", "templates")
    env = Environment(loader=loader)
    return env.get_template(file_name)


def send_email(
    email_to: EmailStr,
    subject_template: Template,
    plain_template: Template = None,
    html_template: Template = None,
    context: dict = {},
) -> None:
    settings = get_settings()
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    assert plain_template or html_template, "at least one template is required"
    msg = MIMEMultipart("alternative")
    msg["To"] = email_to
    msg["From"] = settings.EMAILS_FROM_EMAIL
    msg["Subject"] = subject_template.render(**context)
    if plain_template:
        plain_content: str = plain_template.render(**context)
        msg.attach(MIMEText(plain_content, "plain"))
    if html_template:
        html_content: str = html_template.render(**context)
        msg.attach(MIMEText(html_content, "html"))
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(
            from_addr=settings.EMAILS_FROM_EMAIL, to_addrs=email_to, msg=msg.as_string()
        )


def send_test_email(email_to: str) -> None:
    settings = get_settings()
    send_email(
        email_to=email_to,
        subject_template=Template("{{ project_name }} - Test email"),
        html_template=get_template("test_email.html"),
        context={"project_name": settings.PROJECT_NAME},
    )


def send_reset_password_email(email_to: str, token: str) -> None:
    settings = get_settings()
    send_email(
        email_to=email_to,
        subject_template=Template(f"Password recovery for {email_to}"),
        plain_template=get_template("reset_password.txt"),
        html_template=get_template("reset_password.html"),
        context={
            "project_name": settings.PROJECT_NAME,
            "action_title": "Reset Your Password",
            "action_url": f"{settings.SERVER_HOST}/access/reset-password?token={token}",
            "hours_valid": settings.EMAIL_PASSWORD_RESET_TOKEN_EXPIRE_HOURS,
        },
    )
