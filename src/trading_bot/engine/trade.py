#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# ASYMETRIC RISK TRADE MODEL

import logging
import time
import datetime
import random
import string
import math
import pysnooper

from decimal import Decimal
from src.backpack.bp_fetchers import fetch_timestamp
from src.backpack.bp_generators import generate_msg_id
from src.backpack.bp_general import (
    stdout_msg, pretty_dict_print
)
from src.ar_exceptions import (
    ARInvalidStateException,
    ARPreconditionsException,
)

log = logging.getLogger('AsymetricRisk')


class Trade():
    '''
    [ NOTE ]: Responsibilities:

        * Defines Trade data model.
        * Records state, context and metadata of trade.
        * Keeps action history records.
        * Keeps record of signals that generated trade,
        * Enforces state transition rules.
        * Locally generates default Trade ID.

    [ NOTE ]: State order:
        DRAFT -> EVALUATED -> COMMITED -> DONE
                                       -> DISCARDED
                                       -> EXPIRED

    [ NOTE ]: Each time the Trade status changes, a history record with all the
        the action data is cached, with a default history limit of 20 records.

    [ NOTE ]: Multiple buy/sell signals can be grouped in order to generate the
        Trade() instance. If the Trade already exists and is not yet commited,
        new signals of the same side will also be associated with this instance.
    '''

    STATUS_DRAFT = 'DRAFT'
    STATUS_EVALUATED = 'EVALUATED'
    STATUS_COMMITED = 'COMMITED'
    STATUS_DONE = 'DONE'
    STATUS_DISCARDED = 'DISCARDED'
    STATUS_EXPIRED = 'EXPIRED'
    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'
    ORDER_TYPE = 'STOP_LOSS_LIMIT'
    ORDER_TIME_IN_FORCE = 'GTC'
    ORDER_RESPONSE_TYPE = 'FULL'

#   @pysnooper.snoop()
    def __init__(self, **context) -> None:
        log.debug('')
        self._signals = list()
        self._context = context
        self._history = {} # {<timestamp>: {action: '', context: {}, failed: False, details: {}}}
        self.create_date = datetime.datetime.now()
        self.write_date = self.create_date
        self.trade_id = context.get('trade-id', generate_msg_id(
            random.randint(4, 12), id_characters=list(string.digits)
        ))
        self.ticker_symbol = context.get('ticker-symbol', str()).replace('/', '')
        self.status = self.STATUS_DRAFT
        self.previous_status = None
        self.risk = int()
        self.base_quantity = float()
        self.quote_quantity = float()
        self.side = str()
        self.current_price = float()
        self.stop_loss_price = float()
        self.take_profit_price = float()
        self.price_percent_change = float()
        self.trailing_delta = float()
        self.trade_fee = float()
        self.expires_on = None
        self.result = dict()
        self.filters = dict()

    # MAGIK

    def __str__(self):
        return f'Symbol: {self.ticker_symbol}, Side: {self.sided}, '\
            f'Quantity: {self.base_quantity}, Status: {self.status}, '\
            f'Risk: {self.risk}'

    # SETTERS

    def set_evaluated(self) -> bool:
        '''
        [ NOTE ]:
        '''
        log.debug('')
        return False if not self.check_preconditions() \
            else self.set_state(self.STATUS_EVALUATED)

    def set_commited(self) -> bool:
        '''
        [ NOTE ]:
        '''
        log.debug('')
        return False if not self.check_preconditions() \
            else self.set_state(self.STATUS_COMMITED)

    def set_done(self) -> bool:
        '''
        [ NOTE ]:
        '''
        log.debug('')
        if not self.check_preconditions():
            return False
        self.expires_on = None
        return self.set_state(self.STATUS_DONE)

    def set_state(self, state: str) -> bool:
        log.debug('')
        valid_states = (
            self.STATUS_DRAFT, self.STATUS_EVALUATED, self.STATUS_COMMITED,
            self.STATUS_DONE, self.STATUS_DISCARDED, self.STATUS_EXPIRED,
        )
        if state not in valid_states:
            raise ARInvalidStateException(11, f'Invalid Trade state for {self}')
            return False
        elif self.check_expired():
            state = self.STATUS_EXPIRED
        self.previous_status, self.status = self.status, state
        self.write_date = datetime.datetime.now()
        return True

    # CHECKERS

