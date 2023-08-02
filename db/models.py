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
)

_BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(_BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

_db_filename = os.environ['DB_FILENAME']
db_path = os.path.join(_BASE_DIR, _db_filename)
engine = create_engine(f'sqlite:///{db_path}.db', echo=True)
default_manager_tashkent = os.environ['DEFAULT_MANAGER_KYIV']
default_manager_kyiv = os.environ['DEFAULT_MANAGER_TASHKENT']

Base = declarative_base()
Session = sessionmaker()
    

class Application(Base):
    __tablename__ = 'application'

    id = Column(Integer, primary_key=True)
    created = Column(Date, nullable=False)
    completed = Column(Boolean, nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidate.id"))

    candidate = relationship("Candidate", back_populates="application")
    

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)

   
class Candidate(Base):
    __tablename__ = 'candidate'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=True)
    phone = Column(String(13), nullable=False)
    full_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    city = Column(String(30), nullable=True)
    created = Column(Date, nullable=False)
    education = Column(String(150), nullable=False)
    source = Column(String(80), nullable=False)
    trading_knowledge = Column(Boolean, nullable=False)
    experience = Column(String(200), nullable=True)
    english_level = Column(String(100), nullable=False)
    what_attracted = Column(String(100), nullable=False)
    consent = Column(Boolean, nullable=False)  # что если не дал согласие?
    resume_data = Column(LargeBinary, nullable=True)
    resume_filename = Column(String(100), nullable=True)
    # application

    tashkent_topics = relationship("Topic", back_populates="tashkent_user", foreign_keys="Topic.tashkent_user_id")
    kyiv_topics = relationship("Topic", back_populates="kyiv_user", foreign_keys="Topic.kyiv_user_id")
    question = relationship("Question", back_populates="author")

    def __repr__(self):
        return f'<User - {self.name}, id: {self.id}>'
    
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