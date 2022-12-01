#!/bin/bash
#
# Regards, the Alveare Solutions #!/Society -x
#
# AsymetricRisk - (A)Risk - Functional auto-tester

declare -A AR_DEFAULT
declare -A AR_AUTO_TESTERS

AR_INIT='./asymetric_risk.py'

AR_DEFAULT=(
['log-file']="./log/asymetric_risk.log"
['conf-file']="./conf/asymetric_risk.conf.json"
['profit-baby']=20
['watchdog-pid-file']=".ar-bot.pid"
['watchdog-anchor-file']=".ar-bot.anchor"
['log-format']="[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - %(filename)s - %(lineno)d: %(funcName)s - %(message)s"
['timestamp-format']="%d/%m/%Y-%H:%M:%S"
['api-key']="yxdLHNgKWzka2HjzR5jZF0ZXTCZaHp2V1X9EgXjKBxLsfKoClFvET1PqIUW9ctAw"
['api-secret']="oPyuIoqWHBt5pvfCk1YLIslViuH87DJvRTgtOsLylGB58LRsEuHvu4KuZOv0DAv5"
['taapi-key']="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MmRkNThmYzVhOGFkZmVjM2ZhMmEzIiwiaWF0IjoxNjY3NzAxNzg5LCJleHAiOjMzMTcyMTY1Nzg5fQ.33yXXi5RK1oupATjS-RFMLKfD7grZdJ2r7GT4gH-tAE"
['api-url']="https://api.binance.com/api"
['taapi-url']="https://api.taapi.io"
['max-trades']=3
['trading-account-type']="SPOT"
['trading-order-type']="LIMIT"
['base-currency']="BTC"
['quote-currency']="USDT"
['ticker-symbol']="BTC/USDT"
['order-time-in-force']="GTC"
['order-response-type']="JSON"
['order-recv-window']=60000
['order-list-id']=""
['order-limit-id']=""
['order-stop-id']=""
['order-iceberg-quantity']=0
['order-price']=0
['order-amount']=1
['stop-loss']=10
['take-profit']=30
['trailing-stop']=10
['test']='off'
['debug']='off'
['silence']='off'
['indicator-update-delay']=18
['risk-tolerance']=5
['analyze-risk']='on'
['strategy']="vwap,rsi,macd,adx,ma,ema,price,volume"
['side']="auto"
['interval']="5m"
['period-start']=""
['period-end']=""
['period']=14
['market-open']="08:00"
['market-close']="22:00"
['backtrack']=5
['backtracks']=14
['stop-limit']=0
['stop-price']=0
['stop-limit-price']=0
['stop-iceberg-quantity']=0
['stop-limit-time-in-force']="GTC"
['price-movement']=5
['rsi-top']=70
['rsi-bottom']=30
['rsi-period']=14
['rsi-backtrack']=5
['rsi-backtracks']=12
['rsi-chart']="candles"
['rsi-interval']="5m"
['volume-movement']=5
['volume-interval']="5m"
['ma-period']=30
['ma-backtrack']=5
['ma-backtracks']=12
['ma-chart']="candles"
['ma-interval']="5m"
['ema-period']=30
['ema-backtrack']=5
['ema-backtracks']=12
['ema-chart']="candles"
['ema-interval']="5m"
['macd-backtrack']= 5
['macd-backtracks']=12
['macd-chart']="candles"
['macd-fast-period']=12
['macd-slow-period']=26
['macd-signal-period']=9
['macd-interval']="5m"
['adx-period']=14
['adx-backtrack']=5
['adx-backtracks']=12
['adx-chart']="candles"
['adx-interval']="5m"
['vwap-period']=14
['vwap-backtrack']=5
['vwap-backtracks']=12
['vwap-chart']="candles"
['vwap-interval']="5m"
['price-period']=14
['price-backtrack']=5
['price-backtracks']=12
['price-chart']="candles"
['price-interval']="5m"
['report-id']=""
['report-id-length']=8
['report-id-characters']="abcdefghijklmnopqrstuvwxyz0123456789"
['report-location']="./data/reports"
)

AR_AUTO_TESTERS=(
['test-start-watchdog']='test_asymetric_risk_action_start_watchdog',
['test-stop-watchdog']='test_asymetric_risk_action_stop_watchdog',
['test-single-trade']='test_asymetric_risk_action_single_trade',
['test-generate-report']='test_asymetric_risk_action_generate_report',
['test-list-reports']='test_asymetric_risk_action_list_reports',
['test-read-reports']='test_asymetric_risk_action_read_reports',
['test-remove-reports']='test_asymetric_risk_action_remove_reports',
['test-help']='test_asymetric_risk_help',
)