#   @pysnooper.snoop()
    def check_filter_percent_price_by_side(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'PERCENT_PRICE_BY_SIDE',
            'bidMultiplierUp': '5',
            'bidMultiplierDown': '0.2',
            'askMultiplierUp': '5',
            'askMultiplierDown': '0.2',
            'avgPriceMins': 1
        }, ...]

        [ NOTE ]: PERCENT_PRICE_BY_SIDE is a filter parameter in the Binance API
            that sets the allowed range of price variation for a user's order
            based on the order side (buy or sell) and the market price at the
            time the order is placed. This filter is designed to prevent users
            from placing orders that are too far away from the current market
            price, which could potentially disrupt the market.

        [ NOTE ]: The PERCENT_PRICE_BY_SIDE filter takes two arrays of values,
            one for the buy side and one for the sell side. Each array contains
            two percentage values: "multiplierUp" and "multiplierDown". These
            values define the upper and lower bounds for the allowable price
            range as a percentage of the current market price.

            [ Ex ]: If the current market price for a trading pair is $100, and
                the "multiplierUp" value is set to 1.05 and the "multiplierDown"
                value is set to 0.95 for the buy side, a user can only place a
                buy order with a price between $95 and $105.

        [ NOTE ]: Enforcing the PERCENT_PRICE_BY_SIDE filter can be done through
            the Binance API when placing orders. When making an order request,
            the user can specify the "newOrderRespType" parameter as "FULL" to
            receive a detailed response from the API, including any error messages
            if the order is rejected due to the filter. If the user attempts to
            place an order with a price that falls outside of the allowable range
            defined by the filter, the API will return an error indicating that
            the price is not within the allowed range.

        [ NOTE ]: It is important to note that the PERCENT_PRICE_BY_SIDE filter
            is enforced on the server-side, meaning that if a user attempts to
            place an order with a price outside of the allowable range through
            other means (such as the Binance website or mobile app), the order
            will still be rejected.

        [ NOTE ]: "bid" and "ask" are two terms used to describe the different
            prices at which a security can be bought and sold.

        [ NOTE ]: The bid price is the highest price that a buyer is willing to
            pay for a security at a given time. This is the price that a trader
            would receive if they were to sell the security right away. On the
            other hand, the ask price is the lowest price at which a seller is
            willing to sell the security. This is the price that a trader would
            pay if they were to buy the security right away.

        [ NOTE ]: The difference between the bid and ask prices is known as the
            spread, which represents the profit that the market maker earns for
            facilitating the trade. The spread can vary depending on the liquidity
            of the security, the volatility of the market, and other factors.

            [ Ex ]: Let's say that a trader wants to buy 100 shares of XYZ stock.
                The current bid price is $50.00, and the ask price is $50.10. If the
                trader places a market order to buy the shares, they will pay the ask
                price of $50.10 per share. Alternatively, if the trader places a limit
                order to buy the shares at $50.05, they will only be filled if a seller
                is willing to sell at that price or lower.

            [ Ex ]: Suppose that a trader wants to sell 50 shares of ABC stock.
                The current bid price is $25.50, and the ask price is $25.60. If the
                trader places a market order to sell the shares, they will receive
                the bid price of $25.50 per share. Alternatively, if the trader places
                a limit order to sell the shares at $25.55, they will only be filled
                if a buyer is willing to buy at that price or higher.

        [ NOTE ]: Price Restrictions:

            SELL: Limit Price > Last Price > Stop Price
            BUY : Limit Price < Last Price < Stop Price

        [ NOTE ]: In a BUY OCO (One Cancels the Other) order, there are two orders
            placed simultaneously: a limit order to buy and a stop-limit order to
            sell. The idea behind this type of order is to protect your position
            in case the market moves against you, while also allowing you to profit
            if the market moves in your favor.

            When setting the limit price for the take profit order, it is
            important to remember that the limit price must be lower than the
            current market price. This is because in a BUY order, the take profit
            order is executed when the market price reaches the limit price or
            higher. If the limit price is higher than the current market price,
            the order will not be executed and the position will remain open.

            [ Ex ]: let's say the current market price for a stock is
                $50, and you want to place a BUY OCO order with a take profit limit
                price of $55. If you set the limit price at $55, the order will not
                be executed until the market price reaches $55 or higher. However,
                if the market price never reaches $55, the order will not be filled,
                and you will miss out on potential profits.

            On the other hand, if you set the take profit limit price at
            $48, which is lower than the current market price, the order will
            be executed as soon as the market price reaches $48 or higher. This
            ensures that you lock in profits before the market turns against you.

            Setting the take profit limit price lower than the
            current market price in a BUY OCO order helps to ensure that the order
            is executed and profits are locked in before the market turns against you.

            More details over at:
            https://binance-docs.github.io/apidocs/spot/en/#new-oco-trade
        '''
        log.debug('')
        trade_filter = self.filters.get('PERCENT_PRICE_BY_SIDE')
        if self.side.upper() not in ('BUY', 'SELL'):
            log.error(
                f'Trade side ({self.side}) not set up properly! '
                'Valid values are (BUY | SELL)'
            )
            return False
        elif not self.current_price:
            log.error(
                f'Trade current_price ({self.current_price}) not set up properly. '
                'Cant be zero.'
            )
            return False
        elif not trade_filter:
            log.warning(f'No data found on trade filter PERCENT_PRICE_BY_SIDE! Skipping..')
            return True
        #  We extract the allowed percentage change for the order based on the
        #  side, and enforce the filter by checking if the specified percentage
        #  change is within the allowed range. Finally, we adjust the
        #  percentage change if necessary before placing the OCO order.
        if self.side == 'BUY':
            if self.take_profit_price > self.current_price:
                log.error(
                    f'Take Profit Price {self.take_profit_price} cannot be higher '
                    f'that last known price {self.current_price} on {self.side} '
                    'orders.'
                )
                return False
            if self.stop_loss_price < self.current_price:
                log.error(
                    f'Stop Loss Price {self.stop_loss_price} cannot be lower that '
                    f'last known price {self.current_price} on {self.side} '
                    'orders.'
                )
                return False
        elif self.side == 'SELL':
            if self.take_profit_price < self.current_price:
                log.error(
                    f'Take Profit Price {self.take_profit_price} cannot be lower '
                    f'that last known price {self.current_price} on {self.side} '
                    'orders.'
                )
            if self.stop_loss_price > self.current_price:
                log.error(
                    f'Stop Loss Price {self.stop_loss_price} cannot be higher that '
                    f'last known price {self.current_price} on {self.side} '
                    'orders.'
                )
                return False
        return True

#   @pysnooper.snoop()
    def check_filter_min_notional(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'MIN_NOTIONAL',
            'minNotional': '10.00000000',
            'applyToMarket': True,
            'avgPriceMins': 1
        }, ...]

        [ NOTE ]: MIN_NOTIONAL is a filter parameter in the Binance API that sets
            the minimum value of an order for a given trading pair. This filter
            is designed to prevent users from placing orders that are too small
            and potentially ineffective or disruptive to the market.

        [ NOTE ]: The MIN_NOTIONAL filter takes a single value that represents
            the minimum notional value of an order in the base asset of the trading
            pair. The notional value is calculated by multiplying the order quantity
            by the price of the trading pair. For example, if the trading pair
            is BTC/USDT, the notional value would be calculated by multiplying
            the quantity of BTC by the current price of BTC/USDT in USDT.

        [ NOTE ]: Enforcing the MIN_NOTIONAL filter can be done through the
            Binance API when placing orders. When making an order request, the
            user can specify the "newOrderRespType" parameter as "FULL" to receive
            a detailed response from the API, including any error messages if the
            order is rejected due to the filter. If the user attempts to place an
            order with a notional value below the minimum allowable amount, the
            API will return an error indicating that the order is not within the
            allowed range.

        [ NOTE ]: It is important to note that the MIN_NOTIONAL filter is enforced
            on the server-side, meaning that if a user attempts to place an order
            with a notional value below the minimum allowable amount through other
            means (such as the Binance website or mobile app), the order will still
            be rejected.

        [ NOTE ]: If the order value is below the minimum notional value required
            for the BTCUSDT trading pair, the create_order() method will raise a
            BinanceAPIException with the error message "Filter failure: MIN_NOTIONAL".
            In this case, you should adjust the order quantity or price to meet
            the minimum notional value requirement for the trading pair.
        '''
        log.debug('')
        trade_filter = self.filters.get('MIN_NOTIONAL')
        if not self.current_price or not self.base_quantity:
            log.error(
                f'Trade parameters current_price ({self.current_price}) or '
                f'base_quantity ({self.base_quantity}) not set up properly! '
                'Neither can be zero.'
            )
            return False
        elif not trade_filter:
            log.error(f'No data found on trade filter MIN_NOTIONAL! Skipping..')
            return True
        # We enforce the MIN_NOTIONAL filter settings by calculating the notional
        # value of the order (price * quantity), and comparing it to the minNotional
        # value from the filter settings. If the notional value is less than the
        # minNotional value, we calculate the minimum quantity required to meet
        # the minNotional value and update the quantity value accordingly.
        min_notional = float(trade_filter['minNotional'])
        notional = round(self.current_price * self.base_quantity, 8)
        if notional < min_notional:
            self.base_quantity = math.ceil(
                min_notional / self.current_price * 10**8
            ) / 10**8
        return True

