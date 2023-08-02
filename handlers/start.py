import logging, datetime
from telegram import Update, ForceReply, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
)

from sqlalchemy import select
from db.models import (
    Session,
    engine,
    Candidate,
    Company,
    Application
)
from utils.keyboards import (
    agreement_keyboard,
    about_keyboard,
)

session = Session(bind=engine)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

AGREEMENT, FIO, PHONE, BIRTH, EDUCATION, ENGLISH, FAMILY, RESUME, SOURCE, ABOUT = range(10)
CONVERSATION_TIMEOUT = 900

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        candidate = Candidate(tg_id =user.id, chat_id=update.effective_chat.id)
        session.add(candidate)
        session.commit()

    keyboard = agreement_keyboard()
    await update.message.reply_text("Регистрируясь, я даю своё согласие на обработку персональных данных", reply_markup=InlineKeyboardMarkup(keyboard))

    return AGREEMENT

async def agreement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    answer = query.data.split('_')[1]
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await query.edit_message_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END

    if answer == '0':
        candidate.agreement = False
        session.add(candidate)
        session.commit()
        await query.edit_message_text(text="Спасибо за потраченное время.\n\nНачать регистрацию заново - /start")
        return ConversationHandler.END
    else:
        candidate.agreement = True
        session.add(candidate)
        session.commit()
    
    await query.edit_message_text(text="Здравствуйте! Регистрация займет у вас не больше 5 минут.\n\n Укажите как Вас зовут (ФИО)")
    return ConversationHandler.FIO

async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    full_name = update.message.text
    candidate.full_name = full_name
    session.add(candidate)
    session.commit()

    await update.message.reply_text("Укажите свой телефон в формате +998xxxxxxx")
    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    phone_num = update.message.text
    # TODO: validate phone_num
    candidate.phone = phone_num
    session.add(candidate)
    session.commit()

    await update.message.reply_text("Укажите дату рождения в формате дд.мм.гггг")
    return BIRTH

async def birth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    date = update.message.text
    # TODO: validate date
    candidate.birth_date = date.strptime(date, "%d.%m.%Y")
    session.add(candidate)
    session.commit()

    await update.message.reply_text("Укажите ВУЗ в котором обучаетесь/лись с указание направления(факультета)")
    return EDUCATION

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    education_mess = update.message.text
    candidate.education = education_mess
    session.add(candidate)
    session.commit()

    await update.message.reply_text("Укажите свой уровень английского")
    return ENGLISH

async def english(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    language = update.message.text
    candidate.english_level = language
    session.add(candidate)
    session.commit()

    await update.message.reply_text("Укажите свое семейное положение")
    return FAMILY

async def family(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    family_status = update.message.text
    candidate.family_status = family_status
    session.add(candidate)
    session.commit()

    await update.message.reply_text("Укажите откуда вы узнали о нас (инстаграм, от друга, канал вашего вуза и тд.)")
    return RESUME

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    # family_status = update.message.text
    # candidate.family_status = family_status
    # session.add(candidate)
    # session.commit()

    await update.message.reply_text("Укажите откуда вы узнали о нас (инстаграм, от друга, канал вашего вуза и тд.)")
    return SOURCE

async def source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END
    
    family_status = update.message.text
    candidate.family_status = family_status
    session.add(candidate)
    session.commit()
    
    keyboard = about_keyboard()
    await update.message.reply_text("Вы что-нибудь знаете о нашей компании? (слышали от друга, работали раньше и тд.)", reply_markup=InlineKeyboardMarkup(keyboard))
    return ABOUT

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    answer = query.data.split('_')[1]
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await query.edit_message_text(text="Произошла ошибка, обратитесь к администратору")
        return ConversationHandler.END

    if answer == '0':  #TODO:
        candidate.agreement = False
        session.add(candidate)
        session.commit()
        await query.edit_message_text(text="Спасибо за потраченное время.\n\nНачать регистрацию заново - /start")
        return ConversationHandler.END
    else:
        candidate.agreement = True
        session.add(candidate)
        session.commit()
    
    await query.edit_message_text(text="Здравствуйте! Регистрация займет у вас не больше 5 минут.\n\n Укажите как Вас зовут (ФИО)")
    return ConversationHandler.FIO

async def conv_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGREEMENT: [
                CallbackQueryHandler(agreement, pattern='^agreement_'),
                CallbackQueryHandler(conv_cancel, pattern='^cancel$'),
            ],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
            ConversationHandler.TIMEOUT: [MessageHandler(filters.TEXT | filters.COMMAND, timeout)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=CONVERSATION_TIMEOUT
    )
