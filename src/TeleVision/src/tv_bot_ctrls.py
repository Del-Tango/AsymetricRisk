#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# BOT CTRLS

import logging
import asyncio

from src.backpack.bp_general import write2file, read_file

log = logging.getLogger('TeleVision')

# [ NOTE ]: Put you custom bot command functions here and don't forget to add
# them to the BOT_CTRL_INDEX dictionary.

def update_arisk_input_file(command):
    return write2file(
        command, mode='a', file_path=TV_DEFAULT['out-file']
    )

async def start(update, context):
    '''
    [ NOTE ]: Function that will be called when the /start command is received
    '''
    log.debug('')
    await update.message.reply_text('Welcome to (A)Risky TeleVision!')

async def help(update, context):
    '''
    [ NOTE ]: Function that will be called when the /help command is received
    '''
    log.debug('')
    await update.message.reply_text("Smile! You're on (A)Risky TeleVision!")

async def error(update, context):
    '''
    [ NOTE ]: Log Errors caused by Updates.
    '''
    log.error(
        'Update ({}) caused ({})'.format(update, context.error)
    )

async def echo(update, context):
    await update.message.reply_text(update.message.text)

async def confirm(update, context):
    '''
    [ NOTE ]: Function that will be called when the /confirm command is received
    [ INPUT ]: Trade ID CSV
    [ EX ]: /confirm <trade-id>,<trade-id>
    [ RETURN ]: Displays (A)Risk action exit code
    '''
    update_arisk_input_file(update.message.text)
    await update.message.reply_text(
        '[ INFO ]: Processing confirmation of risky trade...'
    )

async def deny(update, context):
    '''
    [ NOTE ]: Function that will be called when the /deny command is received
    [ INPUT ]: Trade ID CSV
    [ EX ]: /deny <trade-id>,<trade-id>
    [ RETURN ]: Displays (A)Risk action exit code
    '''
    update_arisk_input_file(update.message.text)
    await update.message.reply_text(
        '[ INFO ]: Processing rejection of risky trade...'
    )

async def state(update, context):
    '''
    [ NOTE ]: Function that will be called when the /state command is received
    [ EX ]: /state
    [ RETURN ]: Displays (A)Risk state - account/market/trade/system details
    '''
    update_arisk_input_file(update.message.text)
    await update.message.reply_text('[ INFO ]: Processing (A)Risk state check...')

async def kill(update, context):
    '''
    [ NOTE ]: Function that will be called when the /kill command is received
    [ EX ]: /kill
    [ RETURN ]: Displays (A)Risk state
    '''
    update_arisk_input_file(update.message.text)
    await update.message.reply_text('[ DONE ]: Terminating...')

BOT_CTRL_INDEX = {
    'start': start,
    'help': help,
    'echo': echo,
    'error': error,
    'confirm': confirm,
    'deny': deny,
    'state': state,
    'kill': kill,
}