#   @pysnooper.snoop()
    def check_filter_price(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'PRICE_FILTER',
            'minPrice': '0.00010000',
            'maxPrice': '1000.00000000',
            'tickSize': '0.00010000'
        }, ...]

        [ NOTE ]: PRICE_FILTER is a filter parameter in the Binance API that
            sets the allowable price range for a given trading pair. This filter
            is designed to prevent users from placing orders that are too far
            outside of the current market price, which could potentially disrupt
            the market.

        [ NOTE ]: The PRICE_FILTER filter takes three values: "minPrice",
            "maxPrice", and "tickSize". The "minPrice" value sets the minimum
            allowable price for an order, the "maxPrice" value sets the maximum
            allowable price, and the "tickSize" value sets the allowable price
            increments.

        [ NOTE ]: Enforcing the PRICE_FILTER can be done through the Binance API
            when placing orders. When making an order request, the user can specify
            the "newOrderRespType" parameter as "FULL" to receive a detailed
            response from the API, including any error messages if the order is
            rejected due to the filter. If the user attempts to place an order
            at a price outside of the allowable range or in a price increment
            that is not allowed, the API will return an error indicating that
            the order is not within the allowed range.

        [ NOTE ]: It is important to note that the PRICE_FILTER filter is enforced
            on the server-side, meaning that if a user attempts to place an order
            at a price outside of the allowable range through other means (such
            as the Binance website or mobile app), the order will still be rejected.

        [ EXAMPLE ]: If the price filter specifies a minimum price of 0.01 and a
            tick size of 0.0001, then your order price should be a multiple of
            0.0001 and greater than or equal to 0.01.

        [ NOTE ]: Price Restrictions:

            SELL: Limit Price > Last Price > Stop Price
            BUY : Limit Price < Last Price < Stop Price

            More details over at:
            https://binance-docs.github.io/apidocs/spot/en/#new-oco-trade
        '''
        log.debug('')
        trade_filter = self.filters.get('PRICE_FILTER')
        if not trade_filter:
            log.warning(f'No data found on trade filter PRICE_FILTER! Skipping..')
            return True
        # We enforce the PRICE_FILTER filter settings by rounding the price,
        # stop_price, and stop_limit_price values to the appropriate precision
        # based on the tickSize value from the PRICE_FILTER filter settings.
        price_precision = float(trade_filter['tickSize'])
        min_price = float(trade_filter['minPrice'])
        max_price = float(trade_filter['maxPrice'])
        if self.side == 'BUY':
            if self.take_profit_price > self.current_price:
                self.take_profit_price = self.current_price - 0.01
            if self.stop_loss_price < self.current_price:
                self.stop_loss_price = self.current_price + 0.0
            if float(self.stop_loss_price) <= float(self.take_profit_price):
                self.take_profit_price = str(float(self.stop_loss_price) + 0.01)
        elif self.side == 'SELL':
            if self.take_profit_price < self.current_price:
                self.take_profit_price = self.current_price + 0.01
            if self.stop_loss_price > self.current_price:
                self.stop_loss_price = self.current_price - 0.01
            if self.stop_loss_price >= self.take_profit_price:
                if float(self.stop_loss_price) >= float(self.take_profit_price):
                    self.take_profit_price = str(float(self.stop_loss_price) - 0.01)
        else:
            log.error('Cannot determine Trade side! None specified.')
            return False
        self.current_price = float(Decimal(self.current_price)\
            .quantize(Decimal(str(price_precision))))
        self.take_profit_price = float(Decimal(self.take_profit_price)\
            .quantize(Decimal(str(price_precision))))
        self.stop_loss_price = float(Decimal(self.stop_loss_price)\
            .quantize(Decimal(str(price_precision))))
        return True

#   @pysnooper.snoop()
    def check_filter_stop_loss_price(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'STOP_PRICE_FILTER',
            'minPrice': '0.00010000',
            'maxPrice': '1000.00000000',
            'tickSize': '0.00010000'
        }, ...]

        [ NOTE ]: The STOP_PRICE_FILTER is a filter used by the Binance API to
            restrict the stop price of an order. It ensures that the stop price
            of an order is within certain limits and increments, based on the
            symbol being traded. The filter is applied when placing a STOP_LOSS
            or TAKE_PROFIT order.

        [ NOTE ]: The STOP_PRICE_FILTER has the following parameters:
            * filterType: The type of filter, which is always "STOP_PRICE_FILTER"
              for this filter.
            * minPrice: The minimum stop price for the symbol, as a decimal string.
            * maxPrice: The maximum stop price for the symbol, as a decimal string.
            * tickSize: The increment that stop price can be increased or decreased
              by, as a decimal string.
        '''
        log.debug('')
        trade_filter = self.filters.get('STOP_PRICE_FILTER')
        if not trade_filter:
            log.warning(f'No data found on trade filter STOP_PRICE_FILTER! Skipping..')
            return True
        # Almost the same as for PRICE_FILTER
        price_precision = float(trade_filter['tickSize'])
        self.stop_loss_price = float() if not self.stop_loss_price else round(
            self.stop_loss_price, int(-1 * math.log10(price_precision))
        )
        min_price = float(trade_filter['minPrice'])
        max_price = float(trade_filter['maxPrice'])
        if self.stop_loss_price < min_price:
            self.stop_loss_price = min_price
        elif self.stop_loss_price > max_price:
            self.stop_loss_price = max_price
        return False if self.stop_loss_price < min_price else True

