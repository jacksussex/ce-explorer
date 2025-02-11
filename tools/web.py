from urllib.request import urlopen
from urllib.error import *


def ping_website(url: str) -> bool:
    service_available = True
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("HTTP error - likely servive down:", e)
        service_available = False
    except URLError as e:
        print("URL error - likely URL is malformed", e)
        service_available = False
    return service_available
