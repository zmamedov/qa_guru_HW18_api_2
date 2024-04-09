import requests
from selene import browser, have

from tests.conftest import auth_with_api, URL


def add_product_to_cart(product_url, cookie):
    response = requests.post(
        url=URL + product_url,
        cookies={"NOPCOMMERCE.AUTH": cookie}
    )

    return response.status_code


def clear_cart():
    browser.element('.qty-input').set_value('0').press_enter()


def test_cart_should_have_added_product():
    cookie = auth_with_api()
    browser.open('/')
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
    browser.open('/')

    response_code = add_product_to_cart(product_url='/addproducttocart/catalog/45/1/1', cookie=cookie)
    assert response_code == 200

    browser.element('.ico-cart .cart-label').click()
    browser.element('.product-name').should(have.exact_text('Fiction'))

    clear_cart()


def test_clear_cart():
    cookie = auth_with_api()
    browser.open('/')
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
    browser.open('/')

    response_code = add_product_to_cart(product_url='/addproducttocart/catalog/45/1/1', cookie=cookie)
    assert response_code == 200
    browser.element('.ico-cart .cart-label').click()
    clear_cart()

    browser.element('.order-summary-content').should(have.text('Your Shopping Cart is empty!'))
