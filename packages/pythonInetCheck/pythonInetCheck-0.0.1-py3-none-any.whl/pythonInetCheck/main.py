import notify2
import requests
import time
from config import *


def main_loop():
    inet_status = False
    while True:
        status = []
        for site, url in WEB_SITES.items():
            validated = check_site(url)
            status.append(validated)
            if validated:
                inet_status = True
                notify("up", site)
                break
        s = False
        for i in status:
            s = s or i
        if not s:
            notify("down")
            inet_status = False
        if not inet_status:
            time.sleep(60)
        else:
            time.sleep(300)


def check_site(site: str):
    try:
        req = requests.get(site)
    except requests.ReadTimeout:
        return False
    if req.ok:
        return True
    return False


def notify(inet_status: str, site: str = None):
    if site is None:
        site = "all"
    message = f"the inet status is {inet_status} on account of {site}"
    notify2.init("Test")
    notice = notify2.Notification("inet status", message)
    notice.show()


if __name__ == "__main__":
    main_loop()
