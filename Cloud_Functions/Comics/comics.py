from datetime import datetime
import requests
import traceback
import re
from threading import Thread
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import base64
from bs4 import BeautifulSoup, Tag
import urllib3

# This next statement is to supress 'InsecureRequestWarning' messages
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GOCOMICS = 'gocomics'
COMICSKINGDOM = 'comicskingdom'
DILBERT = 'dilbert'
FARSIDE = 'farside'

GOCOMICS_URL = 'https://www.gocomics.com/'
GOCOMICS_REGEX = r'(\S+item-comic-image.+data-srcset=\")(\S+)'
COMICSKINGDOM_URL = 'https://www.comicskingdom.com/'
COMICSKINGDOM_REGEX = r'(og:image\"\s+content=\")([^\"]+)'
DILBERT_URL = 'https://dilbert.com/'
DILBERT_REGEX = r'(data-image=\")([^\"]+)'
FARSIDE_URL = 'https://www.thefarside.com'
FARSIDE_IMAGE_REGEX = r'(.+data-src=\")([^\"]+)'
FARSIDE_CAPTION_REGEX = r'(.+<figcaption class=\"figure-caption\">\s+)([^\n]+)'

EMAIL_SSL_PORT = 465  # For SSL

COMICS = [
    {"name": "luann", "source": GOCOMICS},
    {"name": "9chickweedlane", "source": GOCOMICS},
    {"name": "dilbert", "source": DILBERT},
    {"name": "dilbert-classics", "source": GOCOMICS},
    {"name": "zits", "source": COMICSKINGDOM},
    {"name": "baby-blues", "source": COMICSKINGDOM},
    {"name": "wallace-the-brave", "source": GOCOMICS},
    {"name": "frazz", "source": GOCOMICS},
    {"name": "bizarro", "source": COMICSKINGDOM},
    {"name": "theargylesweater", "source": GOCOMICS},
    {"name": "nonsequitur", "source": GOCOMICS},
    {"name": "calvinandhobbes", "source": GOCOMICS},
    {"name": "bloomcounty", "source": GOCOMICS},
    {"name": "outland", "source": GOCOMICS},
    {"name": "getfuzzy", "source": GOCOMICS},
    {"name": "funky-winkerbean", "source": COMICSKINGDOM},
    {"name": "theflyingmccoys", "source": GOCOMICS},
    {"name": "closetohome", "source": GOCOMICS},
    {"name": "boundandgagged", "source": GOCOMICS},
    {"name": "doonesbury", "source": GOCOMICS},
    {"name": "academiawaltz", "source": GOCOMICS},
    {"name": "prince-valiant", "source": COMICSKINGDOM},
    {"name": "farside", "source": FARSIDE}
]

def get_image_url(comic_url, comic_regex, verify=True):
    # This assumes the regex returns the desired image url in group(2) of the regex match
    image_url = None
    # verify=False is to eliminate the error, requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
    response = requests.get(comic_url, verify=verify)
    if response.status_code == 200:
        results = response.content.decode('utf-8')
        regex_match = re.search(comic_regex, results)
        if regex_match is not None and len(regex_match.groups()) >= 2:
            image_url = regex_match.group(2)
    else:
        print('%s error calling %s: %s' % (response.status_code, comic_url, response.content))
    return image_url

def get_farside(comic_url):
    image = None
    image_url = None
    caption = None
    response = requests.get(comic_url, verify=False)
    if response.status_code == 200:
        html = response.content.decode('utf-8')
        # 'features' is specified to eliminate the
        # 'GuessedAtParserWarning: No parser was explicitly specified' warning
        soup = BeautifulSoup(html, features="lxml")
        results = soup.find_all(class_='tfs-comic__image')
        todays_comic = results[0]
        children = todays_comic.children
        for child in children:
            if type(child) == Tag:
                image_url = child.attrs.get('data-src')
                break

        next = todays_comic.next_sibling
        while next is not None:
            if type(next) == Tag:
                attrs = next.attrs
                class_ = attrs.get('class')
                if class_ is not None:
                    if 'tfs-comic__caption' in class_:
                        caption = next.text
                        break
                    elif 'tfs-comic__image' in class_ or 'tfs-content__1col' in class_:
                        break
            else:
                next = next.next_sibling

        if image_url is not None:
            headers = {'referer': 'https://www.thefarside.com/'}
            response = requests.get(image_url, headers=headers, verify=False)
            if response.status_code == 200:
                base64_bytes = base64.b64encode(response.content)
                base64_string = base64_bytes.decode('utf-8')
                image = "data:image/jpeg;base64,%s" % base64_string

    return image, caption

