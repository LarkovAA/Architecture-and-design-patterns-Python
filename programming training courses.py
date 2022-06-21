import time
from functools import wraps
import sqlite3
import web_server as ws
from abc import ABC, abstractmethod
import threading


# ДЗ 5
class Debug:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        @wraps(self.func)
        def call():
            print(f'Была вызвана функция {self.func.__name__} {time.ctime(time.time())}' )
            return self.func(*args, **kwargs)
        return call()

class AbstractRecordingsFactory(ABC):

    @abstractmethod
    def create_newbie(self):
        pass

    @abstractmethod
    def create_professional(self):
        pass


class CouresNewbie(ABC):

    @abstractmethod
    def create_course_newbie(self):
        pass


class CouresProfessional(ABC):

    @abstractmethod
    def create_course_professional(self):
        pass


class CoursePythonNewbie(CouresNewbie):
    def __init__(self, url, name, context:dict, handler=None):
        self.url = url
        self.name = name
        self.context = context
        self.handler = handler
        self.context['name_course'] = self.name

    def create_course_newbie(self, context:dict=None):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url, 'course page.html', self.context, self.handler)


class CoursePythonProfessional(CouresProfessional):
    def __init__(self, url, name, context:dict, handler=None):
        self.url = url
        self.name = name
        self.context = context
        self.handler = handler
        self.context['name_course'] = self.name

    def create_course_professional(self, context:dict=None):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url, 'course page.html', self.context, self.handler)


class CourseJavaNewbie(CouresNewbie):
    def __init__(self, url, name, context:dict=None, handler=None):
        self.url = url
        self.name = name
        self.context = context
        self.handler = handler
        self.context['name_course'] = self.name

    def create_course_newbie(self, context:dict=None):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url, 'course page.html', self.context, self.handler)


class CourseJavaProfessional(CouresProfessional):
    def __init__(self, url, name, context:dict, handler=None):
        self.url = url
        self.name = name
        self.context = context
        self.handler = handler
        self.context['name_course'] = self.name

    def create_course_professional(self, context:dict):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url, 'course page.html', self.context, self.handler)


class CreateCoursePython(AbstractRecordingsFactory):

    def create_newbie(self, url, name, context:dict, handler=None):
        return CoursePythonNewbie(url, name, context, handler)

    def create_professional(self, url, name, context, handler=None):
        return CoursePythonProfessional(url, name, context, handler)


class CreateCourseJava(AbstractRecordingsFactory):

    def create_newbie(self, url, name, context:dict, handler=None):
        return CourseJavaNewbie(url, name, context, handler)

    def create_professional(self, url, name, context:dict, handler=None):
        return CourseJavaProfessional(url, name, context, handler)


class Fabric:
    COURSE_ONE = 'Python'
    COURSE_TWO = 'Java'
    dict_course = {}

    @classmethod
    def create_factory(cls, name):
        if name == cls.COURSE_ONE:
            return CreateCoursePython()
        if name == cls.COURSE_TWO:
            return CreateCourseJava()
        else:
            return None

    # @classmethod
    def appent_dict_course(cls, object):
        cls.dict_course[object.name] = object

# ДЗ 6 !!!!!!!!
class Register:

    def __init__(self, index=None, url=None, contect:dict={}):
        self.user = {}
        self.index = index
        self.url = url
        self.handler = self.create_handler
        if self.handler:
            self.contect = self.handler()
        else:
            self.contect = contect

    def create_vief_register(self):
        '''
        Создает представление для страницы регистрации
        :return:
        '''
        serv.create_view(self.url, self.index, self.context, self.handler)

    def create_handler(self, request):
        '''
        Создает обработчик для регистрации
        :param request:
        :return:
        '''
        if request['POST'] == 'POST':
            login = request['login']
            password = request['password']
            connect = sqlite3.connect('database.db')
            register = PersonMapper(connect)
            person = Person(login=login, password=password)
            person.mark_new()
            register.insert(person=person)
            return Users.append_user(login, password)



class Users:
    def __init__(self):
        self.list_users = {}

    def append_user(self, user_login, user_password):
        self.list_users[user_login] = user_password


register = Register(url='register', index='register.html')
register.create_vief_register()

class RegisterCourse:
    def register(self, request):
        if request['POST'] == 'POST':
            course = request['course']
            page = request['page']
            line = request['line']
            login = request['login']
            email = request['email']
            tel = request['tel']

            if line == 'online':
                return ListCourse.append_dict_course_online(course, page, login, email, tel)
            if line == 'offline':
                return ListCourse.append_dict_course_offline(course, page, login, email, tel)

