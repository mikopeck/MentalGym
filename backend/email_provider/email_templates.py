# email_templates.py

Registration = {
    "from": "Ascendance·☁️ <misa@ascendance.cloud>",
    "subject": "Welcome to Ascendance·☁️",
    "bcc":"mikopeck@gmail.com",
    "html": """
    <html>
        <head>
            <style>
                .email-container {
                    font-family: 'Arial', sans-serif;
                    color: #f0f8ff;
                    line-height: 1.6;
                    background-color: #0e0c14;
                }
                .header {
                    background-color: #4a148c;
                    padding: 20px;
                    text-align: center;
                    border-bottom: 3px solid #6a34b9;
                }
                .content {
                    padding: 20px;
                }
                .footer {
                    background-color: #4a148c;
                    padding: 10px;
                    text-align: center;
                    border-top: 3px solid #6a34b9;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    color: f0f8ff;
                    text-decoration: none;
                    border-radius: 5px;
                    border: 1px solid #6a34b9;
                }
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Welcome to Ascendance·☁️</h1>
                </div>
                <div class="content">
                    <p>Dear Ascendant,</p>
                    <p>
                        You're on the brink of an incredible journey! We're thrilled to have you aboard Ascendance.cloud, where your potential is limitless, and every challenge is a new opportunity for growth.
                    </p>
                    <p>
                        Please confirm your email address to start ascending to new heights:
                    </p>
                    <a href="{{ confirmation_link }}" class="button">Confirm Email</a>
                    <p>
                        If you have any questions or need assistance, our mentorship team is here for you every step of the way.
                    </p>
                    <p>
                        Embrace your journey,<br>
                        The Ascendance.cloud Team
                    </p>
                </div>
                <div class="footer">
                    <p>
                        Stay connected:<br>
                        <a href="https://twitter.com/AscendanceCloud">Twitter/X</a> | <a href="https://discord.gg/HWaYnvTp34">Discord</a>
                    </p>
                </div>
            </div>
        </body>
    </html>
    """,
    "text": """Welcome to Ascendance.cloud

Dear Ascendant,

You're on the brink of an incredible journey! We're thrilled to have you aboard Ascendance.cloud, where your potential is limitless, and every challenge is a new opportunity for growth.

Please confirm your email address to start ascending to new heights:
[Confirm Email] {{ confirmation_link }}

If you have any questions or need assistance, our mentorship team is here for you every step of the way.

Embrace your journey,
The Ascendance.cloud Team"""
}
