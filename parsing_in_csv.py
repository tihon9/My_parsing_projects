import csv
from bs4 import BeautifulSoup
import requests

url = "https://parsinger.ru/html/index1_page_1.html"
base_url = "https://parsinger.ru/html/"

with open("res.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(['Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена', 'Старая цена', 'Ссылка'])


def soup(url, retry=5):
    try:
        response = requests.get(url=url)
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print("Произошла ошибка", str(e))
        print(f"Осталось {retry - 1} попытки")
        return soup(url, retry=retry - 1)


# Находим ссылки на все типы товаров (меню слева), внутри проходим по всем страницам, далее заходим в каждую карточку и оттуда достаем нужную информацию
soup1 = soup(url)
nav_url = [link["href"] for link in soup1.find("div", class_="nav_menu").find_all("a")]
for i in nav_url:
    soup1 = soup(f"{base_url}{i}")
    pag_url = [link["href"] for link in soup1.find("div", class_="pagen").find_all("a")]
    for j in pag_url:
        soup1 = soup(f"{base_url}{j}")
        cart_url = [link["href"] for link in soup1.find_all("a", class_="name_item")]
        for k in cart_url:
            soup1 = soup(f"{base_url}{k}")
            name = soup1.find("p", {"id": "p_header"}).text
            art = soup1.find("p", {"class": "article"}).text.split(":")[1].strip()
            brand = soup1.find("li", {"id": "brand"}).text.split(":")[1].strip()
            model = soup1.find("li", {"id": "model"}).text.split(":")[1].strip()
            in_stock = soup1.find("span", {"id": "in_stock"}).text.split(":")[1].strip()
            price = soup1.find("span", {"id": "price"}).text
            old_price = soup1.find("span", {"id": "old_price"}).text
            link = f"{base_url}{k}"
            with open("res.csv", "a", encoding="utf-8-sig", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                data = [name, art, brand, model, in_stock, price, old_price, link]
                writer.writerow(data)