class ListCourse:

    def __init__(self):
        self.list_course_online = []
        self.list_course_offline = []

    def append_dict_course_online(self, course, page, login, email, tel):
        '''
        Добавляет пользователя на онлайн курсы
        :param course: данные курса
        :param page: название
        :param login: логин пользователя
        :param email: емайл
        :param tel: телефон
        :return:
        '''
        participant = {}
        name_course = f'{course}, {page}'
        participant[name_course] = [login, email, tel]
        self.list_course_online.append(participant)

    def append_dict_course_offline(self, course, page, login, email, tel):
        '''
        Добавляет пользователя на офлайн курсы
        :param course: данные курса
        :param page: название
        :param login: логин пользователя
        :param email: емайл
        :param tel: телефон
        :return:
        '''
        participant = {}
        name_course = f'{course}, {page}'
        participant[name_course] = [login, email, tel]
        self.list_course_offline.append(participant)

    def reder_page_course(self, request):
        '''
        Метод выводит в консоль сообщение пользователю о том что произошли изменения в названии во врменеи или дате
        курса
        :param request:
        :return:
        '''
        if request['POST'] == 'POST':
            course = request['course']
            name_course = request['name_course']
            date = request['date']
            time = request['time']
            course = course.split(', ')
            if course[1] == 'online':
                for el in  self.list_course_online:
                    if name_course in el.keys():
                        text = ''
                        if date:
                            text = text + f'Изменилась дата на {date}.'
                        if time:
                            text = text + f'Изменилось время на {time}.'
                        print(f'{el.value()[0]}. {text}')
            if course[1] == 'offline':
                for el in  self.list_course_offline:
                    if name_course in el.keys():
                        text = ''
                        if date:
                            text = text + f'Изменилась дата на {date}.'
                        if time:
                            text = text + f'Изменилось время на {time}.'
                        print(f'{el.value()[0]}. {text}')

    def return_list_course_online(self):
        return self.list_course_online

    def return_list_course_offline(self):
        return self.list_course_offline


# ДЗ 7

class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)
    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)
    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)

class Person(DomainObject):
    def __init__(self, id_person, login, password):
        self.id_person = id_person
        self.login = login
        self.password = password

class PersonMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_person):
        statement = "SELECT ID, LOGIN, PASSWORD FROM REGISTER_CLIENT WHERE IDPERSON=?"
        self.cursor.execute(statement, (id_person,))
        result = self.cursor.fetchone()
        if result:
            return Person(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_person} notfound')

    def insert(self, person):
        statement = "INSERT INTO REGISTER_CLIENT (LOGIN, PASSWORD) VALUES (?, ?)"
        self.cursor.execute(statement, (person.login, person.password))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, person):
        statement = "UPDATE REGISTER_CLIENT SET LOGIN=?, PASSWORD=? WHERE IDPERSON=?"
        self.cursor.execute(statement, (person.login, person.password,
                                    person.id_person))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, person):
        statement = "DELETE FROM REGISTER_CLIENT WHERE IDPERSON=?"
        self.cursor.execute(statement, (person.id_person,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work

class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Person):
            return PersonMapper(connection)



serv = ws.ServerHttp(('127.0.0.1', 8000), url='index', context={'course':False})
serv.add_templates('template')

python_newbie = Fabric.create_factory('Python')
python_professional = Fabric.create_factory('Python')

java_newbie = Fabric.create_factory('Java')
java_professional = Fabric.create_factory('Java')

basic_python = python_newbie.create_newbie('basic_py_newbie', 'Курс по основам Python для начинающих', context={
'date_online': ['11/06/22 19:00', '13/06/22 19:00', '15/06/22 19:00'], 'date_offline': [['12/06/22 13:00','г. Самара Московское шоссе 4а'],
                                                                                        ['14/06/22 13:00','г. Самара Московское шоссе 4а']]}, handler=RegisterCourse.register).create_course_newbie()

prof_python = python_professional.create_professional('prof_py_professional', 'Профессиональный курс по Python', context={
'date_online': ['12/06/22 19:00', '14/06/22 19:00', '16/06/22 19:00'], 'date_offline': [['13/06/22 13:00','г. Самара Московское шоссе 4а'], ['15/06/22 13:00','г. Самара Московское шоссе 4а']]
}, handler=RegisterCourse.register).create_course_professional()

basic_java = java_newbie.create_newbie('basic_java_newbie', 'Курс по основам Java для начинающих', context={
'date_online': ['11/06/22 19:00', '13/06/22 19:00', '15/06/22 19:00'], 'date_offline': [['12/06/22 13:00','г. Самара Московское шоссе 4а'], ['14/06/22 13:00','г. Самара Московское шоссе 4а']]
}, handler=RegisterCourse.register).create_course_newbie()

prof_java = java_professional.create_professional('prof_java_professional', 'Профессиональный курс по Java', context={
'date_online': ['12/06/22 19:00', '14/06/22 19:00', '16/06/22 19:00'], 'date_offline': [['13/06/22 13:00','г. Самара Московское шоссе 4а'], ['15/06/22 13:00','г. Самара Московское шоссе 4а']]
}, handler=RegisterCourse.register).create_course_professional()

serv.create_view(url='edit_course', template='editing courses.html', context= {'online': ListCourse.return_list_course_online(), 'offline': ListCourse.return_list_course_offline()}, handler=ListCourse.reder_page_course)

UnitOfWork.new_current()


# Fabric.appent_dict_course(object=basic_python)

serv.creating_socket(1, 1)
serv.run_server(time=0.1)


