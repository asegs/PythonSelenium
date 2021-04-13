# Selenium 3.14+ doesn't enable certificate checking
import os
from selenium import webdriver
import urllib3
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

mac_safari = {
    'platform': "Mac OS X 10.13",
    'browserName': "safari",
    'version': "11.1",
    'build': "Onboarding Sample App - Python",
    'name': "2-user-site",
}

mac_chrome = {
    'platform': "Mac OS X 10.13",
    'browserName': "chrome",
    'version': "89",
    'build': "Onboarding Sample App - Python",
    'name': "2-user-site",
}

windows_ie = {
    'platform': "Windows 10",
    'browserName': "internet explorer",
    'version': "11",
    'build': "Onboarding Sample App - Python",
    'name': "2-user-site",
}

windows_firefox = {
    'platform': "Windows 10",
    'browserName': "firefox",
    'version': "87",
    'build': "Onboarding Sample App - Python",
    'name': "2-user-site",
}

linux_chrome = {
    'platform': "Linux",
    'browserName': "firefox",
    'version': "45",
    'build': "Onboarding Sample App - Python",
    'name': "2-user-site",
}

caps = [mac_safari, mac_chrome, windows_ie, windows_firefox, linux_chrome]

username = "arctic"
access_key = "PRIVATE_KEY"


def get_faculty(cap):
    driver = webdriver.Remote(
        command_executor='https://{}:{}@ondemand.saucelabs.com:443/wd/hub'.format(username, access_key),
        desired_capabilities=cap)

    driver.get("https://www.rit.edu/computing/faculty")
    overlay_div = driver.find_element_by_id("overlay-body")
    """asserts section"""
    all_passed = True
    try:
        assert overlay_div.get_attribute("class") == "position-fixed"
    except AssertionError:
        all_passed = False
        print("Overlay div not found!")
    try:
        assert "Faculty" in driver.title
    except AssertionError:
        all_passed = False
        print("Unable to load the RIT faculty page!")

    if all_passed:
        print("SUCCESS!")
    driver.quit()


threads = []

for i in range(0, 5):
    t = Thread(target=get_faculty, args=(caps[i],))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()
