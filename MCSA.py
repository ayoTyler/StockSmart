import os
import sys
import time
import smtplib
from datetime import datetime as dt
from dotenv import load_dotenv
from selenium import webdriver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

STORES = {
    'Tustin': '101',
    'Denver': '181',
    'Miami': '185',
    'Duluth': '065',
    'Marietta': '041',
    'Chicago': '151',
    'Westmont': '025',
    'Indianapolis': '165',
    'Overland Park': '191',
    'Cambridge': '121',
    'Rockville': '085',
    'Parkville': '125',
    'Madison Heights': '055',
    'St. Louis Park': '045',
    'Brentwood': '095',
    'Charlotte': '175',
    'North Jersey': '075',
    'Westbury': '171',
    'Brooklyn': '115',
    'Flushing': '145',
    'Yonkers': '105',
    'Columbus': '141',
    'Mayfield Heights': '051',
    'Sharonville': '071',
    'St. Davids': '061',
    'Houston': '155',
    'Dallas': '131',
    'Fairfax': '081',
}

# Update this with whatever products you want to monitor.
PRODUCTS = {
    'fan': 'https://www.microcenter.com/product/667290/lian-li-uni-fan-reverse-sl-infinity-fluid-dynamic-bearing-120mm-case-fan-white',
    'cpu': 'https://www.microcenter.com/product/687907/amd-ryzen-7-9800x3d-granite-ridge-am5-470ghz-8-core-boxed-processor-heatsink-not-included',
}


def prompt_for_email_details():
    # Prompts the user for email and password securely
    print("Security Disclaimer:\n"
          "Your personal information can only be accessed by a system administrator while the program is running.\n"
          "This information cannot be accessed by outside users and is immediately deleted upon the end of program runtime.\n"
          "This means that you will have to re-enter your information every time the program is ran.\n"
          "\n"
          "Email Information Instructions:\n"
          "Go to myaccount.google.com, search 'App Passwords', and click the respective option.\n"
          "In the 'App name' field enter any title specific to this program.\n"
          "Copy and paste the newly generated password into the appropriate field below:")

    # Set the environment variables
    os.environ["email"] = input("Enter your email: ")
    os.environ["password"] = input("Enter your password: ")


def send_test_email():
    try:
        # Get the environment variables
        email_user = os.getenv("email")
        email_password = os.getenv("password")

        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_user
        msg['Subject'] = 'Test Email Successful'
        msg.attach(MIMEText(
            'This is a test email to confirm that your email login is correctly working alongside SMTP within the Microcenter Stock Python Application.\n\n'
            'You may now let the application run in the background while it actively checks stock of your selected Microcenter product.',
            'plain'))

        # Connect to the email server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, email_user, msg.as_string())

        print(f"[{dt.now()}] Test email sent successfully!")
    except Exception as e:
        print(f"[{dt.now()}] Failed to send test email: {e}")
        print(f"[{dt.now()}] Application will continue without user email")


def prompt_for_product():
    print(f"The following products are enabled: {', '.join(PRODUCTS.keys())}")

    os.environ["selected_product"] = input('Select your desired product: ').strip().lower()

    while not os.getenv("selected_product") or os.getenv("selected_product") not in PRODUCTS:
        print('Invalid product selected')
        os.environ["selected_product"] = input('Select your desired product: ').strip().lower()


# Helper method to generate the list of stores to their IDs if needed.
# Since Micro Center store locations are pretty static,
# we can just run this once and update the mapping.
def get_stores():
    # Set up Chrome options to enable headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Fix potential environment issues

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://www.microcenter.com')

    # Wait for the page to load, adjust as needed (seconds)
    time.sleep(1)

    store_selector_elements = driver.find_elements(By.CSS_SELECTOR,
                                                   '.changeMyStore ul.dropdown-menu li.dropdown-itemLI')
    stores = {}
    for store_element in store_selector_elements:
        store_name = store_element.find_element(By.CLASS_NAME, 'storeName').get_attribute('innerText')
        store_id = store_element.get_attribute('class').split()[-1].split('_')[
            -1]  # e.g., 'store_041' -> ['store', '041']
        stores[store_name] = store_id

    driver.quit()

    return stores


