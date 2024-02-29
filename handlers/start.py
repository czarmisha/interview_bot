import logging, datetime, re
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
    BaseHandler,
)

from sqlalchemy import select
from database.models import (
    Session,
    engine,
    Candidate,
    Company,
    Application,
    channel_id,
)
from utils.keyboards import (
    agreement_keyboard,
    final_keyboard,
    lang_keyboard,
)
from utils.build_text import build_text
from text.start import text
from text.company import company_description


session = Session(bind=engine)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

LANGUAGE, ABOUT, AGREEMENT, FIO, PHONE, BIRTH, EDUCATION, ENGLISH, FAMILY, RESUME, SOURCE, FINAL, REASON = range(13)


# TODO: do logging
# TODO: do statistic for admin only
# TODO: list application and candidates count for period
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        candidate = Candidate(
            tg_id =user.id, chat_id=update.effective_chat.id,
            created=datetime.datetime.now(), last_activity=datetime.datetime.now()
        )
        session.add(candidate)
        session.commit()
        context.chat_data['user_id'] = candidate.id
        lang = 'ru'
        keyboard = lang_keyboard()
        await update.message.reply_text(text['select_lang'][lang], reply_markup=InlineKeyboardMarkup(keyboard))
        return LANGUAGE
    else:
        candidate.last_activity = datetime.datetime.now()
        session.add(candidate)
        session.commit()
        lang = candidate.language
        context.chat_data['lang'] = lang
        context.chat_data['user_id'] = candidate.id
        stmt = select(Application).where(Application.candidate_id==candidate.id)
        application = session.execute(stmt).scalars().first()
        if application and application.completed:
            await update.message.reply_text(text['application_already_completed'][lang])
            return ConversationHandler.END  # TODO: если заявку уже подали но с ним не связались?? 

        await update.message.reply_text(company_description[lang])
        keyboard = final_keyboard(lang)
        await update.message.reply_text(text['what_d_u_think'][lang], reply_markup=InlineKeyboardMarkup(keyboard))

        return ABOUT


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    answer = query.data.split('_')[1]
    user = update.effective_user
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][answer])
        return ConversationHandler.END
    
    candidate.language = answer
    context.chat_data['user_id'] = candidate.id

    session.add(candidate)
    session.commit()

    stmt = select(Application).where(Application.candidate_id==candidate.id)
    application = session.execute(stmt).scalars().first()
    if application and application.completed:
        await update.message.reply_text(text['application_already_completed'][answer])
        return ConversationHandler.END  # TODO: если заявку уже подали но с ним не связались?? 

    await query.edit_message_text(text=company_description[answer])
    keyboard = final_keyboard(answer)
    await query.edit_message_text(text=text['what_d_u_think'][answer], reply_markup=InlineKeyboardMarkup(keyboard))

    return ABOUT


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    answer = query.data.split('_')[1]
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang

    if answer == '0':
        candidate.final_answer = False
        session.add(candidate)
        session.commit()
        await query.edit_message_text(text=text['reason'][lang])
        return REASON
    else:
        candidate.final_answer = True
        session.add(candidate)
        session.commit()
    
    keyboard = agreement_keyboard(lang)
    await query.edit_message_text(text=text['agreement'][lang], reply_markup=InlineKeyboardMarkup(keyboard))
    return AGREEMENT


async def agreement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    answer = query.data.split('_')[1]
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang

    if answer == '0':
        candidate.agreement = False
        session.add(candidate)
        session.commit()
        await query.edit_message_text(text=text['false_agreement'][lang])
        return ConversationHandler.END
    else:
        candidate.agreement = True
        session.add(candidate)
        session.commit()
    
    await query.edit_message_text(text=text['fio'][lang])
    return FIO


async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    full_name = update.message.text
    candidate.full_name = full_name
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['phone'][lang])
    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    phone_num = update.message.text
    pattern = r"^(\+998)[ .,-]?[0-9]{2}[ .,-]?[0-9]{3}[ .,-]?[0-9]{2}[ .,-]?[0-9]{2}$"
    if not re.match(pattern, phone_num):
        await update.message.reply_text(text['phone_format'][lang])
        return PHONE

    candidate.phone = phone_num
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['birth'][lang])
    return BIRTH


async def birth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    date = update.message.text
    try:
        birth_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        candidate.birth_date = birth_date
    except ValueError:
        await update.message.reply_text(text['birth_format'][lang])
        return BIRTH
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['study'][lang])
    return EDUCATION


async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    education_mess = update.message.text
    candidate.education = education_mess
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['lang_lvl'][lang])
    return ENGLISH


async def english(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    language = update.message.text
    candidate.english_level = language
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['family'][lang])
    return FAMILY


