from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


def example():
    Session = sessionmaker(bind=engine)
    session = Session()

    new_row = Table(task='This is string field!',
                    deadline=datetime.strptime('06-26-2020', '%m-%d-%Y').date())
    session.add(new_row)
    session.commit()
    rows = session.query(Table).all()
    first_row = rows[0]  # In case rows list is not empty
    print(first_row.task)  # Will print value of the string_field
    print(first_row.id)  # Will print the id of the row.
    print(first_row)  # Will print the string that was returned by __repr__ method


def menu_fun():
    # menu = "1) Today's tasks \n2) Add task \n0) Exit "
    menu = """
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""".strip().lower()

    print(menu)

    chose = int(input())
    return chose


def print_tasks(date_today):
    Session = sessionmaker(bind=engine)
    session = Session()

    today = datetime.today()

    rows = session.query(Table).all()
    print('\nToday {} {}:'.format(today.day, today.strftime('%b')))

    day_tasks(date_today, rows)


def day_tasks(date_today, rows):
    i = 0
    for row in rows:
        if row.deadline == date_today.date():
            i = 1 + i
            print(str(i) + '. ' + row.task)
    if i == 0:
        print('Nothing to do!')
    print('')


def add_task():
    print('\nEnter task')
    task = input()

    print('Enter deadline')
    task_date = input()
    date = datetime.strptime(task_date, '%Y-%m-%d')

    Session = sessionmaker(bind=engine)
    session = Session()
    new_row = Table(task=task,
                    deadline=date.date())
    session.add(new_row)
    session.commit()

    print('The task has been added!\n')


def week_tasks(today):
    Session = sessionmaker(bind=engine)
    session = Session()

    rows = session.query(Table).all()

    for i in range(0, 7):
        next_day = today + timedelta(days=i)
        print('\n{} {} {}:'.format(next_day.strftime('%A'), next_day.day, next_day.strftime('%b')))
        day_tasks(next_day, rows)


def all_tasks():
    Session = sessionmaker(bind=engine)
    session = Session()

    rows = session.query(Table).all()
    rows.sort()

    print('\nAll tasks:')
    i = 1
    for row in rows:
        print(str(i) + '. ' + row.task +
              ' {} {}'.format(row.deadline.day, row.deadline.strftime('%b')))
        i = i + 1

    print('')


def missed_tasks():
    Session = sessionmaker(bind=engine)
    session = Session()

    rows = session.query(Table).filter(Table.deadline < datetime.today()).all()
    rows.sort()
    print('\nMissed tasks:')
    i = 1
    for row in rows:
        print(str(i) + '. ' + row.task +
              ' {} {}'.format(row.deadline.day, row.deadline.strftime('%b')))
        i = i + 1

    if i == 1:
        print('Nothing is missed!')

    print('')


def delete_task():
    Session = sessionmaker(bind=engine)
    session = Session()

    rows = session.query(Table).all()
    rows.sort()


    print('')
    if len(rows) == 0:
        print('Nothing to delete')
    else:
        print('Chose the number of the task you want to delete:')
        i = 1
        for row in rows:
            print(str(i) + '. ' + row.task +
                  ' {} {}'.format(row.deadline.day, row.deadline.strftime('%b')))
            i = i + 1

        to_remove = int(input())
        chosen_row = rows[to_remove]
        session.delete(chosen_row)

        session.commit()

        print('The task has been deleted!')

    print('')



engine = create_engine('sqlite:///todo.db?'
                       'check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    def __lt__(self, other):
        return self.deadline < other.deadline


Base.metadata.create_all(engine)

# example()


again_main = True



while again_main:
    choice = menu_fun()

    # print today's tasks
    if choice == 1:
        print_tasks(datetime.today())

    # Exit
    if choice == 0:
        print('\nBye!', end='')
        again_main = False

    # create task
    if choice == 5:
        add_task()

    # print week's tasks
    if choice == 2:
        week_tasks(datetime.today())

    # print all tasks deadline sorted
    if choice == 3:
        all_tasks()

    # print all missed tasks
    if choice == 4:
        missed_tasks()

    # delete task
    if choice == 6:
        delete_task()
