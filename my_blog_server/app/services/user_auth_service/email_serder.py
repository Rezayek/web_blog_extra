from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.services.user_auth_service import auth_schemas
from app.app_models.db_models  import User
from app.services.user_auth_service import oauth2
import app.config_env as config_env

#configuration used to send verification email
conf = ConnectionConfig(
    MAIL_USERNAME = config_env.settings.mail,
    MAIL_PASSWORD = config_env.settings.mail_password,
    MAIL_FROM = config_env.settings.mail,
    MAIL_PORT = 587,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(email: auth_schemas.EmailSchema, instance: User): 
    token_data = {
        "user_id": instance.id,
        "user_name": instance.user_name
    }
    
    token = oauth2.create_access_token (token_data)
    template = f"""        
         <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            <div style=" align-items: center; justify-content: center; ">
                <h3> Account Verification </h3>
                <br>
                <p>Thanks for choosing MyBlog, please 
                click on the link below to verify your account</p> 
                <br>
                <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                 href="http://127.0.0.1:8000/auth/verification/?token={token}">
                    Verify your email
                <a>
                <br>
                <br>
                <br>
                <p">If you did not register for MyBlog, 
                please kindly ignore this email and nothing will happen. Thanks<p>
            </div>
        </body>
        </html>
    """
    
    message = MessageSchema(
        subject= "Account Verification Email",
        recipients= email.email, 
        body= template,
        subtype= "html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message= message)