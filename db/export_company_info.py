# import os, inspect, sys

# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir) 
from models import Company, Session, engine
from sqlalchemy import select

file_path = 'files/company_info.txt'

try:
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
        session = Session(bind=engine)
        stmt = select(Company)
        company = session.execute(stmt).scalars().first()
        if company:
            print(f'Обновляю информацию')
            company.description = content
            session.add(company)
            session.commit()
        else:
            print(f'Создаю информацию')
            company = Company(description=content)
            session.add(company)
            session.commit()

        session.close()
        print(f'Успешно')
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error occurred: {e}")
