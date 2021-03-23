import requests
import re
import base64

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
FARSIDE_REGEX = r'(.+data-src=\")([^\"]+)'

COMICS = [
    {"name": "luann", "source": GOCOMICS},
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
    {"name": "doonesbury", "source": GOCOMICS},
    {"name": "theflyingmccoys", "source": GOCOMICS},
    {"name": "closetohome", "source": GOCOMICS},
    {"name": "boundandgagged", "source": GOCOMICS},
    {"name": "doonesbury", "source": GOCOMICS},
    {"name": "academiawaltz", "source": GOCOMICS},
    {"name": "prince-valiant", "source": COMICSKINGDOM},
    {"name": "farside", "source": FARSIDE}
]

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
#            'referer': 'https://www.thefarside.com/',
#            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'}

headers = {'referer': 'https://www.thefarside.com/'}
response = requests.get(FARSIDE_URL)
if response.status_code == 200:
    results = response.content.decode('utf-8')
    regex_match = re.search(FARSIDE_REGEX, results)
    if regex_match is not None and len(regex_match.groups()) >= 2:
        image_url = regex_match.group(2)
        response = requests.get(image_url, headers=headers)
        print(response.status_code)
        base64_bytes = base64.b64encode(response.content)
        base64_string = base64_bytes.decode('utf-8')

        html = '<html>\n\t<head>\n\t\t<title>Your Daily Comics</title>\n\t</head>\n\t<body>'
        html += '<div><img src="data:image/jpeg;base64,%s" alt="an image" />' % base64_string
        html += '\n\t</body>\n</tml>'
        f = open('base64.html', 'w')
        f.write(html)
        f.close()
        print(html)