#   @pysnooper.snoop()
    def check_preconditions_evaluated(self):
        log.debug('')
        if not self.stop_loss_price or not self.take_profit_price:
            log.warning(
                f'Trade take_profit ({self.take_profit_price}), stop_loss '
                f'({self.stop_loss_price}) not set up properly! '
                'Neither can be zero.'
            )
        elif not self._signals:
            log.warning(
                f'Trade Signals ({self._signals}) not set up properly! '
                'Must have at least one.'
            )
        return False if not self._signals or not self.stop_loss_price \
            or not self.take_profit_price \
            or not self.filter_check(*list(self.filters.values())) else True

#   @pysnooper.snoop()
    def check_preconditions(self):
        '''
        [ NOTE ]: Checks all Trade data to be aligned to the constraints imposed
            by the Trade state. Results may differ when executed in different
            states with the same data set.
        '''
        log.debug('')
        if not self.status:
            log.error(
                'Trade status not set! Cannot check preconditions for unknown '
                'state transition.'
            )
            return False
        checkers = {
            self.STATUS_DRAFT: self.check_preconditions_draft,
            self.STATUS_EVALUATED: self.check_preconditions_evaluated,
            self.STATUS_COMMITED: self.check_preconditions_commited,
            self.STATUS_DONE: self.check_preconditions_done,
        }
        if self.status not in checkers.keys() \
                or not self.check_preconditions_general():
            return False
        return checkers[self.status]()

#   @pysnooper.snoop()
    def check_preconditions_general(self):
        log.debug('')
        if not self.ticker_symbol or not self.side:
            log.warning(
                f'Trade ticker_symbol ({self.ticker_symbol}) or trade side '
                f'({self.side}) not set up properly! Both must be set.'
            )
        elif not self.current_price or not self.base_quantity:
            log.warning(
                f'Trade current_price ({self.current_price}) or base_quantity '
                f'({self.base_quantity}) not set up properly! Neither can be zero.'
            )
        return False if not self.ticker_symbol or not self.side \
            or not self.base_quantity or not self.current_price else True

