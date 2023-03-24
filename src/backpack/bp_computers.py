#!/usr/bin/python3
#
# Regards, the Alveare Solutions #!/Society -x
#
# COMPUTERS

import logging
import pysnooper

log = logging.getLogger('AsymetricRisk')


#@pysnooper.snoop()
def compute_base_quantity(last_price, account_value, price_percentage):
    """
    [ DESCRIPTION ]: Compute the base quantity of a stock or crypto coin based
        on the last ticker price, the value of your trading account in quote
        currency, and a price percentage value of your account value.

    [ EXAMPLE ]: Compute the base quantity for a stock with a last price of $100,
        a trading account value of $10,000, and a price percentage of 10% of the
        account value.

        >>> base_quantity = compute_base_quantity(100, 10000, 10)
        >>> print(base_quantity)  # Output: 99.009900990099

    [ INPUT ]:
        * last_price (float):
          The last ticker price of the stock or crypto coin.
        * account_value (float):
          The value of your trading account in quote currency.
        * price_percentage (float):
          The percentage change in price of your account value.

    [ RETURN ]: float: The base quantity of the stock or crypto coin.
    """
    account_value_percentage = account_value * price_percentage / 100
    base_quantity = account_value_percentage * last_price
    return base_quantity


def compute_quote_quantity(base_quantity, last_price):
    """
    [ DESCRIPTION ]: Compute the quote quantity from the base quantity and last
        price of a given stock.

    [ EXAMPLE ]: Compute the quote quantity for a stock with a base quantity of
        100 and a last price of $50.

        >>> quote_quantity = compute_quote_quantity(100, 50)
        >>> print(quote_quantity)  # Output: 5000.0

    [ INPUT ]:
        * base_quantity (float):
          The base quantity of the stock.
        * last_price (float):
          The last ticker price of the stock.

    [ RETURN ]: float: The quote quantity of the stock.
    """
    quote_quantity = base_quantity * last_price
    return quote_quantity


#@pysnooper.snoop()
def compute_value_threshold(value, percentage):
    """
    [ DESCRIPTION ]: Convert a percentage value to a value threshold.

    [ INPUT ]:
        * value (float): The value to use as a basis for the calculation.
        * percentage (float): The percentage value to convert.

    [ RETURN ]: float: The value threshold.
    """
    return float(value) * (1 + float(percentage) / 100)


def compute_percentage(whole, part, operation=None):
    """
    [ NOTE ]: If not operation is specified, it returns a value that represents
        the specified percentage of a given whole value -

    [ EXAMPLE ]:

        >>> compute_percentage(1000, 10)
        100

    [ NOTE ]: If the operation= keyword is specified, it returns a value with
        the percentage value added or subtracted

    [ EXAMPLE ]:

        >>> compute_percentage(1000, 10, operation='add')
        1100

        >>> compute_percentage(1000, 10, operation='subtract')
        900
    """
    if not operation:
        return (float(part)/100) * float(whole)
    if operation not in ['add', 'subtract']:
        log.error('Invalid operation specified! {}'.format(operation))
        return False
    elif operation == 'subtract':
        part *= -1  # Multiply by -1 to subtract instead of add.
    return float(whole) * (1 + float(part)/100)


def compute_percentage_of(part, whole):
    log.debug('')
    try:
        if part == 0:
            percentage = 0
        else:
            percentage = 100 * float(part) / float(whole)
        return percentage #"{:.0f}".format(percentage)
    except Exception as e:
        percentage = 100
        return percentage #"{:.0f}".format(percentage)


