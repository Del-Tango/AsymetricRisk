# **(A)Risk**

[ **Description** ]: Crypto trading bot for Binance - now integrated with
TeleVision (a telegram messaging bot) ever since v1.1AR15.

[ **Dox** ]: Read up on how to configure the bot

    ~$ ./dox/ar_setup.dox

[ **Setup** ]: Install project dependencies and configure for live runs

    ~$ ./asymetric-risk --setup

[ **Test** ]: Run (A)RAT suit - (A)Risk Auto Testers

    ~$ ./tst/test_asymetric_risk.sh full

[ **Example** ]: Start trading bot in debug mode with the telegram support extension

    ~$ ./asymetric-risk --config-file=conf/asymetric_risk.conf.json --log-file=log/asymetric_risk.log --action=start-watchdog --television --debug
