import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

from database.models import (
    admin_ids
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def command_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tg_id = user.id
    if str(tg_id) in admin_ids:
        text = "/mark - отметить заявку/и как обработанные\n"\
               "/get_unmarked - список необработанных заявок\n"\
               "/statistic - статистика\n"
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Эта команда только для администраторов.\n Для регистрации попробуйте /start")


command_list_handler = CommandHandler('command_list', command_list)