def format_email(results, date_string):
    text_opening = 'Hi,\n\nHere are your daily comics for %s:\n' % date_string
    text_closing = '\n\n'
    html_opening = '<html>\n\t<head>\n\t\t<title>Your Daily Comics</title>'
    html_opening += '\n\t\t<style>\n\t\t\tbody,html {background-color: #6b7b84; height: 100%; margin-top: 30px; margin-bottom: 30px; margin-left: 30px; margin-right: 30px; font-size: 125%;}'
    html_opening += '\n\t\t\t.mono {font-family: "Lucida Console", "Courier New", monospace;}'
    html_opening += '\n\t\t\tp.pad {padding-bottom: 50px; font-family: "Lucida Console", "Courier New", monospace;}'
    html_opening += '\n\t\t\tp.caption {text-align: center; font-family: "Lucida Console", "Courier New", monospace;}'
    html_opening += '\n\t\t\th1 {color: black;}'
    html_opening += '\n\t\t\th2 {color: black; padding-top: 20px;}'
    html_opening += '\n\t\t\ta {color: black;}'
    html_opening += '\n\t\t\timg {max-width: 100%; height: auto; box-shadow: 5px 10px 18px #111111;}\n\t\t</style>'
    html_opening += '\n\t</head>\n\t<body>\n\t\t<basefont face = "courier">'
    html_opening += '\n\t\t<h1 class="mono">%s</h1>' % date_string
    html_closing = '\n\t\t<p class="pad">\n\t</body>\n</html>'

    text = text_opening
    html = html_opening
    for entry in results:
        if entry.get('image_url') is not None:
            text += '\n\t- %s: %s' % (entry['name'], entry['image_url'])
        else:
            text += '\n\t- %s: No comic for today.' % entry['name']
        html += '\n\t\t<h2 class="mono">%s</h2>' % entry['name']
        if entry.get('image_url') is not None:
            html += '\n\t\t\t<a href="%s">' % entry['comics_url']
            html += '\n\t\t\t<img src="%s" alt="%s">' % (entry['image_url'], entry['name'])
        elif entry['name'] == 'farside' and entry['image'] is not None:
            html += '\n\t\t\t<a href="%s">' % FARSIDE_URL
            html += '\n\t\t\t<img src="%s" alt="%s">' % (entry['image'], entry['name'])
            if entry['caption'] is not None:
                html += '\n\t\t\t<p class="caption"><b>%s</b>' % entry['caption']
        else:
            html += '\n\t\t\t<p class="pad"><b>No comic for today.</b>'
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
    with smtplib.SMTP_SSL("smtp.gmail.com", EMAIL_SSL_PORT, context=context) as server:
        server.login(GMAIL_ID, GMAIL_PW)
        server.sendmail(
            GMAIL_ID, TARGET_EMAIL, message.as_string()
        )
        server.close()
        print("Email sent")
    return

def process_comic(comic, today_date_string, results):
    image_url = None
    image = None
    caption = None
    if comic['source'] == GOCOMICS:
        url = "%s%s/%s" % (GOCOMICS_URL, comic['name'], today_date_string)
        image_url = get_image_url(url, GOCOMICS_REGEX)
    elif comic['source'] == COMICSKINGDOM:
        url = "%s%s" % (COMICSKINGDOM_URL, comic['name'])
        image_url = get_image_url(url, COMICSKINGDOM_REGEX, verify=False)
    elif comic['source'] == DILBERT:
        url = DILBERT_URL
        image_url = get_image_url(DILBERT_URL, DILBERT_REGEX)
    elif comic['source'] == FARSIDE:
        url = FARSIDE_URL
        image_url = None
        image, caption = get_farside(FARSIDE_URL)
    else:
        raise Exception('Invalid comic type.')

    if image_url is not None:
        new_entry = {'name': comic['name'], 'comics_url': url, 'image_url': image_url}
        print(new_entry)
    elif comic['source'] == FARSIDE and image is not None:
        new_entry = {'name': comic['name'],
                     'comics_url': url,
                     'image_url': image_url,
                     'image': image,
                     'caption': caption}
    else:
        print('Comic %s not found for %s.' % (comic['name'], today_date_string))
        new_entry = {'name': comic['name'], 'comics_url': url, 'image_url': image_url}
    results.append(new_entry)
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

        now = datetime.now()
        today_date_string = now.strftime("%Y/%m/%d")
        processing_results = []

        threads = []
        for comic in COMICS:
            th = Thread(target=process_comic,
                        args=(comic, today_date_string, processing_results))
            th.start()
            threads.append(th)

        for th in threads:
            th.join()

        def sort_function(element):
            indices = [i for i, c in enumerate(COMICS) if c['name'] == element['name']]
            return (indices[0])
        processing_results.sort(key=sort_function)

        print(processing_results)

        email_text, email_html = format_email(processing_results, today_date_string)
        send_email(email_text, email_html, GMAIL_ID, GMAIL_PW, TARGET_EMAIL)

        return {"statusCode": 200}

    except Exception as e:
        print('Error: ' + str(e))
        traceback.print_exc()
        return {"statusCode": 500, "body": str(e)}

if __name__ == '__main__':
    print("Python %s" % sys.version)
    input = {"GMAIL_ID": os.environ['GMAIL_ID'],
             "GMAIL_PW": os.environ['GMAIL_PW'],
             "TARGET_EMAIL": os.environ['TARGET_EMAIL']}
    main(input)