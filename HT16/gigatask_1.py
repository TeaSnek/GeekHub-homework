"""
1. Отримайте та прочитайте дані з
"https://robotsparebinindustries.com/orders.csv". Увага! Файл має бути
прочитаний з сервера кожного разу при запускі скрипта, не зберігайте файл
локально.
2. Зайдіть на сайт "https://robotsparebinindustries.com/"
3. Перейдіть у вкладку "Order your robot"
4. Для кожного замовлення з файлу реалізуйте наступне:
    - закрийте pop-up, якщо він з'явився. Підказка: не кожна кнопка його
    закриває.
    - оберіть/заповніть відповідні поля для замовлення
    - натисніть кнопку Preview та збережіть зображення отриманого робота.
    Увага! Зберігати треба тільки зображення робота, а не всієї сторінки сайту.
    - натисніть кнопку Order та збережіть номер чеку. Увага! Інколи сервер
    тупить і видає помилку, але повторне натискання кнопки частіше всього
    вирішує проблему. Дослідіть цей кейс.
    - переіменуйте отримане зображення у формат <номер чеку>_robot (напр.
    123456_robot.jpg). Покладіть зображення в директорію output (яка має
    створюватися/очищатися під час запуску скрипта).
    - замовте наступного робота (шляхом натискання відповідної кнопки)

** Додаткове завдання (необов'язково)
    - окрім збереження номеру чеку отримайте також HTML-код всього чеку
    - збережіть отриманий код в PDF файл
    - додайте до цього файлу отримане зображення робота (бажано на одній
    сторінці, але не принципово)
    - збережіть отриманий PDF файл у форматі <номер чеку>_robot в директорію
    output. Окремо зображення робота зберігати не потрібно. Тобто замість
    зображень у вас будуть pdf файли які містять зображення з чеком.
"""

from time import sleep

import csv
from io import StringIO
from xhtml2pdf import pisa
import os
from pathlib import Path
import shutil

import cv2
import numpy as np
import requests
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

DEFAULT_SERVISE_ARGS = [
    '--no-sandbox',
    '--disable-application-cache',
    '--allow-running-insecure-content',
    '--hide-scrollbars',
    '--disable-infobars',
    '--disable-notificaions',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-setuid-sandbox',
    '--disable-notifications',
    '--start-maximized',
]

BASE_DIR = Path(__file__).parent

chrome_opions = ChromeOptions()
chrome_opions.add_experimental_option('excludeSwitches', ['enable-automtion'])
chrome_opions.add_experimental_option(
    'prefs',
    {
        'profile.default_content_settings_values.notifications': 2,
        'profile.default_content_settings.popups': 0
    }
)

for arg in DEFAULT_SERVISE_ARGS:
    chrome_opions.add_argument(arg)


class TaskScraper:
    def __init__(self) -> None:
        self.site_url = 'https://robotsparebinindustries.com/'
        self.file_url = self.site_url + 'orders.csv'
        self.file_content = []
        self.driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install(),
            ),
            options=chrome_opions
        )

    def start(self):
        self.get_file()
        self.create_or_clear_directory()
        self.open_site()

    def create_or_clear_directory(self):
        directory_path = Path(BASE_DIR, 'output')
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)

        os.makedirs(directory_path)

    def get_picture(self, pic_tag: WebElement):
        pic_location = pic_tag.location
        pic_size = pic_tag.size
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_np = np.frombuffer(screenshot, np.uint8)
        image = cv2.imdecode(screenshot_np, cv2.IMREAD_COLOR)
        left = int(pic_location['x'])
        top = int(pic_location['y'])
        right = int(pic_location['x'] + pic_size['width'])
        bottom = int(pic_location['y'] + pic_size['height'])
        return image[top:bottom, left:right]

    def form_pdf(self, receipt, order_num):
        html_template = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>HTML with Image</title>
            </head>
        <body>
            <img src="{
                Path(
                    BASE_DIR,
                    'output',
                    f'{order_num}_robot.png'
                ).as_posix()
            }" alt="Image">
            {receipt}
        </body>
        </html>
        '''
        pdf_path = Path(BASE_DIR, 'output',
                        f'{order_num}_robot.pdf').as_posix()

        with open(pdf_path, "wb") as pdf_file:
            pisa.CreatePDF(html_template, dest=pdf_file)

    def get_file(self):
        try:
            response = requests.get(self.file_url)
            reader = csv.DictReader(StringIO(response.text))
            self.file_content = [row for row in reader]
        except requests.RequestException:
            print('Unable to get orders data!')

    def open_site(self):
        self.driver.get(self.site_url)
        order_button = self.driver.find_element(
            By.CSS_SELECTOR,
            'a[href="#/robot-order"]'
        )
        order_button.click()
        for robot in self.file_content:
            self.order_robot(robot)

    def order_robot(self, robot_info):
        noway_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-dark')))
        noway_btn.click()
        head_selector = Select(self.driver.find_element(By.NAME, 'head'))
        body_check = self.driver.find_element(
            By.ID,
            f'id-body-{robot_info['Body']}'
        )
        leg_input = self.driver.find_element(
            By.CSS_SELECTOR,
            'input[placeholder="Enter the part number for the legs"]'
        )
        address_input = self.driver.find_element(By.NAME, 'address')
        head_selector.select_by_index(robot_info['Head'])

        body_check.click()
        leg_input.send_keys(robot_info['Legs'])
        address_input.send_keys(robot_info['Address'])

        preview_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button[id="preview"]')))
        order_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button[id="order"]')))
        try:
            preview_btn.click()
        except ElementClickInterceptedException:
            sleep(1)
            preview_btn.click()

        sleep(2)  # waiting picture to load
        pic_loction = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.ID, 'robot-preview')))
        robot_pic = self.get_picture(pic_loction)

        order_btn.click()

        try:
            alert_div = self.driver.find_element(By.CLASS_NAME, 'alert-danger')
            while alert_div.is_displayed():
                order_btn.click()
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass
        order_another_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'order-another')))
        order_number = self.driver.find_element(By.CLASS_NAME,
                                                'badge-success').text.lower()
        cv2.imwrite(
            filename=Path(BASE_DIR, 'output',
                          f'{order_number}_robot.png').as_posix(),
            img=robot_pic)

        receipt_div = self.driver.find_element(By.ID, 'receipt')
        receipt_html = receipt_div.get_attribute('outerHTML')
        self.form_pdf(receipt_html, order_number)
        order_another_btn = self.driver.find_element(By.ID, 'order-another')
        order_another_btn.click()

    def __del__(self):
        try:
            self.driver.close()
        except ImportError:
            pass


if __name__ == '__main__':
    task = TaskScraper()
    task.start()
    print('Hello world!')
