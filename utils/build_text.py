import logging

from sqlalchemy import select
from db.models import (
    Session,
    engine,
    Candidate,
)

session = Session(bind=engine)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def build_text(id):
    logger.info('starting to build text for channel')
    stmt = select(Candidate).where(Candidate.id==id)
    candidate = session.execute(stmt).scalars().first()
    if not candidate:
        logger.error("error! no candidate in db. can not build text for channel")
        return ''
    
    text = ''
    text += f'- Согласие на обработку персональных данных: {"да" if candidate.agreement else "нет"}\n'
    text += f'- ФИО: {candidate.full_name if candidate.full_name else "-"}\n'
    text += f'- Телефон: {candidate.phone if candidate.phone else "-"}\n'
    text += f'- Дата рождения: {candidate.birth_date.strftime("%d.%m.%Y") if candidate.birth_date else "-"}\n'
    text += f'- Образование: {candidate.education if candidate.education else "-"}\n'
    text += f'- Откуда узнал: {candidate.source if candidate.source else "-"}\n'
    text += f'- Уровень английского: {candidate.english_level if candidate.english_level else "-"}\n'
    text += f'- Семейное положение: {candidate.family_status if candidate.family_status else "-"}\n'
    text += f'- Знаком с компанией: {candidate.company_knowledge_text if candidate.company_knowledge_text else "-"}\n'
    # text += f'- Опыт: {candidate.experience if candidate.experience else "-"}\n'
    # text += f'- Причина отказа: {candidate.rejection_reason if candidate.rejection_reason else "-"}\n'

    return text