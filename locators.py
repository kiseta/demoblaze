import random
from datetime import datetime

from faker import Faker
fake = Faker(locale='en_US')

# ------------------ DEMOBLAZE DATA ------------------------------
app = 'DEMOBLAZE'
base_url = 'https://www.demoblaze.com/index.html'
product_url = 'https://www.demoblaze.com/prod.html?idp_='
home_page_title = "STORE"
full_name = f'{fake.first_name()} {fake.last_name()}'
credit_card_number = fake.credit_card_number()
username = full_name.replace(' ','').lower()
password = fake.password()
random_ids = random.sample(range(1, 15), 3)
country = fake.country()
city = fake.city()
rndint = fake.pyint(1, 12)
month = rndint
year = datetime.now().year + rndint
product_list = []
total = 0
deleted_item_price = 0
cart_total = 0
new_cart_total = 0
order_total = 0

# print(full_name, credit_card_number, username, password, random_ids, country, city, month, rndint, year)
# -------------------------------------------------