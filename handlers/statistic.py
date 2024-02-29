import logging, datetime, re
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
)

from sqlalchemy import select
from database.models import (
    Session,
    engine,
    Application,
    admin_ids,
)
from utils.keyboards import (
    statistic_keyboard,
)
from utils.build_text import build_text
from utils.statistic import Statistic

session = Session(bind=engine)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TYPE = range(1)
# TODO: do logging
async def statistic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tg_id = user.id
    if str(tg_id) in admin_ids:
        text = "Выберите за какой период вам нужна статистика"
        keyboard = statistic_keyboard()
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return TYPE
    else:
        await update.message.reply_text("Эта команда только для администраторов.\n Для регистрации попробуйте /start")
        return ConversationHandler.END

    

async def type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    user = update.effective_user
    tg_id = user.id
    if not str(tg_id) in admin_ids:
        await update.message.reply_text("Эта команда только для администраторов.\n Для регистрации попробуйте /start")
        return ConversationHandler.END
    
    answer = query.data.split('_')[1]
    commands = "---------------------------\n"\
               "/mark - отметить заявку/и как обработанные\n"\
               "/get_unmarked - список необработанных заявок\n"\
               "/statistic - статистика\n"

    statistic = Statistic(answer)
    text = statistic.get_stat()
    
    await query.edit_message_text(text=text + "\n\n" + commands)
    return ConversationHandler.END

async def query_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    query.answer()
    await query.edit_message_text(
        text="Вы отменили регистрацию \nКоманда для регистрации - /start"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Вы отменили регистрацию \nКоманда для регистрации - /start"
    )

    return ConversationHandler.END

async def timeout(update, context):
   await update.message.reply_text('Вы бездействовали больше 15 минут. Сеанс регистрации отменен.\n\nМожете начать регистрацию заново командой /start')
   return ConversationHandler.END

statistic_handler = ConversationHandler(
        entry_points=[CommandHandler('statistic', statistic)],
        states={
            TYPE: [
                CallbackQueryHandler(type, pattern='^type_'),
                CallbackQueryHandler(query_cancel, pattern='^cancel$'),
            ],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, timeout)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=datetime.timedelta(seconds=900)
    )