# AUTOTESTERS

# TODO
function test_asymetric_risk_action_start_watchdog() {
    echo 'TODO - Under construction'
}
function test_asymetric_risk_action_stop_watchdog() {
    echo 'TODO - Under construction'
}
function test_asymetric_risk_action_single_trade() {
    echo 'TODO - Under construction'
}
function test_asymetric_risk_action_generate_report() {
    echo 'TODO - Under construction'
}
function test_asymetric_risk_action_list_reports() {
    echo 'TODO - Under construction'
}
function test_asymetric_risk_action_read_reports() {
    echo 'TODO - Under construction'
}
function test_asymetric_risk_action_remove_reports() {
    echo 'TODO - Under construction'
}
function test_asymetric_risk_help() {
    echo 'TODO - Under construction'
}

# FORMATTERS

# TODO
function format_asymetric_risk_action_start_watchdog() {
    echo 'TODO - Under construction'
function format_asymetric_risk_action_stop_watchdog() {
    echo 'TODO - Under construction'
function format_asymetric_risk_action_single_trade() {
    echo 'TODO - Under construction'
function format_asymetric_risk_action_generate_report() {
    echo 'TODO - Under construction'
function format_asymetric_risk_action_list_reports() {
    echo 'TODO - Under construction'
function format_asymetric_risk_action_read_reports() {
    echo 'TODO - Under construction'
function format_asymetric_risk_action_remove_reports() {
    echo 'TODO - Under construction'
function format_asymetric_risk_action_remove_reports() {
    echo 'TODO - Under construction'
#   local ARGUMENTS=(

#   )
#   echo ${ARGUMENTS[@]}
    return $?

function format_asymetric_risk_constant_args() {
    local ARGUMENTS=(
        "--log-file ${AR_DEFAULT['log-file']}"
        "--config-file ${AR_DEFAULT['conf-file']}"
    )
    if [[ ${AR_DEFAULT['silence']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--silence' )
    fi
    if [[ ${AR_DEFAULT['debug']} == 'on' ]]; then
        local ARGUMENTS=( ${ARGUMENTS[@]} '--debug' )
    fi
    echo -n "${ARGUMENTS[@]}"
    return $?
}

function format_init_script_arguments() {
    local AUTOTESTER="$1"
    case "$AUTOTESTER" in
        'test-start-watchdog')
            format_asymetric_risk_action_start_watchdog
            ;;
        'test-stop-watchdog')
            format_asymetric_risk_action_stop_watchdog
            ;;
        'test-single-trade')
            format_asymetric_risk_action_single_trade
            ;;
        'test-generate-report')
            format_asymetric_risk_action_generate_report
            ;;
        'test-list-reports')
            format_asymetric_risk_action_list_reports
            ;;
        'test-read-reports')
            format_asymetric_risk_action_read_reports
            ;;
        'test-remove-reports')
            format_asymetric_risk_action_remove_reports
            ;;
        'test-help')
            format_asymetric_risk_action_remove_reports
            ;;
        *)
            echo "[ WARNING ]: Invalid autotester label! (${AUTOTESTER})"
            return 1
            ;;
    esac
    return $?
}

# TRIGGER

function start_auto_tester() {
    local FAILURES=0
    echo "[ TEST ]: Starting AsymetricRisk interface auto-tester..."
    for tester_label in ${!AR_AUTO_TESTERS[@]}; do
        local ARGUMENTS=( `format_init_script_arguments ${tester_label}` )
        ${AR_AUTO_TESTERS[${tester_label}]} ${ARGUMENTS[@]}
        if [ $? -ne 0 ]; then
            local FAILURES=$((FAILURES+1))
            echo "[ NOK ]: Test failed! (${tester_label})"
        else
            echo "[ OK ]: Test passed! (${tester_label})"
        fi
    done
    if [ $FAILURES -eq 0 ]; then
        echo "[ DONE ]: All tests pass!"
    else
        echo "[ WARNING ]: (${FAILURES}) tests failed!"
    fi
    return $FAILURES
}

# MISCELLANEOUS

start_auto_tester()
exit $?
