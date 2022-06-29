import select
import socket
import time
from functools import wraps

from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

class Debug:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        @wraps(self.func)
        def call():
            print(f'Была вызвана функция {self.func.__name__} {time.ctime(time.time())}' )
            return self.func(*args, **kwargs)
        return call()


# Боязнь размещать логику в объектах предметной области. Рендеры расположены отдельно от объекта который создает объект представления.
def render(template_name, **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # Открываем шаблон по имени
    with open(template_name, encoding='utf-8') as f:
        # Читаем
        template = Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)

# Боязнь размещать логику в объектах предметной области. Рендеры расположены отдельно от объекта который создает объект представления.
def render_base(template_name, folder='templates', **kwargs):
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)


# Божественный объект. Объект по сути занимается всем создает веб сервер, создает представления, URL-лы и шаблоны
class ServerHttp:

    def __init__(self, ADDRES:tuple, index='index.html', url='', context:dict={}, handler=None,):
        self.ADDRES = ADDRES
        self.list_client = []
        self.views = []
        self.index = index
        self.url = url

        self.handler = handler
        if handler:
            self.context = handler()
            self.context = {**context, **self.context}
        else:
            self.context = context

        self.views.append([self.url, self.index, self.context, self.handler])
        self.templates = []

    def add_templates(self, template):
        self.templates.append(template)

    def creating_socket(self, number_max_connections, time):
        """
        Метод создает сокет
        :param number_max_connections: колличество мак соединений
        :param time: время
        :return:
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.ADDRES)
        self.sock.listen(number_max_connections)
        self.sock.settimeout(time)


    @Debug
    def create_view(self, url, template, context:dict, handler=None):
        """
        Метож создает вид который определяет адресс и его шаблон а так же данные которые должны быть переданы в шаблон
        :param url: название адреса
        :param template: шаблон
        :param context: данные в шаблоне
        :param handler: обработчик запроса
        :return:
        """
        self.views.append([url, template, context, handler])

    def change_view(self, what, which, on_what):
        """
        Метод редактирует адресс, либо шаблон, либо данные передающиеся в шаблон
        :param what: что меняем
        :param which_url: какой меняем
        :param on_what_url: на что меняем
        :return:
        """
        for el in self.views:
            if what == 'url':
                if which == el[0]:
                    el[0] = on_what
                    break
            if what == 'template':
                if which == el[1]:
                    el[1] = on_what
                    break
            if what == 'context':
                if which == el[2]:
                    el[2] = on_what
                    break
            if what == 'handler':
                if which == el[3]:
                    el[3] = on_what
                    break

    def run_server(self, time=0):
        """
        Метод запускает работу сервера
        :param time:
        :return:
        """
        while True:
            try:
                client, addr = self.sock.accept()
            except:
                pass
            else:
                self.list_client.append(client)
                print(len(self.list_client))
            finally:
                time = time
                list_reader = []
                list_write = []
                list_error = []
            try:
                list_write, list_reader, list_error = select.select(self.list_client, self.list_client, [], time)
            except Exception:
                pass
            # В цикле принимает все соединения готовые к отправле данных
            for iwtd in list_write:
                try:

                    # Принимаем инф от пользователя и декодируем ее
                    data = iwtd.recv(2048)
                    # print(data)
                    # params = parse_qs(data)

                    data = data.decode()
                    print(data)
                    # print(iwtd)
                except:
                    pass
                else:

                    # В цикле проходим по всем пользователям которые готовы на чтение данных
                    for owtd in list_reader:

                        # Разбиваем получившиеся данные по разделителю / для создания словаря
                        list_data = data.split('/')
                        print(len(list_data))

                        # num = 0
                        # for i in list_data:
                        #     print(f'{num} : {i}')
                        #     num += 1
                        # Если содинение которое отправила данные и то которое начал принимать данные одно и то же то продолжаем следующие действия
                        if iwtd == owtd:

                            try:
                                # print(list_data[1])
                                if list_data[1] == 'favicon.ico HTTP':
                                    self.list_client.remove(owtd)
                                    # client.close()
                                    break
                            except:
                                pass
                            if list_data[0] == 'GET ':
                                stop = False
                                for date in self.views:
                                    if not stop:
                                        # Для
                                        # print(len(list_data))
                                        if 'Chrome' in list_data[2] and (len(list_data) == 15 or len(list_data) == 18) or 'Yandex' in list_data[2] and (len(list_data) == 17 or len(list_data) == 20):
                                            if date[0] == '':
                                                url = ' HTTP'
                                                temp = date[1]
                                                context = date[2]
                                            else:
                                                url = f'{date[0]} HTTP'
                                                temp = date[1]
                                                context = date[2]

                                        # В случае если имеем данные передаваемые в строке
                                        if 'Chrome' in list_data[2] and len(list_data) == 16 or 'Yandex' in list_data[2] and len(list_data) == 18:
                                            url = date[0]
                                            temp = date[1]
                                            context = date[2]

                                            # Производим поиск данных и подставляем их в словарь с параметрами.
                                            list_parameter_is_http = list_data[2].split(' ')
                                            list_parameter = list_parameter_is_http[0].split('&')
                                            parameters = {}
                                            for par in list_parameter:
                                                par = par.split('=')
                                                parameters[par[0]] = par[1]
                                            context = {**context, **parameters}

                                        try:
                                            for temp_ in self.templates:
                                                if list_data[1] == url:
                                                    if context:
                                                        output_test = render_base(template_name=temp,folder=temp_, object_list=context)
                                                    else:
                                                        output_test = render_base(template_name=temp,folder=temp_)

                                                    text = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n {output_test}'
                                                    output_test = text.encode('utf-8')

                                                    iwtd.send(output_test)
                                                    # iwtd.shatdown(socket.SHUT_WR)
                                                    self.list_client.remove(iwtd)
                                                    print(len(self.list_client))
                                                    # client.close()
                                                    stop = True

                                        except:
                                            pass
                                    else:
                                        break
                                # if list_data[0] == 'POST ':
                                #     pass
                                #     # text = requests.post(list_data)
                                #     # text = text.json()['form']
                                #     # pprint.pprint(list_data)
                                #     # print(params.decode())
                        if list_data[0] == 'POST ':
                            # Если мы получаем пост запрос то мы с момошью функции split получаем данные которые были получени от него
                            print(list_data[-1])
                            data_post = list_data[-1].split(' ')
                            print(data_post)
                            data_post = data_post[-1].split('\r\n\r\n')
                            print(data_post)
                            data_post = data_post[-1].split('&')
                            # создаем словарь с данными
                            request = {'POST': 'POST'}
                            for par in data_post:
                                par = par.split('=')
                                request[par[0]] = par[1]
                            # В списке self.views изем url от которого мы получили POST запрос и далее вызываем функцию обработчик
                            for view in self.views:
                                if f'{view[0]} HTTP' == list_data[1]:
                                    view[3](request)



if __name__ == '__main__':

    def request_post_output(request):
        if request['POST'] == 'POST':
            import datetime
            name = request['text']
            topic = request['topic']
            email = request['email']
            date = str(datetime.datetime.now()).replace(' ', '')
            path = f'post_output\\{date}.txt'
            with open(path, encoding='utf-8', mode='w') as nm:
                list_text = [f'Email {email}\n', f'Заголовок: {topic}\n', f'Тексе: {name}\n']
                nm.writelines(list_text)



    context = {'name': 'Алексей', 'year': 1993, 'city': 'Самара'}

    # Тут антипаттерн Магические числа '127.0.0.1', 8000 не понятно чтио означают данные в кортеже.
    serv = ServerHttp(('127.0.0.1', 8000), context=context, url='index')

    serv.create_view('about', 'about.html', {})
    serv.create_view('contact', 'list_contact.html', {}, request_post_output)

    serv.add_templates('template')




    serv.creating_socket(1, 1)
    serv.run_server(time=0.1)
