# email_templates.py

Registration = {
    "from": "Ascendance·☁️ <misa@ascendance.cloud>",
    "subject": "Welcome to Ascendance·☁️",
    "html": """
    <html>
        <head>
            <style>
                .email-container {
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    line-height: 1.6;
                }
                .header {
                    background-color: #f4f4f4;
                    padding: 20px;
                    text-align: center;
                    border-bottom: 3px solid #e2e2e2;
                }
                .content {
                    padding: 20px;
                }
                .footer {
                    background-color: #f4f4f4;
                    padding: 10px;
                    text-align: center;
                    border-top: 3px solid #e2e2e2;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Welcome to Ascendance.cloud</h1>
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
                        <a href="#">Facebook</a> | <a href="#">Twitter</a> | <a href="#">Instagram</a>
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
