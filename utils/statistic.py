import logging, datetime
from sqlalchemy import select, func
from database.models import (
    Session,
    engine,
    Application,
    Candidate,
)

session = Session(bind=engine)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class Statistic:
    def __init__(self, type) -> None:
        self.type = type
        self.text = None
        self.session = Session(bind=engine)

    def get_stat(self):
        if self.type == '1':
            return self.get_stat_for_type_1()
        elif self.type == '2':
            return self.get_stat_for_type_2()
        elif self.type == '3':
            return self.get_stat_for_type_3()
        elif self.type == '4':
            return self.get_stat_for_type_4()
        elif self.type == '5':
            return self.get_stat_for_type_5()
        elif self.type == '6':
            return self.get_stat_for_type_6()
        # elif self.type == '7':
        #     return self.get_stat_for_type_7()
        # elif self.type == '8':
        #     return self.get_stat_for_type_8()
        elif self.type == '9':
            return self.get_stat_for_type_9()
# за сегодня
# за вчера
# за текущую неделю
# за прошлую неделю
# за за текущий месяц
# за за прошлый месяц
# за конкретный месяц
# за конкретную дату
# за все время
    def get_stat_for_type_1(self):
        text = "Статистика за сегодня:\n\n"
        today = datetime.date.today()

        stmt = select(Application.id).where(func.DATE(Application.created) == today)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Заполненных заявок: {len(apps)}\n"

        stmt = select(Candidate.id).where(func.DATE(Candidate.last_activity) == today)
        candidates = self.session.execute(stmt).scalars().all()
        text += f"Кандидатов: {len(candidates)}\n"

        stmt = select(Application.id).where(func.DATE(Application.created) == today, Application.processed == True)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Обработанных заявок: {len(apps)}\n"

        return text

    def get_stat_for_type_2(self):
        text = "Статистика за вчера:\n\n"
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        stmt = select(Application.id).where(func.DATE(Application.created) == yesterday)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Заполненных заявок: {len(apps)}\n"

        stmt = select(Candidate.id).where(func.DATE(Candidate.last_activity) == yesterday)
        candidates = self.session.execute(stmt).scalars().all()
        text += f"Кандидатов: {len(candidates)}\n"

        stmt = select(Application.id).where(func.DATE(Application.created) == yesterday, Application.processed == True)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Обработанных заявок: {len(apps)}\n"

        return text

    def get_stat_for_type_3(self):
        text = "Статистика за текущую неделю:\n\n"
        today = datetime.date.today()
        start = today - datetime.timedelta(days=today.weekday())
        end = today + datetime.timedelta(days=(6 - today.weekday()))

        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Заполненных заявок: {len(apps)}\n"

        stmt = select(Candidate.id).where(func.DATE(Candidate.last_activity) >= start, func.DATE(Candidate.last_activity) <= end)
        candidates = self.session.execute(stmt).scalars().all()
        text += f"Кандидатов: {len(candidates)}\n"

        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end, Application.processed == True)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Обработанных заявок: {len(apps)}\n"

        return text

    def get_stat_for_type_4(self):
        text = "Статистика за прошлую неделю:\n\n"
        today = datetime.date.today()
        start = today - datetime.timedelta(days=(today.weekday() + 7))
        end = today - datetime.timedelta(days=(today.weekday() + 1))

        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Заполненных заявок: {len(apps)}\n"

        stmt = select(Candidate.id).where(func.DATE(Candidate.last_activity) >= start, func.DATE(Candidate.last_activity) <= end)
        candidates = self.session.execute(stmt).scalars().all()
        text += f"Кандидатов: {len(candidates)}\n"

        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end, Application.processed == True)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Обработанных заявок: {len(apps)}\n"

        return text

    def get_stat_for_type_5(self):
        text = "Статистика за текущий месяц:\n\n"
        today = datetime.date.today()
        start = today - datetime.timedelta(days=today.day - 1)
        end = datetime.date.today() + datetime.timedelta(days=32)
        end = end - datetime.timedelta(days=end.day)

        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Заполненных заявок: {len(apps)}\n"

        stmt = select(Candidate.id).where(func.DATE(Candidate.last_activity) >= start, func.DATE(Candidate.last_activity) <= end)
        candidates = self.session.execute(stmt).scalars().all()
        text += f"Кандидатов: {len(candidates)}\n"

        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end, Application.processed == True)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Обработанных заявок: {len(apps)}\n"

        return text

    def get_stat_for_type_6(self):
        text = "Статистика за прошлый месяц:\n\n"
        today = datetime.date.today()
        end = today - datetime.timedelta(days=today.day)
        start = end - datetime.timedelta(days=end.day -1)
        
        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Заполненных заявок: {len(apps)}\n"

        stmt = select(Candidate.id).where(func.DATE(Candidate.last_activity) >= start, func.DATE(Candidate.last_activity) <= end)
        candidates = self.session.execute(stmt).scalars().all()
        text += f"Кандидатов: {len(candidates)}\n"

        stmt = select(Application.id).where(func.DATE(Application.created) >= start, func.DATE(Application.created) <= end, Application.processed == True)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Обработанных заявок: {len(apps)}\n"

        return text

    # def get_stat_for_type_7(self):
    #     pass
    #     # за конкретный месяц

    # def get_stat_for_type_8(self):
    #     pass
    #     # за конкретную дату

    def get_stat_for_type_9(self):
        text = "Статистика за все время:\n\n"

        stmt = select(Application.id)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Заполненных заявок: {len(apps)}\n"

        stmt = select(Candidate.id)
        candidates = self.session.execute(stmt).scalars().all()
        text += f"Кандидатов: {len(candidates)}\n"

        stmt = select(Application.id).where(Application.processed == True)
        apps = self.session.execute(stmt).scalars().all()
        text += f"Обработанных заявок: {len(apps)}\n"

        return text