def verification_email(name: str, verification_link: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif;">

        <h2>Welcome, {name}! 👋</h2>

        <p>
            Thank you for creating an account.
        </p>

        <p>
            Please verify your email address by clicking the link below:
        </p>

        <p>
            <a href="{verification_link}">
                Verify Email
            </a>
        </p>

        <p>
            Or copy and paste this URL into your browser:
        </p>

        <p>{verification_link}</p>

        <hr>

        <p>
            This verification link will expire in 15 minutes.
        </p>

        <p>
            If you didn't create this account, you can safely ignore this email.
        </p>

    </body>
    </html>
    """

def welcome_email(name: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif;">

        <h2>Welcome to URL Shortener, {name}! 🎉</h2>

        <p>
            Your email has been successfully verified.
        </p>

        <p>
            Your account is now active and you can start creating short URLs.
        </p>

        <p>
            Thank you for joining us!
        </p>

    </body>
    </html>
    """

def password_reset_email(name: str, reset_link: str):
    return f"""
    <html>
        <body>
            <h2>Hello {name},</h2>

            <p>We received a request to reset your password.</p>

            <p>
                <a href="{reset_link}">
                    Reset Password
                </a>
            </p>

            <p>This link expires in 15 minutes.</p>

            <p>If you didn't request this, you can safely ignore this email.</p>
        </body>
    </html>
    """

def password_reset_success_email(name: str):
    return f"""
    <html>
        <body>
            <h2>Hello {name},</h2>

            <p>Your password has been changed successfully.</p>

            <p>If you made this change, no further action is required.</p>

            <p><strong>If you did NOT change your password, please reset it immediately and contact support.</strong></p>

            <br>

            <p>Thank you.</p>
        </body>
    </html>
    """

def account_deleted_email(name: str):
    pass

def url_expired_email(name: str, short_code: str):
    pass