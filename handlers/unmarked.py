import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
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

# TODO: do logging
async def unmarked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tg_id = user.id
    if str(tg_id) in admin_ids:
        text = "---------------------------\n"\
               "/mark - отметить заявку/и как обработанные\n"\
               "/get_unmarked - список необработанных заявок\n"\
               "/statistic - статистика\n"
        stmt = select(Application.id).where(Application.processed!=True)
        applications = session.execute(stmt).scalars().all()
        if not applications:
            await update.message.reply_text("Все заявки обработаны или заявок нет вообще\n\n" + text)
        else:
            ids = [str(app) for app in applications]
            result = ', '.join(ids)
            await update.message.reply_text("Номера всех необработанных заявок:\n" + result + f" (кол-во: {len(ids)})" +"\n\n" + text)
    else:
        await update.message.reply_text("Эта команда только для администраторов.\n Для регистрации попробуйте /start")


unmarked_handler = CommandHandler('get_unmarked', unmarked)
