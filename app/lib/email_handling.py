from app.lib.token_handling import generate_activation_token
from flask_mail import Message
from app.extensions import mail

def send_activate_email(userId, email, name):
    token = generate_activation_token(userId, email, salt='email-activate')
    activation_link = f"http://127.0.0.1:5000/activate/{token}"
    msg = Message(
        subject="註冊成功，啟用APP帳號",
        recipients=[email],
        html=f"""
            <html>
                <body>
                    <p>{name} 您好，</p>
                    <p>請點擊以下連結以啟用您的帳號：</p>
                    <p><a href="{activation_link}">啟用帳號</a></p>
                    <p>如果您並未註冊此帳號，請忽略此封郵件。</p>
                </body>
            </html>
        """
    )
    mail.send(msg)

def send_reset_password_email(userId, email, name):
    reset_token = generate_activation_token(userId, email, salt='reset-password')
    reset_url = f"http://127.0.0.1:5000/reset-password/{reset_token}"
        
    msg = Message(
        subject="Password Reset Request",
        recipients=[email],
        html=f"""
            <html>
                <body>
                    <p>{user.name} 您好，</p>
                    <p>請點擊以下連結以重設您的密碼：</p>
                    <p><a href="{reset_url}">重設密碼</a></p>
                </body>
            </html>
        """
    )
    mail.send(msg)