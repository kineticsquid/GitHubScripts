import subprocess
from datetime import datetime
import traceback
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import urllib3

# This next statement is to supress 'InsecureRequestWarning' messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def format_email(results, title):
    text_opening = '%s:\n' % title
    text_closing = '\n\n'
    html_opening = '<html>\n\t<head>\n\t\t<title>%s</title>' % title
    html_opening += '\n\t\t<style>\n\t\t\tbody,html {background-color: #6b7b84; height: 100%; margin-top: 30px; margin-bottom: 30px; margin-left: 30px; margin-right: 30px; font-size: 125%;}'
    html_opening += '\n\t\t\t.mono {font-family: "Lucida Console", "Courier New", monospace;}'
    html_opening += '\n\t\t\tp.pad {padding-bottom: 50px; font-family: "Lucida Console", "Courier New", monospace;}'
    html_opening += '\n\t\t\tp.caption {text-align: center; font-family: "Lucida Console", "Courier New", monospace;}'
    html_opening += '\n\t\t\th1 {color: black;}'
    html_opening += '\n\t\t\th2 {color: black; padding-top: 20px;}'
    html_opening += '\n\t\t\ta {color: black;}'
    html_opening += '\n\t\t\timg {max-width: 100%; height: auto; box-shadow: 5px 10px 18px #111111;}\n\t\t</style>'
    html_opening += '\n\t</head>\n\t<body>\n\t\t<basefont face = "courier">'
    html_opening += '\n\t\t<h1 class="mono">%s</h1>' % title
    html_closing = '\n\t\t<p class="pad">\n\t</body>\n</html>'

    text = text_opening
    html = html_opening
    for entry in results:
        html += '\n\t\t\t<pre>\n'
        html += entry
        html += '\n\t\t\t</pre>'
    text += text_closing
    html += html_closing

    return text, html

def send_email(text, html, title, email, pw, target_email, ssl_port):
    message = MIMEMultipart("alternative")
    message["Subject"] = title
    message["From"] = email
    message["To"] = target_email
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", ssl_port, context=context) as server:
        server.login(email, pw)
        server.sendmail(
            email, target_email, message.as_string()
        )
        server.close()
        print("Email sent")
    return

def process_command(command):
    try:
        # commands needs to be an array. e.g. ['logon', '...']
        output_bytes = subprocess.check_output([command], shell=True)
        output = output_bytes.decode('utf-8')
    except Exception as e:
        output = str(e)
    return output

def main(cloud_function_input):
    try:
        GMAIL_ID = cloud_function_input.get('GMAIL_ID')
        GMAIL_PW = cloud_function_input.get('GMAIL_PW')
        TARGET_EMAIL = cloud_function_input.get('TARGET_EMAIL')
        EMAIL_SSL_PORT = cloud_function_input.get('EMAIL_SSL_PORT')
        COMMANDS = cloud_function_input.get('COMMANDS')
        TITLE = cloud_function_input.get('TITLE')
        TEXT = cloud_function_input.get('TEXT')

        if TEXT is not None:
            processing_results = [TEXT]
        else:
            processing_results = []
        if COMMANDS is not None:
            for command in COMMANDS:
                output = process_command(command)
                processing_results.append(output)
        print(processing_results)

        email_text, email_html = format_email(processing_results, TITLE)
        send_email(email_text, email_html, TITLE, GMAIL_ID, GMAIL_PW, TARGET_EMAIL, EMAIL_SSL_PORT)

        return {"statusCode": 200}

    except Exception as e:
        print('Error: ' + str(e))
        traceback.print_exc()
        return {"statusCode": 500, "body": str(e)}

if __name__ == '__main__':
    print("Python %s" % sys.version)
    input = {"GMAIL_ID": os.environ['GMAIL_ID'],
             "GMAIL_PW": os.environ['GMAIL_PW'],
             "EMAIL_SSL_PORT": os.environ['EMAIL_SSL_PORT'],
             "TARGET_EMAIL": os.environ['TARGET_EMAIL'],
             "TITLE": os.environ['TITLE'],
             "COMMANDS": ['date', 'printenv']}
    main(input)
