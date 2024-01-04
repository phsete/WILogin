from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from selenium_stealth import stealth
from selenium.common.exceptions import NoSuchElementException

USERNAMES = ["YOURUSERNAME1", "YOURUSERNAME2"]
PASSWORDS = ["YOURPASSWORD1", "YOURPASSWORD2"]

start_time = time.time()

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless") # comment out to track progress
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://wurzelimperium.de"

driver.get(url)

screenshot = driver.get_screenshot_as_png()

elapsed = "%s seconds" % (time.time() - start_time)

print("Done in " + elapsed)

server_dropdown = Select(driver.find_element(By.ID, "login_server"))

server_list = [''.join(option.accessible_name.split()).lower() for option in server_dropdown.options] # get all available servers
print(f"Available Servers: {server_list}")

for USERNAME in USERNAMES:
    for PASSWORD in PASSWORDS:
        print(f"Testing with username \"{USERNAME}\" and password \"{PASSWORD}\"")
        for server in server_list:
            server_dropdown.select_by_value(server)

            selected_server = server_dropdown.first_selected_option.accessible_name

            username = driver.find_element(By.ID, "login_user")
            password = driver.find_element(By.ID, "login_pass")
            
            username.clear()
            password.clear()

            username.send_keys(USERNAME)
            password.send_keys(PASSWORD)
            password.send_keys(Keys.ENTER)

            def element_exists(element_id):
                try:
                    element =  driver.find_element(By.ID, element_id)
                    style = element.get_attribute("style")
                    if "display: block;" in style:
                        return True
                    else:
                        return False
                except NoSuchElementException:
                    return False

            while not (login_fail := element_exists("infolayer")) and not (login_success := element_exists("menuUserdata")):
                pass
                #print("waiting for login ...")
                
            if login_fail:
                driver.find_element(By.ID, "infolayer_close").click()

            driver.save_screenshot("loginpage.png")  # change image name
            
            print(f"Tried {selected_server} successfully!")

            if not login_fail and login_success:
                print(f"Found Server! It is {selected_server} with username {USERNAME} and password {PASSWORD}")
                exit(0)
                
        print("No Server responds the given credentials. :-(") # the machine influences your emotions :(