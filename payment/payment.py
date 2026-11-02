
import random
import os
import sys
import time
import logging
import uuid
import json
import requests
import traceback

from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from rabbitmq import Publisher

# Prometheus
import prometheus_client
from prometheus_client import Counter, Histogram
from prometheus_client import CONTENT_TYPE_LATEST

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

CART = os.getenv('CART_HOST', 'cart')
USER = os.getenv('USER_HOST', 'user')
PAYMENT_GATEWAY = os.getenv('PAYMENT_GATEWAY', 'https://paypal.com/')

# Prometheus business metrics
PromMetrics = {}

PromMetrics['SOLD_COUNTER'] = Counter(
    'sold_count',
    'Running count of items sold'
)

PromMetrics['AUS'] = Histogram(
    'units_sold',
    'Average Unit Sale',
    buckets=(1, 2, 5, 10, 100)
)

PromMetrics['AVS'] = Histogram(
    'cart_value',
    'Average Value Sale',
    buckets=(100, 200, 500, 1000, 2000, 5000, 10000)
)

# Prometheus HTTP request metrics
PromMetrics['HTTP_REQUESTS'] = Counter(
    'robot_shop_http_requests_total',
    'Total HTTP requests handled by the payment service',
    ['method', 'route', 'status_code']
)

PromMetrics['HTTP_REQUEST_DURATION'] = Histogram(
    'robot_shop_http_request_duration_seconds',
    'HTTP request duration in seconds for the payment service',
    ['method', 'route', 'status_code'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5)
)


# HTTP request instrumentation
@app.before_request
def start_request_timer():
    if request.path != '/metrics':
        request.start_time = time.perf_counter()


@app.after_request
def record_http_metrics(response):
    # Exclude Prometheus scraping from HTTP metrics
    if request.path == '/metrics':
        return response

    start_time = getattr(request, 'start_time', None)

    if start_time is not None:
        duration = time.perf_counter() - start_time

        # Use Flask route patterns instead of dynamic URL IDs
        route = (
            request.url_rule.rule
            if request.url_rule
            else 'unmatched'
        )

        labels = {
            'method': request.method,
            'route': route,
            'status_code': str(response.status_code)
        }

        PromMetrics['HTTP_REQUESTS'].labels(**labels).inc()

        PromMetrics['HTTP_REQUEST_DURATION'].labels(
            **labels
        ).observe(duration)

    return response


@app.errorhandler(Exception)
def exception_handler(err):
    app.logger.error(str(err))
    return str(err), 500


@app.route('/health', methods=['GET'])
def health():
    return 'OK'


# Prometheus metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(
        prometheus_client.generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


@app.route('/pay/<id>', methods=['POST'])
def pay(id):
    app.logger.info('payment for {}'.format(id))
    cart = request.get_json()
    app.logger.info(cart)

    anonymous_user = True

    # Check user exists
    try:
        req = requests.get(
            'http://{user}:8080/check/{id}'.format(
                user=USER,
                id=id
            )
        )
    except requests.exceptions.RequestException as err:
        app.logger.error(err)
        return str(err), 500

    if req.status_code == 200:
        anonymous_user = False

    # Check that the cart is valid
    has_shipping = False

    for item in cart.get('items'):
        if item.get('sku') == 'SHIP':
            has_shipping = True

    if cart.get('total', 0) == 0 or has_shipping == False:
        app.logger.warning('cart not valid')
        return 'cart not valid', 400

    # Dummy call to payment gateway
    try:
        req = requests.get(PAYMENT_GATEWAY)
        app.logger.info(
            '{} returned {}'.format(
                PAYMENT_GATEWAY,
                req.status_code
            )
        )
    except requests.exceptions.RequestException as err:
        app.logger.error(err)
        return str(err), 500

    if req.status_code != 200:
        return 'payment error', req.status_code

    # Prometheus business metrics
    item_count = countItems(cart.get('items', []))

    PromMetrics['SOLD_COUNTER'].inc(item_count)
    PromMetrics['AUS'].observe(item_count)
    PromMetrics['AVS'].observe(cart.get('total', 0))

    # Generate order ID
    orderid = str(uuid.uuid4())

    queueOrder({
        'orderid': orderid,
        'user': id,
        'cart': cart
    })

    # Add to order history
    if not anonymous_user:
        try:
            req = requests.post(
                'http://{user}:8080/order/{id}'.format(
                    user=USER,
                    id=id
                ),
                data=json.dumps({
                    'orderid': orderid,
                    'cart': cart
                }),
                headers={'Content-Type': 'application/json'}
            )

            app.logger.info(
                'order history returned {}'.format(
                    req.status_code
                )
            )

        except requests.exceptions.RequestException as err:
            app.logger.error(err)
            return str(err), 500

    # Delete cart
    try:
        req = requests.delete(
            'http://{cart}:8080/cart/{id}'.format(
                cart=CART,
                id=id
            )
        )

        app.logger.info(
            'cart delete returned {}'.format(req.status_code)
        )

    except requests.exceptions.RequestException as err:
        app.logger.error(err)
        return str(err), 500

    if req.status_code != 200:
        return 'order history update error', req.status_code

    return jsonify({'orderid': orderid})


def queueOrder(order):
    app.logger.info('queue order')

    # Optional delay for screenshot demonstrations
    delay = int(os.getenv('PAYMENT_DELAY_MS', 0))
    time.sleep(delay / 1000)

    headers = {}
    publisher.publish(order, headers)


def countItems(items):
    count = 0

    for item in items:
        if item.get('sku') != 'SHIP':
            count += item.get('qty')

    return count


# RabbitMQ
publisher = Publisher(app.logger)


if __name__ == "__main__":
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)

    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    app.logger.info(
        'Payment gateway {}'.format(PAYMENT_GATEWAY)
    )

    port = int(os.getenv("SHOP_PAYMENT_PORT", "8080"))

    app.logger.info(
        'Starting on port {}'.format(port)
    )

    app.run(
        host='0.0.0.0',
        port=port
    )
