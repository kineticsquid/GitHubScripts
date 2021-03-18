from datetime import datetime
import requests
import traceback
import re
from threading import Thread
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

GOCOMICS_URL = 'https://www.gocomics.com/'
IMAGE_URL_REGEX = r'(\S+item-comic-image.+data-srcset=\")(\S+)'
SSL_PORT = 465  # For SSL

def process_comic(comic_name, today_date_string, processing_results):
    url = "%s%s/%s" % (GOCOMICS_URL, comic_name, today_date_string)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.content.decode('utf-8')
        regex_match = re.search(IMAGE_URL_REGEX, results)
        if regex_match is not None:
            image_url = regex_match.group(2)
            if image_url is not None:
                new_entry = {'name': comic_name, 'image_url': image_url, 'gocomics_url': url}
                processing_results.append(new_entry)
                print(new_entry)
            else:
                print('Comic %s not found for %s.' % (comic_name, today_date_string))
        else:
            print('Comic %s not found for %s.' % (comic_name, today_date_string))
    else:
        print('%s error calling gocomics.com: %s' % (response.status_code, response.content))
    return

def format_email(results, date_string):
    text_opening = 'Hi,\n\nHere are your daily comics for %s:\n' % date_string
    text_closing = '\n\n'
    html_opening = '<html>\n\t<head>\n\t\t<title>Your Daily Comics</title>'
    html_opening += '\n\t\t<style>\n\t\t\tbody,html {background-color: #6b7b84; height: 100%; margin-top: 30px; margin-bottom: 30px; margin-left: 30px; margin-right: 30px; font-size: 125%;}'
    html_opening += '\n\t\t\t.mono {font-family: "Lucida Console", "Courier New", monospace;}'
    html_opening += '\n\t\t\tp.pad {padding-bottom: 50px;}'
    html_opening += '\n\t\t\th1,h2,h3 {color: black;}'
    html_opening += '\n\t\t\timg {max-width: 100%; height: auto; box-shadow: 5px 10px 18px #111111;}\n\t\t</style>'
    html_opening += '\n\t</head>\n\t<body>\n\t\t<basefont face = "courier">'
    html_opening += '\n\t\t<h1 class="mono">%s</h1>' % date_string
    html_closing = '\n\t\t<p class="pad">\n\t</body>\n</html>'

    text = text_opening
    html = html_opening
    for entry in results:
        text += '\n\t- %s: %s' % (entry['name'], entry['image_url'])
        html += '\n\t\t<h2 class="mono">%s</h2>' % entry['name']
        html += '\n\t\t\t<a href="%s">' % entry['gocomics_url']
        html += '\n\t\t\t<img src="%s">' % entry['image_url']
        html += '</a>'
    text += text_closing
    html += html_closing

    return text, html

def send_email(text, html, GMAIL_ID, GMAIL_PW, TARGET_EMAIL):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Daily Comics"
    message["From"] = GMAIL_ID
    message["To"] = TARGET_EMAIL
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", SSL_PORT, context=context) as server:
        server.login(GMAIL_ID, GMAIL_PW)
        server.sendmail(
            GMAIL_ID, TARGET_EMAIL, message.as_string()
        )
        server.close()
    return

def main(cloud_function_input):
    try:
        GMAIL_ID = cloud_function_input.get('GMAIL_ID')
        if GMAIL_ID is None:
            raise Exception("Error no GMAIL_ID parameter defined.")
        GMAIL_PW = cloud_function_input.get('GMAIL_PW')
        if GMAIL_PW is None:
            raise Exception("Error no GMAIL_PW parameter defined.")
        TARGET_EMAIL = cloud_function_input.get('TARGET_EMAIL')
        if TARGET_EMAIL is None:
            raise Exception("Error no TARGET_EMAIL parameter defined.")
        COMICS = cloud_function_input.get('COMICS')
        if COMICS is None:
            raise Exception("Error no COMICS parameter defined.")
        else:
            COMICS = json.loads(COMICS)

        now = datetime.now()
        today_date_string = now.strftime("%Y/%m/%d")
        processing_results = []
        threads = []
        for comic_name in COMICS:
            th = Thread(target=process_comic,
                        args=(comic_name, today_date_string, processing_results))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()

        def sort_function(i):
            return (COMICS.index(i['name']))

        processing_results.sort(key=sort_function)

        print(processing_results)

        email_text, email_html = format_email(processing_results, today_date_string)
        send_email(email_text, email_html, GMAIL_ID, GMAIL_PW, TARGET_EMAIL)

        return {"statusCode": 200}

    except Exception as e:
        print('Error: ' + str(e))
        traceback.print_exc()

if __name__ == '__main__':
    input = {"GMAIL_ID": os.environ['GMAIL_ID'],
             "GMAIL_PW": os.environ['GMAIL_PW'],
             "TARGET_EMAIL": os.environ['TARGET_EMAIL'],
             "COMICS": os.environ['COMICS']}
    main(input)