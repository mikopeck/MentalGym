# resend_api.py

import resend

def send_registration_email(email, template, confirmation_link):
    custom_email_html = fill_info(template, confirmation_link)
    email_data = {
        "to": email,
        "subject": template['subject'],
        "html": custom_email_html,
        "from": template['from']
    }
    email_id = resend.Emails.send(email_data)
    print(email, email_id)

def fill_info(template, confirmation_link):
    custom_email = template['html'].replace("{{ confirmation_link }}", confirmation_link)
    return custom_email