#   @pysnooper.snoop()
    def check_filter_lot_size(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'LOT_SIZE',
            'minQty': '0.10000000',
            'maxQty': '90000.00000000',
            'stepSize': '0.10000000'
        }, ...]

        [ NOTE ]: LOT_SIZE is a filter parameter in the Binance API that sets
            the minimum and maximum allowable quantity for an order on a given
            trading pair. This filter is designed to prevent users from placing
            orders that are too small or too large, which could potentially
            disrupt the market.

        [ NOTE ]: The LOT_SIZE filter takes three values: "minQty", "maxQty",
            and "stepSize". The "minQty" value sets the minimum allowable quantity
            for an order, the "maxQty" value sets the maximum allowable quantity,
            and the "stepSize" value sets the allowable quantity increments.

        [ NOTE ]: Enforcing the LOT_SIZE filter can be done through the Binance
            API when placing orders. When making an order request, the user can
            specify the "newOrderRespType" parameter as "FULL" to receive a
            detailed response from the API, including any error messages if the
            order is rejected due to the filter. If the user attempts to place
            an order with a quantity outside of the allowable range or in a
            quantity increment that is not allowed, the API will return an error
            indicating that the order is not within the allowed range.

        [ NOTE ]: It is important to note that the LOT_SIZE filter is enforced
            on the server-side, meaning that if a user attempts to place an order
            outside of the allowable range through other means (such as the Binance
            website or mobile app), the order will still be rejected.
        '''
        log.debug('')
        trade_filter = self.filters.get('LOT_SIZE')
        if not trade_filter:
            log.warning(f'No data found on trade filter LOT_SIZE! Skipping..')
            return True
        # We enforce the LOT_SIZE filter settings by rounding the quantity value
        # to the appropriate precision based on the stepSize value from the
        # LOT_SIZE filter settings.
        step_size = float(trade_filter['stepSize'])
        quantity_precision = int(round(-1 * math.log(step_size, 10)))
        if self.base_quantity:
            self.base_quantity = float(
                Decimal(self.base_quantity).quantize(Decimal(str(step_size)))
            )
        if self.quote_quantity:
            self.quote_quantity = float(
                Decimal(self.quote_quantity).quantize(Decimal(str(step_size)))
            )
        return True

#   @pysnooper.snoop()
    def check_filter_market_lot_size(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'MARKET_LOT_SIZE',
            'minQty': '0.00000000',
            'maxQty': '10000.00000000',
            'stepSize': '0.00000000'
        }, ...]

        [ NOTE ]: MARKET_LOT_SIZE is a filter parameter in the Binance API that
            sets the minimum and maximum allowable quantity for a market order.
            This filter is designed to prevent users from placing orders that
            are too small or too large, which could potentially disrupt the market.

        [ NOTE ]: The MARKET_LOT_SIZE filter takes three values: "minQty",
            "maxQty", and "stepSize". The "minQty" value sets the minimum allowable
            quantity for a market order, the "maxQty" value sets the maximum
            allowable quantity, and the "stepSize" value sets the allowable
            quantity increments.

        [ NOTE ]: Enforcing the MARKET_LOT_SIZE filter can be done through the
            Binance API when placing market orders. When making an order request,
            the user can specify the "newOrderRespType" parameter as "FULL" to
            receive a detailed response from the API, including any error messages
            if the order is rejected due to the filter. If the user attempts to
            place a market order with a quantity outside of the allowable range
            or in a quantity increment that is not allowed, the API will return
            an error indicating that the order is not within the allowed range.

        [ NOTE ]: It is important to note that the MARKET_LOT_SIZE filter is
            enforced on the server-side, meaning that if a user attempts to place
            a market order outside of the allowable range through other means
            (such as the Binance website or mobile app), the order will still be
            rejected.
        '''
        log.debug('')
        trade_filter = self.filters.get('MARKET_LOT_SIZE')
        if not self.current_price or not self.quote_quantity:
            log.error(
                f'Trade parameters current_price ({self.current_price}) or '
                f'base_quantity ({self.quote_quantity}) not set up properly! '
                'Neither can be zero.'
            )
            return False
        elif not trade_filter:
            log.warning(f'No data found on trade filter MARKET_LOT_SIZE! Skipping..')
            return True
        # We then enforce the MARKET_LOT_SIZE filter settings by rounding the
        # order quantity down to the nearest stepSize value, and adjusting it
        # to the minimum or maximum allowed quantity if it falls outside the
        # allowed range. We then calculate the order quantity in the base asset
        # using the current price of the trading pair.
        min_qty = float(trade_filter['minQty'])
        max_qty = float(trade_filter['maxQty'])
        step_size = float(trade_filter['stepSize'])
        if step_size <= 0:
            rounded_qty = self.quote_quantity
        else:
            rounded_qty = self.quote_quantity - (self.quote_quantity % step_size)
        if rounded_qty < min_qty:
            rounded_qty = min_qty
        elif rounded_qty > max_qty:
            rounded_qty = max_qty
        # Calculate order quantity in base asset
        self.quote_quantity = rounded_qty / self.current_price
        return True

    # WARNING - Unused
    def check_filter_iceberg_parts(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'ICEBERG_PARTS',
            'limit': 10
        }, ...]

        [ NOTE ]: ICEBERG_PARTS is a filter parameter in the Binance API that
            sets the maximum number of "iceberg" orders that can be placed for
            a single symbol. An iceberg order is a type of order that allows a
            large order to be split into smaller, hidden orders, which are then
            executed over time. The ICEBERG_PARTS filter is designed to prevent
            users from placing too many iceberg orders for a single symbol,
            which could potentially disrupt the market.

        [ NOTE ]: The ICEBERG_PARTS filter takes a single integer value that
            represents the maximum number of iceberg orders that can be placed
            for a single symbol. This value ranges from 1 to 10,000, and is
            enforced on a per-account basis.

        [ NOTE ]: Enforcing the ICEBERG_PARTS filter can be done through the
            Binance API when placing iceberg orders. When making an order request,
            the user can specify the "newOrderRespType" parameter as "FULL" to
            receive a detailed response from the API, including any error messages
            if the order is rejected due to the filter. If the user attempts to
            place an iceberg order that exceeds the allowable number of parts for
            the symbol, the API will return an error indicating that the order is
            not within the allowed range.

        [ NOTE ]: It is important to note that the ICEBERG_PARTS filter is enforced
            on the server-side, meaning that if a user attempts to place iceberg
            orders that exceed the allowable number of parts through other means
            (such as the Binance website or mobile app), the orders will still
            be rejected.
        '''
        log.debug('[ WARNING ]: Excluded from filter checks.')
        trade_filter = self.filters.get('ICEBERG_PARTS')
        if not trade_filter:
            log.warning(f'No data found on trade filter ICEBERG_PARTS! Skipping..')
            return True
        # We enforce the ICEBERG_PARTS filter settings by calculating the maximum
        # quantity per part based on the total quantity of the order, and comparing
        # it to the maxQtyPerPart value from the filter settings. If the calculated
        # value is greater than the maxQtyPerPart value, we adjust the icebergQty
        # parameter to the maximum allowed value, and update the quantity parameter
        # accordingly.
        max_iceberg_parts = int(trade_filter['limit'])
        max_qty_per_part = self.iceberg_quantity / max_iceberg_parts
        if self.iceberg_quantity > max_iceberg_parts:
            self.iceberg_quantity = max_iceberg_parts
            self.base_quantity = max_qty_per_part * self.iceberg_qty
        return True

    # WARNING - Unused
    def check_filter_trailing_delta(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'TRAILING_DELTA',
            'minTrailingAboveDelta': 10,
            'maxTrailingAboveDelta': 2000,
            'minTrailingBelowDelta': 10,
            'maxTrailingBelowDelta': 2000
        }, ...]

        [ NOTE ]: TRAILING_DELTA is a filter parameter in the Binance API that
            is used to set the allowable price range for a trailing stop order.
            A trailing stop order is a type of order that is designed to
            automatically adjust the stop loss price as the market price moves
            in a favorable direction. The TRAILING_DELTA filter is designed to
            prevent users from placing trailing stop orders with a too wide
            range of price variation.

        [ NOTE ]: The TRAILING_DELTA filter takes a floating-point value that
            represents the allowable price range for the trailing stop order.
            This value is expressed as a percentage of the market price at the
            time the order is placed. For example, if the TRAILING_DELTA value
            is set to 0.05 (5%), and the market price is $100, the trailing stop
            order will be adjusted as the market price moves, but the new stop
            loss price will not be more than 5% away from the current market price.

        [ NOTE ]: Enforcing the TRAILING_DELTA filter can be done through the
            Binance API when placing a trailing stop order. When making an order
            request, the user can specify the "newOrderRespType" parameter as
            "FULL" to receive a detailed response from the API, including any
            error messages if the order is rejected due to the filter. If the
            user attempts to place a trailing stop order with a TRAILING_DELTA
            value outside of the allowable range, the API will return an error
            indicating that the order is not within the allowed range.

        [ NOTE ]: It is important to note that the TRAILING_DELTA filter is
            enforced on the server-side, meaning that if a user attempts to place
            a trailing stop order with a TRAILING_DELTA value outside of the
            allowable range through other means (such as the Binance website or
            mobile app), the order will still be rejected.

        [ NOTE ]: The TRAILING_DELTA filter is a useful tool for managing risk
            and maintaining stability in the market, and users should ensure they
            are aware of the filter settings for any trailing stop orders they
            are working with to avoid any potential errors or disruptions.
        '''
        log.debug('[ WARNING ]: Excluded from filter checks.')
        trade_filter = self.filters.get('TRAILING_DELTA')
        if not trade_filter:
            log.warning(f'No data found on trade filter TRAILING_DELTA! Skipping..')
            return True
        # We extract the minimum and maximum values for this filter, and define
        # the trailing delta value for the order.
        trailing_delta_min = float(trade_filter['minQty'])
        trailing_delta_max = float(trade_filter['maxQty'])
        # Finally, we enforce the filter by checking if the trailing delta is
        # within the allowed range, and adjust it if necessary before placing
        # the OCO order. Get the minimum and maximum values for the
        # TRAILING_STOP_MARKET filter
        if self.trailing_delta < trailing_delta_min:
            self.trailing_delta = trailing_delta_min
        elif self.trailing_delta > trailing_delta_max:
            self.trailing_delta = trailing_delta_max
        return True

    # TODO
    def check_filter_max_num_orders(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'MAX_NUM_ORDERS',
            'maxNumOrders': 200
        }, ...]

        [ NOTE ]: MAX_NUM_ORDERS is a filter parameter in the Binance API that
            sets the maximum number of open orders that can be placed by a user
            for a specific trading pair. This filter is designed to prevent users
            from placing an excessive number of orders and potentially disrupting
            the market.

        [ NOTE ]: The MAX_NUM_ORDERS filter takes an integer value and can be set
            on a per-symbol basis. For example, if the filter is set to 100 for a
            particular trading pair, a user can only have up to 100 open orders
            for that pair at any given time. If the user attempts to place additional
            orders, the API will return an error indicating that the maximum number
            of orders has been exceeded.

        [ NOTE ]: Enforcing the MAX_NUM_ORDERS filter can be done through the
            Binance API when placing orders. When making an order request, the
            user can specify the "newOrderRespType" parameter as "FULL" to receive
            a detailed response from the API, including any error messages if the
            order is rejected due to the filter. It is important to note that the
            MAX_NUM_ORDERS filter is enforced on the server-side, meaning that if
            a user has open orders through other means (such as the Binance website
            or mobile app), those orders will also be counted towards the maximum
            number allowed.

        [ NOTE ]: Additionally, the MAX_NUM_ORDERS filter can be set in combination
            with the MAX_NUM_ALGO_ORDERS filter to further limit the number of
            open orders a user can have for a specific trading pair. This can
            help prevent excessive market activity and reduce the risk of unintended
            consequences from large numbers of open orders.
        '''
        log.debug('TODO - Unimplemented')
        trade_filter = self.filters.get('MAX_NUM_ORDERS')
        if not trade_filter:
            log.warning(f'No data found on trade filter MAX_NUM_ORDERS! Skipping..')
        return True

    # TODO
    def check_filters_max_num_algo_orders(self, filters: dict) -> bool:
        '''
        [ INPUT ]: *filters - [{
            'filterType': 'MAX_NUM_ALGO_ORDERS',
            'maxNumAlgoOrders': 5
        }, ...]

        [ NOTE ]: MAX_NUM_ALGO_ORDERS is a filter parameter in the Binance API
            that sets the maximum number of open stop-loss, take-profit, and
            other algorithmic orders that can be placed by a user for a specific
            trading pair. This filter is designed to prevent users from placing
            an excessive number of orders and potentially disrupting the market.

        [ NOTE ]: The MAX_NUM_ALGO_ORDERS filter takes an integer value and can
            be set on a per-symbol basis. For example, if the filter is set to
            10 for a particular trading pair, a user can only have up to 10 open
            algorithmic orders for that pair at any given time. If the user attempts
            to place additional orders, the API will return an error indicating
            that the maximum number of orders has been exceeded.

        [ NOTE ]: Enforcing the MAX_NUM_ALGO_ORDERS filter can be done through
            the Binance API when placing orders. When making an order request,
            the user can specify the "newOrderRespType" parameter as "FULL" to
            receive a detailed response from the API, including any error messages
            if the order is rejected due to the filter. It is important to note
            that the MAX_NUM_ALGO_ORDERS filter is enforced on the server-side,
            meaning that if a user has open algorithmic orders through other
            means (such as the Binance website or mobile app), those orders will
            also be counted towards the maximum number allowed.

        [ NOTE ]: The MAX_NUM_ALGO_ORDERS filter is a useful tool for maintaining
            order and stability in the market, and users should ensure they are
            aware of the filter settings for any trading pairs they are working
            with to avoid any potential errors or disruptions.
        '''
        log.debug('TODO - Unimplemented')
        trade_filter = self.filters.get('MAX_NUM_ALGO_ORDERS')
        if not trade_filter:
            log.warning(f'No data found on trade filter MAX_NUM_ALGO_ORDERS! Skipping..')
        return True

    def check_time_until_expires(self) -> int:
        '''
        [ RETURN ]: Number of seconds until trade opportunity expires. If the
            trade will not be commited in this time it will no longer be viable
            and the TradingMarket will refuse to execute it.
        '''
        log.debug('')
        if self.check_expired():
            return 0
        now = datetime.datetime.now()
        tdelta = self.expires_on - now
        return int(tdelta.total_seconds())

    def check_expired(self):
        '''
        [ NOTE ]: First it checks if a datetime.datetime object is set to
            expires_on, and if is, verifies if its in the future or the past
            relative to the current datetime.
        '''
        log.debug('')
        if not self.expires_on:
            return False
        now = datetime.datetime.now()
        return now > self.expires_on

    def check_preconditions_draft(self):
        log.debug('')
        if not self.risk or not self.trade_fee:
            log.warning(
                f'Trade risk index ({self.risk}) or trade_fee ({self.trade_fee}) '
                'not set up properly! Neither can be zero.'
            )
        return False if not self.risk or not self.trade_fee else True

    def check_preconditions_commited(self):
        log.debug('')
        if not self.result:
            log.warning(
                f'Result ({self.result}) not set up properly! Must be set.'
            )
        return False if not self.result else True

    def check_preconditions_done(self):
        log.debug('')
        if self.expires_on:
            log.warning(
                f'Trade expiration date cannot be set in state {self.status}! '
                'Currently set to ({})'.format(self.expires_on.strftime(
                    self._context.get('timestamp-format', '%d-%m-%Y %H:%M:%S')
                ))
            )
        return False if self.expires_on else True

    # UPDATES

#   @pysnooper.snoop()
    def update(self, **new_data) -> bool:
        '''
        [ NOTE ]: Updates the following Trade parameters in a single GO:
            * trade_id
            * ticker_symbol
            * status
            * risk'
            * base_quantity
            * quote_quantity
            * side
            * current_price
            * stop_loss_price
            * take_profit_price
            * price_percent_change
            * trailing_delta
            * trade_fee
        '''
        log.debug('')
        if not new_data:
            return False
        state = self.status
        self.__dict__.update({
            'trade_id': str(new_data.get('trade-id', self.trade_id)),
            'ticker_symbol': str(new_data.get('ticker-symbol', self.ticker_symbol)).replace('/', ''),
            'status': str(new_data.get('status', self.status)),
            'risk': int(new_data.get('risk', self.risk)),
            'base_quantity': new_data.get('base_quantity', self.base_quantity) or float(),
            'quote_quantity': new_data.get('quote_quantity', self.quote_quantity) or float(),
            'side': str(new_data.get('side', self.side)),
            'current_price': float(new_data.get('current_price', self.current_price)),
            'stop_loss_price': float(new_data.get('stop_loss_price', self.stop_loss_price)),
            'take_profit_price': float(new_data.get('take_profit_price', self.take_profit_price)),
            'trade_fee': float(new_data.get('trade_fee', self.trade_fee)),
            'price_percent_change': float(new_data.get('price_percent_change', self.price_percent_change)),
            'trailing_delta': float(new_data.get('trailing_delta', self.trailing_delta)),
        })
        if self.status != state:
            self.previous_status = state
        self.write_date = datetime.datetime.now()
        log.debug(f'Updated Trade instance: {self.__dict__}')
        return True

    def update_context(self, **new_updates) -> dict:
        '''
        [ NOTE ]: Merges new context values with the olds ones. If there are
            any duplicate value keys, they are overwritten with the new value.
        '''
        log.debug('')
        self._context.update(new_updates)
        log.debug(f'Trade context updated: {self._context}')
        return self._context

    def update_signals(self, *new_signals) -> list:
        '''
        [ NOTE ]: Adds more Signal() instances that validate this Trade to the
            list.
        '''
        log.debug('')
        self._signals.extend(new_signals)
        log.debug(f'Trade signals updated: {self._signals}')
        return self._signals

    def update_action_history(self, action: str, failed: bool = False, **new_updates) -> dict:
        log.debug('')
        timestamp = fetch_timestamp()
        self._history.update({timestamp: {
            'action': action,
            'failed': failed,
            'details': new_update,
            'context': self._context,
        }})
        log.debug(f'Trade action history updated: {self._history}')
        return self._history

#   @pysnooper.snoop()
    def update_filters(self, *filters):
        log.debug('')
        if not filters:
            return False
        self.filters = {
            item['filterType']: item for item in filters if item.get('filterType')
        }
        log.debug(f'Trade filters updated: {self.filters}')
        return self.filters

    # GENERAL

    def pickle_me_rick(self) -> dict:
        log.debug('')
        pickle_rick = self.__dict__.copy()
        pickle_rick.update({
            '_signals': [str(signal) for signal in pickle_rick['_signals']],
            'create_date': pickle_rick['create_date'].strftime(
                self._context.get('timestamp-format', '%d-%m-%Y %H:%M:%S')
            ),
            'write_date': pickle_rick['write_date'].strftime(
                self._context.get('timestamp-format', '%d-%m-%Y %H:%M:%S')
            ),
        })
        return pickle_rick

#   @pysnooper.snoop()
    def filter_check(self, *filters) -> bool:
        '''
        [ INPUT ]: *filters - [
            {'filterType': 'PRICE_FILTER', 'minPrice': '0.00010000', 'maxPrice': '1000.00000000', 'tickSize': '0.00010000'},
            {'filterType': 'STOP_PRICE_FILTER', 'minPrice': '0.00010000', 'maxPrice': '1000.00000000', 'tickSize': '0.00010000'},
            {'filterType': 'LOT_SIZE', 'minQty': '0.10000000', 'maxQty': '90000.00000000', 'stepSize': '0.10000000'},
            {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 1},
            {'filterType': 'ICEBERG_PARTS', 'limit': 10},
            {'filterType': 'MARKET_LOT_SIZE', 'minQty': '0.00000000', 'maxQty': '10000.00000000', 'stepSize': '0.00000000'},
            {'filterType': 'TRAILING_DELTA', 'minTrailingAboveDelta': 10, 'maxTrailingAboveDelta': 2000, 'minTrailingBelowDelta': 10, 'maxTrailingBelowDelta': 2000},
            {'filterType': 'PERCENT_PRICE_BY_SIDE', 'bidMultiplierUp': '5', 'bidMultiplierDown': '0.2', 'askMultiplierUp': '5', 'askMultiplierDown': '0.2', 'avgPriceMins': 1},
            {'filterType': 'MAX_NUM_ORDERS', 'maxNumOrders': 200},
            {'filterType': 'MAX_NUM_ALGO_ORDERS', 'maxNumAlgoOrders': 5}
        ]

        [ NOTE ]: Called on preconditions check when current state is EVALUATED

        [ WARNING ]: The following filters are currently ignored -
            * ICEBERG_PARTS
            * TRAILING_DELTA
            * MAX_NUM_ORDERS
            * MAX_NUM_ALGO_ORDERS
        '''
        log.debug('')
        filters = self.update_filters(*filters)
        if not filters:
            return False
        failures, checkers = 0, {
            'PRICE_FILTERS': self.check_filter_price,
            'LOT_SIZE': self.check_filter_lot_size,
            'MIN_NOTIONAL': self.check_filter_min_notional,
            'MARKET_LOT_SIZE': self.check_filter_market_lot_size,
            'PERCENT_PRICE_BY_SIDE': self.check_filter_percent_price_by_side,
            'STOP_PRICE_FILTERS': self.check_filter_stop_loss_price,
#           'ICEBERG_PARTS': self.check_filter_iceberg_parts,
#           'TRAILING_DELTA': self.check_filter_trailing_delta,
#           'MAX_NUM_ORDERS': self.check_filter_max_num_orders,
#           'MAX_NUM_ALGO_ORDERS': self.check_filters_max_num_algo_orders,
        }
        for check in checkers:
            result = checkers[check](filters)
            if not result:
                failures += 1
        if failures:
            log.debug(f'{failures} errors detected during Trade filter check!')
        return False if failures else True

    # ACTIONS

    def expire(self) -> bool:
        log.debug('')
        return self.set_state(self.STATUS_EXPIRED)

    def discard(self) -> bool:
        log.debug('')
        return self.set_state(self.STATUS_DISCARDED)

    def next_state(self) -> bool:
        '''
        [ NOTE ]: Acts as a jump-table for unspecified state transitions
        '''
        log.debug('')
        current_state = self.status
        if current_state in (
                self.STATUS_DONE, self.STATUS_DISCARDED, self.STATUS_EXPIRED):
            return False
        state_changers =  {
            self.STATUS_DRAFT: self.set_evaluated,
            self.STATUS_EVALUATED: self.set_commited,
            self.STATUS_COMMITED : self.set_done,
        }
        return state_changers[current_state]()

    def previous_state(self) -> bool:
        log.debug('')
        if not self.previous_status:
            return False
        return self.set_state(self.previous_status)

    def unpack(self, **context) -> dict:
        '''
        [ NOTE ]: Unpacks Trade instance data into kwargs for binance.create_oco_order():

        [ RETURN ]: {
            'symbol':               self.ticker_symbol,
            'side':                 self.side,
            'quantity':             self.base_quantity,
            'price':                self.take_profit_price,
            'stopPrice':            self.stop_loss_price,
            'type':                 self.ORDER_TYPE,
            'newOrderRespType':     self.ORDER_RESPONSE_TYPE,
            'timeInForce':          self.ORDER_TIME_IN_FORCE,
            'newClientOrderID':     self.trade_id,
            'recvWindow':           context.get(
                'recv-window', self._context.get('recv-window', 60000)
            )
        }
        '''
        log.debug('')
        if not self.ticker_symbol or not self.side or not self.base_quantity \
                or not self.current_price:
            return False
        return {
            'symbol':               self.ticker_symbol,
            'side':                 self.side,
            'quantity':             round(self.base_quantity, 8),
            'price':                round(float(self.take_profit_price), 8),     #round(float(self.current_price), 8),
            'stopPrice':            round(float(self.stop_loss_price), 8),       #round(self.take_profit_price, 8),
            'type':                 self.ORDER_TYPE,
            'newOrderRespType':     self.ORDER_RESPONSE_TYPE,
            'timeInForce':          self.ORDER_TIME_IN_FORCE,
            'newClientOrderId':     self.trade_id,
            'recvWindow':           context.get(
                'recv-window', self._context.get('recv-window', 60000)
            ),
        }

# CODE DUMP

