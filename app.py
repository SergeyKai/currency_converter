from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from currency_api_conn import CurrencyAPI
from models import db, CurrencyRate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


def fetch_currency_rates():
    response = CurrencyAPI().live()
    currencies = CurrencyAPI().list().get('currencies')
    if response is not None:
        timestamp = datetime.utcfromtimestamp(response['timestamp'])

        usd = CurrencyRate(currency='USD',
                           description='United States Dollar',
                           rate=1,
                           timestamp=timestamp,
                           last_updated=timestamp)

        db.session.add(usd)
        db.session.commit()

        for currency, rate in response.get('quotes').items():
            existing_rate = CurrencyRate.query.filter_by(currency=currency[3:]).first()
            if existing_rate:
                existing_rate.rate = rate
                existing_rate.last_updated = timestamp
            else:
                new_rate = CurrencyRate(currency=currency[3:],
                                        description=currencies.get(currency[3:]),
                                        rate=rate,
                                        timestamp=timestamp,
                                        last_updated=timestamp)
                db.session.add(new_rate)

        db.session.commit()


@app.route('/update_rates', methods=['POST'])
def update_rates():
    fetch_currency_rates()
    return jsonify({"message": "Currency rates updated successfully"}), 200


@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    from_currency = data.get('from')
    to_currency = data.get('to')
    amount = data.get('amount')

    if not all([from_currency, to_currency, amount]):
        return jsonify({"message": "Invalid data"}), 400

    print(
        data,
        from_currency,
        to_currency,
        amount,
    )

    from_rate = CurrencyRate.query.filter_by(currency=from_currency).first()
    to_rate = CurrencyRate.query.filter_by(currency=to_currency).first()

    print(
        from_rate,
        to_rate,
    )

    if not from_rate or not to_rate:
        return jsonify({"message": "Currency not supported"}), 400

    base_currency_amount = amount / from_rate.rate
    converted_amount = base_currency_amount * to_rate.rate

    print('pass')

    return jsonify({"converted_amount": converted_amount}), 200


@app.route('/')
def index():
    currencies = CurrencyRate.query.all()
    return render_template('index.html', currencies=currencies)


app.run()