def set_current_store(driver, store_id):
    # Get the main store page URL so you don't overload the product webpage. Selenium limitation
    driver.get("https://www.microcenter.com")

    # Wait for the page to load, adjust as needed (seconds)
    time.sleep(0)

    # Micro Center uses the 'storeSelected' cookie to determine the currently selected store. Default: 131 (Dallas store)
    driver.add_cookie({
        'name': 'storeSelected',
        'value': store_id,
        'domain': '.microcenter.com',
        'path': '/',
        'secure': True,
        'httpOnly': False
    })


def navigate_to_product(driver, product_link):
    driver.get(product_link)

    # Wait for the page to load, adjust as needed (seconds)
    time.sleep(0)


def send_in_stock_email(store, product_name, quantity_in_stock):
    try:
        # Get the environment variables
        email_user = os.getenv("email")
        email_password = os.getenv("password")

        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_user
        msg['Subject'] = 'Your Microcenter Product is Now In Stock'
        msg.attach(
            MIMEText(
                f'{product_name} is in stock at {store}. There are {quantity_in_stock} in stock. Reserve it online or head to the store to get it while supplies last.',
                'plain'
            )
        )

        # Connect to the email server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, email_user, msg.as_string())

        print(f"[{dt.now()}] Email sent successfully!")
    except Exception as e:
        print(f"[{dt.now()}] Failed to send email: {e}")


def check_stock(driver):
    # Micro Center's site uses a DOM element with the class 'inventoryCnt', which also lists the quantity in stock if present.
    # If no such DOM element exists, the product is sold out.
    try:
        inventory_count_element = driver.find_element(By.CLASS_NAME, 'inventoryCnt')
        return inventory_count_element.get_attribute('innerText').split()[0].strip()  # It'll be either 1-24 or 25+.
    except:
        # Selenium throws an exception if no such element can be found. This is expected.
        pass

    # Just to double check, we'll also check their Google Tag Manager event, which uses 'inStock': 'True|False' to indicate its availability.
    # Inventory count is not available that way though, so we'll just consider it 1 or 0 to be simple.
    return str(int("'inStock':'True'" in driver.page_source))


def main():
    prompt_for_product()

    # Load email credentials from the config.env file if possible
    config_path = ".venv/config.env"
    load_dotenv(config_path)

    if not os.getenv("email") or not os.getenv("password"):
        prompt_for_email_details()

    # Confirm whether email credentials were entered
    if not os.getenv("email") or not os.getenv("password"):
        raise Exception("Email credentials not found")

    if os.getenv("enable_test_email") and os.getenv("enable_test_email").strip().lower() == 'true':
        send_test_email()
    else:
        print(f'[{dt.now()}] Skipping test email')

    # Set up Chrome options to enable headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Fix potential environment issues

    stores_to_check = ['Dallas', 'Houston']  # Update this with the stores you want to check. Reference the map at the start.
    while True:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        for store in stores_to_check:
            set_current_store(driver, STORES[store])
            navigate_to_product(driver, PRODUCTS[os.getenv('selected_product')])
            product_name = driver.find_element(By.CLASS_NAME, 'product-header').get_attribute('innerText')
            quantity_in_stock = check_stock(driver)

            if quantity_in_stock != '0':
                print(f'[{dt.now()}] {product_name} is in stock at {store}! Available quantity: {quantity_in_stock}')
                send_in_stock_email(store, product_name, quantity_in_stock)
                driver.quit()  # Close the browser
                sys.exit()
            else:
                print(f'[{dt.now()}] {product_name} is out of stock at {store}!')

            time.sleep(10)  # An arbitrary delay between checking stores to hopefully avoid being flagged as a bot.
        driver.quit()  # Use a new driver and close it afterwards for every loop to mitigate memory leaks.
        time.sleep(
            300)  # Change the number to check stock sooner/faster (seconds). Default: checks stock every ~5 minutes


if __name__ == '__main__':
    main()
