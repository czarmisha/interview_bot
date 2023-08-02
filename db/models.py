import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    BigInteger,
    LargeBinary,
    Text,
)

_BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(_BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

_db_filename = 'bot_db'
db_path = os.path.join(_BASE_DIR, _db_filename)
engine = create_engine(f'sqlite:///{db_path}.db', echo=True)
channel_id = os.environ['CHANNEL_ID']
admin_ids = os.environ['ADMIN_IDS']

Base = declarative_base()
Session = sessionmaker()
    

class Application(Base):
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    created = Column(Date, nullable=True)
    completed = Column(Boolean, nullable=True)
    candidate_id = Column(Integer, ForeignKey("candidate.id"))

    candidate = relationship("Candidate", back_populates="application")

    def __repr__(self):
        return f'<Application - {self.candidate_id}'
    

class Company(Base):
    __tablename__ = 'company'

    description = Column(Text, nullable=True)

    id = Column(Integer, primary_key=True)

   
class Candidate(Base):
    __tablename__ = 'candidate'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=True)
    chat_id = Column(BigInteger, nullable=True)
    phone = Column(String(13), nullable=True)
    full_name = Column(String(50), nullable=True)
    birth_date = Column(Date, nullable=True)
    city = Column(String(30), nullable=True)
    created = Column(Date, nullable=True)
    education = Column(Text, nullable=True)
    source = Column(String(80), nullable=True)
    trading_knowledge = Column(Boolean, nullable=True)
    experience = Column(Text, nullable=True)
    english_level = Column(String(100), nullable=True)
    what_attracted = Column(String(100), nullable=True)
    agreement = Column(Boolean, nullable=True)
    resume_data = Column(LargeBinary, nullable=True)
    resume_filename = Column(String(100), nullable=True)
    resume_text = Column(Text, nullable=True)
    family_status = Column(String(50), nullable=True)
    company_knowledge = Column(Boolean, nullable=True)
    company_knowledge_text = Column(Text, nullable=True)

    application = relationship("Application", back_populates="candidate")

    def __repr__(self):
        return f'<Candidate - {self.full_name}, {self.phone}>'
    
# def save_resume(user_id, filename, file_path):
#     with open(file_path, 'rb') as file:
#         resume_data = file.read()

#     new_resume = UserResume(user_id=user_id, filename=filename, resume_data=resume_data)
#     session.add(new_resume)
#     session.commit()

# def retrieve_resume(user_id):
#     user_resume = session.query(UserResume).filter_by(user_id=user_id).first()
#     if user_resume:
#         file_path = f"{user_resume.filename}"
#         with open(file_path, 'wb') as file:
#             file.write(user_resume.resume_data)
#         return file_path
#     return None