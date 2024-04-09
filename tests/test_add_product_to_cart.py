import logging

import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, have

from tests.conftest import auth_with_api, URL


def add_product_to_cart(product_url, cookie):
    response = requests.post(
        url=URL + product_url,
        cookies={"NOPCOMMERCE.AUTH": cookie}
    )
    allure.attach(body=response.text, name='Response', attachment_type=AttachmentType.TEXT, extension='.txt')
    logging.info(response.status_code)
    logging.info(response.text)

    return response.status_code


def clear_cart():
    browser.element('.qty-input').set_value('0').press_enter()


def test_add_fiction_book_to_cart():
    with allure.step('Авторизоваться через API.'):
        cookie = auth_with_api()

    with allure.step('Открыть страницу интерент-магазина "Demo Web Shop".'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with allure.step('Добавить товар "Fiction" в корзину через API.'):
        response_code = add_product_to_cart(product_url='/addproducttocart/catalog/45/1/1', cookie=cookie)
        assert response_code == 200

    with allure.step('Проверить, что в корзине содержится добавленный товар.'):
        browser.element('.ico-cart .cart-label').click()
        browser.element('.product-name').should(have.exact_text('Fiction'))

    with allure.step('Очистить корзину.'):
        clear_cart()


def test_add_jeans_to_cart():
    with allure.step('Авторизоваться через API.'):
        cookie = auth_with_api()

    with allure.step('Открыть страницу интерент-магазина "Demo Web Shop".'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with allure.step('Добавить товар "Blue Jeans" в корзину через API.'):
        response_code = add_product_to_cart(product_url='/addproducttocart/catalog/36/1/1', cookie=cookie)
        assert response_code == 200

    with allure.step('Проверить, что в корзине содержится добавленный товар.'):
        browser.element('.ico-cart .cart-label').click()
        browser.element('.product-name').should(have.exact_text('Blue Jeans'))

    with allure.step('Очистить корзину.'):
        clear_cart()
