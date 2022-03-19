import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import locators as locators

s = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service = s)
hr = '--------~*~----------------~*~----------\n'

def setUp():
    driver.maximize_window()  # open web browser and maximize the window
    driver.implicitly_wait(30)  # wait for up to 30 sec for the browser response
    driver.get(locators.base_url)  # navigate to app website

    # check the correct URL and the correct title
    if driver.current_url == locators.base_url and driver.title == locators.home_page_title:
        assert driver.current_url == locators.base_url
        assert driver.title == locators.home_page_title
        print(f'{hr}Launch {locators.app} Website\nURL: {driver.current_url}\nPage title: {driver.title}')
        # breakpoint()
    else:
        print(f'{hr}>>>> We are NOT on {locators.app} Home Page. Check your code.')
        print(f'{hr}Expected URL: {locators.base_url} \nActual URL: {driver.current_url}')
        print(f'{hr}Expected Page Title: {locators.home_page_title} \nActual Page Title: {driver.title}')
        tearDown()


def tearDown():  # function to end the session
    if driver is not None:
        print(f'{hr}Test Completed at: {datetime.datetime.now()}')
        sleep(0.25)
        driver.close()
        driver.quit()


def checkout_cart():
    print('--------------------~* ADD ITEMS TO SHOPPING CART *~---------------------')
    print(locators.random_ids)
    if driver.current_url == locators.base_url:
        # add items to cart
        for i in locators.random_ids:
            driver.get(f'{locators.product_url}{i}')
            sleep(2)
            assert driver.find_element(By.CLASS_NAME, 'name').is_displayed()
            product_name = driver.find_element(By.CLASS_NAME, 'name').text
            locators.product_list.append(product_name)
            price_tag = driver.find_element(By.CLASS_NAME, 'price-container').text
            item_price = int(''.join(filter(str.isdigit, price_tag)))   # capture numerical value only
            locators.total += item_price
            print(f'{hr}Go to: {product_name} page, Product ID: {i}')
            driver.find_element(By.LINK_TEXT, 'Add to cart').click()
            sleep(0.5)
            driver.switch_to.alert.accept()
            print(f'{product_name} is added to Shopping Cart, item price: {item_price}')
            sleep(0.25)
            driver.find_element(By.ID, 'nava').click()
            sleep(0.25)

        print(f'{hr}Product List: {locators.product_list}')
        print(f'Cart total: {locators.total}')

        # go to cart
        driver.find_element(By.ID, 'cartur').click()
        print(f'{hr}Go to cart')

        sleep(0.25)
        # validate items in the list
        for p in locators.product_list:
            item_in_cart = driver.find_element(By.XPATH, f'//td[contains(.,"{p}")]').is_displayed()
            assert item_in_cart
            print(f'{hr}Success! {p} is in Shopping Cart: {item_in_cart}')
            sleep(0.25)

        # validate cart total
        cart_total = int(driver.find_element(By.ID, 'totalp').text)
        print(f'{hr}Validate Cart Total:\nExpected cart total: {locators.total}, Actual cart total: {cart_total} ')
        assert cart_total == locators.total

        #driver.find_element(By.LINK_TEXT, 'Delete').click()
        # delete second item from the cart
        locators.deleted_item_price = driver.find_element(By.XPATH, f'//tr[contains(.,"{locators.product_list[1]}")]/td[3]').text
        driver.find_element(By.XPATH, f"//td[contains(., '{locators.product_list[1]}')]/../td/a[contains(text(),'Delete')]").click()
        print(f'{hr}Now deleting {locators.product_list[1]} from Shopping Cart')
        sleep(0.25)
        print(f'{hr}{locators.product_list[1]} is deleted!')

        sleep(2)
        locators.total = locators.total - int(locators.deleted_item_price)
        locators.new_cart_total = int(driver.find_element(By.ID, 'totalp').text)
        assert locators.new_cart_total == locators.total
        print(f'Deleted Item Price: {locators.deleted_item_price}, Cart total updated: {locators.total}')
        print(f'New Cart total confirmed: {locators.new_cart_total}\nContinue to Place Order')

        sleep(0.5)

        # checkout cart
        driver.find_element(By.XPATH, '//button[contains(text(),"Place Order")]').click()
        sleep(0.5)
        assert driver.find_element(By.ID, 'orderModalLabel').is_displayed()
        order_total = driver.find_element(By.ID, 'totalm').text
        order_total = int(''.join(filter(str.isdigit, order_total)))  # capture numerical value only
        print(f'{hr}Order total: {order_total}')
        assert order_total == locators.new_cart_total

        sleep(0.25)
        driver.find_element(By.ID, 'name').send_keys(locators.full_name)
        sleep(0.5)
        driver.find_element(By.ID, 'country').send_keys(locators.country)
        sleep(0.5)
        driver.find_element(By.ID, 'city').send_keys(locators.city)
        sleep(0.5)
        driver.find_element(By.ID, 'card').send_keys(locators.credit_card_number)
        sleep(0.5)
        driver.find_element(By.ID, 'month').send_keys(locators.month)
        sleep(0.5)
        driver.find_element(By.ID, 'year').send_keys(locators.year)
        sleep(0.5)
        driver.find_element(By.XPATH, '//button[contains(text(),"Purchase")]').click()
        sleep(0.5)
        assert driver.find_element(By.XPATH, '//h2[contains(text(),"Thank you for your purchase!")]').is_displayed()
        order_confirmation = driver.find_element(By.XPATH, '//p[contains(text(),"Id:")]').text
        print(f'{hr}Order Confirmation:\n{order_confirmation}')
        assert locators.full_name in order_confirmation
        print(f'{hr}Full Name: {locators.full_name} is confirmed')
        assert locators.credit_card_number in order_confirmation
        print(f'Credit Card Number: {locators.credit_card_number} is confirmed')
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
    driver.find_element(By.ID, 'sign-username').send_keys(locators.username)
    sleep(0.25)
    driver.find_element(By.ID, 'sign-password').send_keys(locators.password)
    sleep(0.5)
    driver.find_element(By.XPATH, '//button[contains(text(),"Sign up")]').click()
    sleep(0.5)
    driver.switch_to.alert.accept()
    print(f'{hr}Sign up successful, user: {locators.username}/{locators.password} is created')


def log_in():
    print('--------------------~* LOG IN *~---------------------')
    driver.find_element(By.LINK_TEXT, 'Log in').click()
    sleep(0.25)
    assert driver.find_element(By.ID, 'logInModalLabel').is_displayed()
    sleep(0.25)
    driver.find_element(By.ID, 'loginusername').send_keys(locators.username)
    sleep(0.25)
    driver.find_element(By.ID, 'loginpassword').send_keys(locators.password)
    sleep(0.25)
    driver.find_element(By.XPATH, '//button[contains(text(),"Log in")]').click()
    sleep(0.5)
    # nameofuser
    print(driver.find_element(By.ID, 'nameofuser').get_attribute("text"))
    assert driver.find_element(By.XPATH, f'//a[contains(text(), "Welcome {locators.username}")]').is_displayed()
    logincheck = driver.find_element(By.XPATH, f'//a[contains(text(),{locators.username})]').is_displayed()
    print(f'Login is successful {locators.username} username is displayed: {logincheck}')


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

