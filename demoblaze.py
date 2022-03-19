import datetime
import random
from time import sleep
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

fake = Faker(locale='en_US')

s = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service = s)



# ------------------ DEMOBLAZE DATA ------------------------------
app = 'DEMOBLAZE'
base_url = 'https://www.demoblaze.com/index.html'
product_url = 'https://www.demoblaze.com/prod.html?idp_='
home_page_title = "STORE"
full_name = f'{fake.first_name()} {fake.last_name()}'
credit_card_number = fake.credit_card_number()
username = full_name.replace(' ','').lower()
password = fake.password()
# all_products = ['Samsung galaxy s6', 'Nokia lumia 1520', 'Nexus 6',
#                 'Samsung galaxy s7', 'Iphone 6 32gb', 'Sony xperia z5',
#                 'HTC One M9', 'Sony vaio i5', 'Sony vaio i7',
#                 'Apple monitor 24', 'MacBook air', 'Dell i7 8gb',
#                 '2017 Dell 15.6 Inch', 'ASUS Full HD', 'MacBook Pro']

random_ids = random.sample(range(1, 15), 3)
product_list = []
hr = '--------~*~----------------~*~----------\n'
# -------------------------------------------------


def setUp():
    driver.maximize_window()  # open web browser and maximize the window
    driver.implicitly_wait(30)  # wait for up to 30 sec for the browser response
    driver.get(base_url)  # navigate to app website

    # check the correct URL and the correct title
    if driver.current_url == base_url and driver.title == home_page_title:
        assert driver.current_url == base_url
        assert driver.title == home_page_title
        print(f'{hr}Launch {app} Website\nURL: {driver.current_url}\nPage title: {driver.title}')
        # breakpoint()
    else:
        print(f'{hr}>>>> We are NOT on {app} Home Page. Check your code.')
        print(f'{hr}Expected URL: {base_url} \nActual URL: {driver.current_url}')
        print(f'{hr}Expected Page Title: {home_page_title} \nActual Page Title: {driver.title}')
        tearDown()


def tearDown():  # function to end the session
    if driver is not None:
        print(f'{hr}Test Completed at: {datetime.datetime.now()}')
        sleep(0.25)
        driver.close()
        driver.quit()


