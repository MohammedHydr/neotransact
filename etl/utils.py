import logging

from etl.constants import FIXED_CURRENCY_RATES

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message)


def convert_currency(amount, from_currency, to_currency, fixed_rates=FIXED_CURRENCY_RATES):
    if from_currency == to_currency:
        return round(amount, 2)

    try:
        # Check if the currency pair exists in the fixed rates mapping
        rate = fixed_rates.get((from_currency, to_currency))
        if rate is None:
            raise Exception(f"Conversion rate from {from_currency} to {to_currency} is not defined.")

        converted_amount = amount * rate
        return round(converted_amount, 2)
    except Exception as e:
        raise Exception("Currency conversion failed: " + str(e))
