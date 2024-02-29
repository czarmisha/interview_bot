import logging, datetime
from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    filters,
)

from sqlalchemy import select
from database.models import (
    Session,
    engine,
    Application,
    admin_ids,
)

session = Session(bind=engine)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

FINAL = range(1)
# TODO: do logging
async def mark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tg_id = user.id
    if str(tg_id) in admin_ids:
        text = "Отправьте номер/а заявки/вок, которые были обработаны.\n"\
                "если заявка одна просто отправьте ее номер (пример: 1), "\
                "если заявок много - отправьте номера заявок через запятую без пробела (пример: 1,2,3)"\
                "для отмены /cancel"
        await update.message.reply_text(text)
        return FINAL
    else:
        await update.message.reply_text("Эта команда только для администраторов.\n Для регистрации попробуйте /start")
        return ConversationHandler.END
    
async def final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tg_id = user.id
    if str(tg_id) in admin_ids:
        message = update.message.text
        if ',' in message:
            ids = message.strip().split(',')
            for id in ids:
                if not id.isdigit():
                    await update.message.reply_text("Проверьте формат данных! Номера заявок - числа, разделенные запятой и все. (1,2,3,4,5)\nДля отмены /cancel")
                    return FINAL
            for id in ids:
                stmt = select(Application).where(Application.id==int(id))
                application = session.execute(stmt).scalars().first()
                if not application:
                    await update.message.reply_text(f"Заявка с номером {id} не найдена.")
                    continue
                application.processed = True
                session.add(application)
                session.commit()
        else:
            id = message.strip()
            if not id.isdigit():
                await update.message.reply_text("Проверьте формат данных! Номер заявки - число (1)\nДля отмены /cancel")
                return FINAL
            stmt = select(Application).where(Application.id==int(id))
            application = session.execute(stmt).scalars().first()
            if not application:
                await update.message.reply_text("Заявка с таким номером не найдена. Отправьте еще раз!\nДля отмены /cancel")
                return FINAL
            application.processed = True
            session.add(application)
            session.commit()

        text = "---------------------------\n"\
               "/mark - отметить заявку/и как обработанные\n"\
               "/get_unmarked - список необработанных заявок\n"\
               "/statistic - статистика\n"
        await update.message.reply_text("Готово!\n\n" + text)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Эта команда только для администраторов.\n Для регистрации попробуйте /start")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Вы отменили регистрацию \nКоманда для регистрации - /start"
    )

    return ConversationHandler.END

async def timeout(update, context):
   await update.message.reply_text('Вы бездействовали больше 15 минут. Сеанс регистрации отменен.\n\nМожете начать регистрацию заново командой /start')
   return ConversationHandler.END

mark_handler = ConversationHandler(
        entry_points=[CommandHandler('mark', mark)],
        states={
            FINAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, final)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.ALL, timeout)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=datetime.timedelta(seconds=900)
    )