async def family(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    family_status = update.message.text
    candidate.family_status = family_status
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['cv'][lang])
    return RESUME


async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang

    if update.message.document:
        document = update.message.document
        file = await context.bot.get_file(document)
        file_path = f'resumes/{candidate.id}.{document.file_name.split(".")[-1]}'
        await file.download_to_drive(file_path)
        candidate.resume_filepath = file_path
        candidate.resume_text = None
    else:
        resume_text = update.message.text
        candidate.resume_filepath = None
        candidate.resume_text = resume_text
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['source'][lang])
    return SOURCE


async def source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    source_mess = update.message.text
    candidate.source = source_mess
    session.add(candidate)
    session.commit()
    
    await update.message.reply_text(text['about'][lang])
    return FINAL


async def final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    company_knowledge = update.message.text
    candidate.company_knowledge_text = company_knowledge
    session.add(candidate)
    session.commit()

    stmt = select(Application).where(Application.candidate_id==candidate.id)
    application = session.execute(stmt).scalars().first()
    if application:
        if application.completed:
            await update.message.reply_text(text['error'][lang])
            return ConversationHandler.END
    else:
        application = Application(completed=True, candidate_id=candidate.id, created=datetime.datetime.now())
    session.add(application)
    session.commit()

    msg_text = build_text(candidate.id)
    if text:
        msg_text = f'Новая заявка. №{application.id}\n\n' + msg_text
        try:
            if candidate.resume_filepath:
                f = open(candidate.resume_filepath, 'rb')
                # await context.bot.send_document(chat_id=channel_id, document=f, caption=msg_text)
                print('sended message to channel1')
                f.close
            else:
                msg_text += f'- Резюме: {candidate.resume_text if candidate.resume_text else ""}\n'
                print('sended message to channel2')
                # await context.bot.send_message(chat_id=channel_id, text=msg_text) 
        except Exception as e:
            logger.error('can not send message to channel', e)

    await update.message.reply_text(text['thanks'][lang])
    return ConversationHandler.END

 
async def reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.chat_data.get('lang')
    stmt = select(Candidate).where(Candidate.tg_id==int(user.id))
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        await update.message.reply_text(text=text['error'][lang or 'ru'])
        return ConversationHandler.END

    lang = candidate.language
    context.chat_data['lang'] = lang
    
    rejection_reason = update.message.text
    candidate.rejection_reason = rejection_reason
    session.add(candidate)
    session.commit()

    await update.message.reply_text(text['thanks_2'][lang])
    return ConversationHandler.END


async def query_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    query.answer()
    lang = context.chat_data.get('lang')
    await query.edit_message_text(
        text=text['canceled'][lang or 'ru']
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.chat_data.get('lang')
    await update.message.reply_text(
        text['canceled'][lang or 'ru']
    )

    return ConversationHandler.END


async def timeout(update, context):
    lang = context.chat_data.get('lang')
    msg_text = text['timeout'][lang or 'ru']
    if update.message:
        await update.message.reply_text(msg_text)
    else:
        await context.bot.send_message(chat_id=update.effective_user.id, text=msg_text)

    return ConversationHandler.END


start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGREEMENT: [
                CallbackQueryHandler(agreement, pattern='^agreement_'),
                CallbackQueryHandler(query_cancel, pattern='^cancel$'),
            ],
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
            BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, birth)],
            EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, education)],
            ENGLISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, english)],
            FAMILY: [MessageHandler(filters.TEXT & ~filters.COMMAND, family)],
            RESUME: [MessageHandler(
                filters.Document.APPLICATION
                | filters.Document.TEXT
                # filters.Document.FileExtension("xls")
                # | filters.Document.FileExtension("xlsx")
                # | filters.Document.FileExtension("txt")
                # | filters.Document.FileExtension("doc")
                # | filters.Document.FileExtension("docx")
                # | filters.Document.FileExtension("pdf")
                # | filters.Document.FileExtension("ppt")
                # | filters.Document.FileExtension("pptx")
                | filters.TEXT
                & ~filters.COMMAND, resume)
            ],
            SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, source)],
            FINAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, final)],
            ABOUT: [
                CallbackQueryHandler(about, pattern='^final_'),
                CallbackQueryHandler(query_cancel, pattern='^cancel$'),
            ],
            LANGUAGE: [
                CallbackQueryHandler(language, pattern='^lang_'),
            ],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, reason)],
            ConversationHandler.TIMEOUT: [
                MessageHandler(filters.ALL, timeout),
                CallbackQueryHandler(timeout, pattern='.*'),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=datetime.timedelta(seconds=900)
    )