def checkout_cart():
    print('--------------------~* ADD ITEMS TO SHOPPING CART *~---------------------')
    print(random_ids)
    total = 0
    if driver.current_url == base_url:
        # add items to cart
        for i in random_ids:
            driver.get(f'{product_url}{i}')
            sleep(2)
            assert driver.find_element(By.CLASS_NAME, 'name').is_displayed()
            product_name = driver.find_element(By.CLASS_NAME, 'name').text
            product_list.append(product_name)
            price_tag = driver.find_element(By.CLASS_NAME, 'price-container').text
            item_price = int(''.join(filter(str.isdigit, price_tag)))   # capture numerical value only
            total += item_price
            print(f'{hr}Go to: {product_name} page, Product ID: {i}')
            driver.find_element(By.LINK_TEXT, 'Add to cart').click()
            sleep(0.5)
            driver.switch_to.alert.accept()
            print(f'{product_name} is added to Shopping Cart, item price: {item_price}')
            sleep(0.25)
            driver.find_element(By.ID, 'nava').click()
            sleep(0.25)

        print(f'{hr}Product List: {product_list}')
        print(f'Cart total: {total}')

        # go to cart
        driver.find_element(By.ID, 'cartur').click()
        print(f'{hr}Go to cart')

        sleep(0.25)
        # validate items in the list
        for p in product_list:
            item_in_cart = driver.find_element(By.XPATH, f'//td[contains(.,"{p}")]').is_displayed()
            assert item_in_cart
            print(f'{hr}Success! {p} is in Shopping Cart: {item_in_cart}')
            sleep(0.25)

        # validate cart total
        cart_total = int(driver.find_element(By.ID, 'totalp').text)
        print(f'{hr}Validate Cart Total:\nExpected cart total: {total}, Actual cart total: {cart_total} ')
        assert cart_total == total

        #driver.find_element(By.LINK_TEXT, 'Delete').click()
        # delete second item from the cart
        deleted_item_price = driver.find_element(By.XPATH, f'//tr[contains(.,"{product_list[1]}")]/td[3]').text
        driver.find_element(By.XPATH, f"//td[contains(., '{product_list[1]}')]/../td/a[contains(text(),'Delete')]").click()
        print(f'{hr}Now deleting {product_list[1]} from Shopping Cart')
        sleep(0.25)
        print(f'{hr}{product_list[1]} is deleted!')

        sleep(2)
        total = total - int(deleted_item_price)
        new_cart_total = int(driver.find_element(By.ID, 'totalp').text)
        assert new_cart_total == total
        print(f'Deleted Item Price: {deleted_item_price}, Cart total updated: {total}')
        print(f'New Cart total confirmed: {new_cart_total}\nContinue to Place Order')

        sleep(0.5)

        # checkout cart
        driver.find_element(By.XPATH, '//button[contains(text(),"Place Order")]').click()
        sleep(0.5)
        assert driver.find_element(By.ID, 'orderModalLabel').is_displayed()
        order_total = driver.find_element(By.ID, 'totalm').text
        order_total = int(''.join(filter(str.isdigit, order_total)))  # capture numerical value only
        print(f'{hr}Order total: {order_total}')
        assert order_total == new_cart_total

        sleep(0.25)
        driver.find_element(By.ID, 'name').send_keys(full_name)
        sleep(0.5)
        driver.find_element(By.ID, 'country').send_keys('Canada')
        sleep(0.5)
        driver.find_element(By.ID, 'city').send_keys(fake.city())
        sleep(0.5)
        driver.find_element(By.ID, 'card').send_keys(credit_card_number)
        sleep(0.5)
        driver.find_element(By.ID, 'month').send_keys(12)
        sleep(0.5)
        driver.find_element(By.ID, 'year').send_keys(2029)
        sleep(0.5)
        driver.find_element(By.XPATH, '//button[contains(text(),"Purchase")]').click()
        sleep(0.5)
        assert driver.find_element(By.XPATH, '//h2[contains(text(),"Thank you for your purchase!")]').is_displayed()
        order_confirmation = driver.find_element(By.XPATH, '//p[contains(text(),"Id:")]').text
        print(f'{hr}Order Confirmation:\n{order_confirmation}')
        assert full_name in order_confirmation
        print(f'{hr}Full Name: {full_name} is confirmed')
        assert credit_card_number in order_confirmation
        print(f'Credit Card Number: {credit_card_number} is confirmed')
        assert str(order_total) in order_confirmation
        print(f'Order Total: {order_total} is confirmed')
        sleep(0.25)
        driver.find_element(By.XPATH, '//button[contains(text(),"OK")]').click()
        # breakpoint()


def sign_up():
    print('--------------------~* SIGN UP *~---------------------')
    driver.find_element(By.LINK_TEXT, 'Sign up').click()
    sleep(0.5)
    assert driver.find_element(By.ID, 'signInModalLabel').is_displayed()
    sleep(0.25)
    driver.find_element(By.ID, 'sign-username').send_keys(username)
    sleep(0.25)
    driver.find_element(By.ID, 'sign-password').send_keys(password)
    sleep(0.5)
    driver.find_element(By.XPATH, '//button[contains(text(),"Sign up")]').click()
    sleep(0.5)
    driver.switch_to.alert.accept()
    print(f'{hr}Sign up successful, user: {username}/{password} is created')


def log_in():
    print('--------------------~* LOG IN *~---------------------')
    driver.find_element(By.LINK_TEXT, 'Log in').click()
    sleep(0.25)
    assert driver.find_element(By.ID, 'logInModalLabel').is_displayed()
    sleep(0.25)
    driver.find_element(By.ID, 'loginusername').send_keys(username)
    sleep(0.25)
    driver.find_element(By.ID, 'loginpassword').send_keys(password)
    sleep(0.25)
    driver.find_element(By.XPATH, '//button[contains(text(),"Log in")]').click()
    sleep(0.5)
    # nameofuser
    print(driver.find_element(By.ID, 'nameofuser').get_attribute("text"))
    assert driver.find_element(By.XPATH, f'//a[contains(text(), "Welcome {username}")]').is_displayed()
    logincheck = driver.find_element(By.XPATH, f'//a[contains(text(),{username})]').is_displayed()
    print(f'Login is successful {username} username is displayed: {logincheck}')


def log_out():
    print('--------------------~* LOG OUT *~---------------------')
    driver.find_element(By.LINK_TEXT, 'Log out').click()
    assert driver.find_element(By.ID, 'login2').is_displayed()
    print(f'Logout Successful')
    sleep(0.25)


setUp()
sign_up()
log_in()
checkout_cart()
log_out()
tearDown()

