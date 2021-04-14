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

    print("Thread started on:\nOS: " + cap['platform'] + "\nBrowser: " + cap['browserName'] + "\n\n")

    driver.get("https://www.rit.edu/computing/faculty")

    """asserts section"""
    all_passed = True
    try:
        overlay_div = driver.find_element_by_id("overlay-body")
        assert overlay_div.get_attribute("class") == "position-fixed"
    except AssertionError:
        all_passed = False
        print("Overlay div not found!")
    try:
        assert "Faculty" in driver.title
    except AssertionError:
        all_passed = False
        print("Unable to load the RIT faculty page!")
    try:
        find_now_button = driver.find_element_by_id("edit-submit-directory--2")
        assert find_now_button.get_attribute("value") == "Find Now"
    except AssertionError:
        all_passed = False
        print("Search button not found")

    try:
        filter_by = driver.find_element_by_id("directory-select")
        assert filter_by.get_attribute("class") == "form-select"
    except AssertionError:
        all_passed = False
        print("Filter by dropdown not found")
    try:
        filter_by = driver.find_element_by_id("directory-select")
        options = filter_by.find_elements_by_xpath("*")
        children = []
        expected_children = ["All", "Computer Science, Dept. of", "Computing and Information Sciences Ph.D. Program",
                             "Computing Security, Dept. of", "Information, School of",
                             "Interactive Games and Media, School of", "Software Engineering, Dept. of"]
        for o in options:
            children.append(o.get_attribute("innerHTML"))
        assert children == expected_children
    except AssertionError:
        all_passed = False
        print("Proper children not found")
    if all_passed:
        print("SUCCESS!")
    else:
        raise Exception("Webpage missing key elements")
    driver.quit()


threads = []

for i in range(0, 5):
    t = Thread(target=get_faculty, args=(caps[i],))
    threads.append(t)
    t.start()
