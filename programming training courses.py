import web_server as ws
from abc import ABC, abstractmethod


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
    def __init__(self, url, name, context:dict):
        self.url = url
        self.name = name
        self.context = context
        self.context['name_course'] = self.name

    def create_course_newbie(self, context:dict=None):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url,'course page.html', self.context)


class CoursePythonProfessional(CouresProfessional):
    def __init__(self, url, name, context:dict):
        self.url = url
        self.name = name
        self.context = context
        self.context['name_course'] = self.name

    def create_course_professional(self, context:dict=None):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url, 'course page.html', self.context)


class CourseJavaNewbie(CouresNewbie):
    def __init__(self, url, name, context:dict=None):
        self.url = url
        self.name = name
        self.context = context
        self.context['name_course'] = self.name

    def create_course_newbie(self, context:dict=None):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url, 'course page.html', self.context)


class CourseJavaProfessional(CouresProfessional):
    def __init__(self, url, name, context:dict):
        self.url = url
        self.name = name
        self.context = context
        self.context['name_course'] = self.name

    def create_course_professional(self, context:dict):
        if context:
            self.context = {**self.context, **context}
        serv.create_view(self.url, 'course page.html', self.context)


class CreateCoursePython(AbstractRecordingsFactory):

    def create_newbie(self, url, name, context:dict):
        return CoursePythonNewbie(url, name, context)

    def create_professional(self, url, name, context):
        return CoursePythonProfessional(url, name, context)


class CreateCourseJava(AbstractRecordingsFactory):

    def create_newbie(self, url, name, context:dict):
        return CourseJavaNewbie(url, name, context)

    def create_professional(self, url, name, context:dict):
        return CourseJavaProfessional(url, name, context)


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

serv = ws.ServerHttp(('127.0.0.1', 8000), url='index', context={'course':False})
serv.add_templates('template')

python_newbie = Fabric.create_factory('Python')
python_professional = Fabric.create_factory('Python')

java_newbie = Fabric.create_factory('Java')
java_professional = Fabric.create_factory('Java')

basic_python = python_newbie.create_newbie('basic_py_newbie', 'Курс по основам Python для начинающих', context={
'date_online': ['11/06/22 19:00', '13/06/22 19:00', '15/06/22 19:00'], 'date_offline': [['12/06/22 13:00','г. Самара Московское шоссе 4а'], ['14/06/22 13:00','г. Самара Московское шоссе 4а']]
}).create_course_newbie()


# Fabric.appent_dict_course(object=basic_python)

serv.creating_socket(1, 1)
serv.run_server(time=0.1)


