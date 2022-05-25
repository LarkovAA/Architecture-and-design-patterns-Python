import select
import socket
import pprint
import requests
from jinja2 import Template

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

class ServerHttp:

    def __init__(self, ADDRES:tuple, index='index.html', url='', context:dict={}, handler=None):
        self.ADDRES = ADDRES
        self.list_client = []
        self.views = []
        self.index = index
        self.url = url
        self.context = context
        self.handler = handler
        self.views.append([self.url, self.index, self.context, self.handler])

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

    def create_view(self, url, template, context:dict, handler=None):
        """
        Метож создает вид который определяет адресс и его шаблон а так же данные которые должны быть переданы в шаблон
        :param url: название адреса
        :param template: шаблон
        :param context: данные в шаблоне
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
                    data = iwtd.recv(2048).decode()
                    print(data)

                except:
                    pass
                else:

                    # В цикле проходим по всем пользователям которые готовы на чтение данных
                    for owtd in list_reader:

                        # Разбиваем получившиеся данные по разделителю / для создания словаря
                        list_data = data.split('/')

                        # Если содинение которое отправила данные и то которое начал принимать данные одно и то же то продолжаем следующие действия
                        if iwtd == owtd:
                            try:
                                print(list_data[1])
                                if list_data[1] == 'favicon.ico HTTP':
                                    self.list_client.remove(owtd)
                                    client.close()
                                    break
                            except:
                                pass
                            if list_data[0] == 'GET ':
                                for date in self.views:
                                    print(len(list_data))
                                    if len(list_data) == 15:
                                        if date[0] == '':
                                            url = ' HTTP'
                                            temp = date[1]
                                            context = date[2]
                                        else:
                                            url = f'{date[0]} HTTP'
                                            temp = date[1]
                                            context = date[2]

                                    # В случае если имеем данные передаваемые в строке
                                    if len(list_data) == 16:
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
                                        if list_data[1] == url:
                                            if context:
                                                output_test = render(temp, object_list=context)
                                            else:
                                                output_test = render(temp)

                                            text = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n {output_test}'
                                            output_test = text.encode('utf-8')

                                            iwtd.send(output_test)
                                            self.list_client.remove(owtd)
                                            client.close()
                                            break
                                    except:
                                        pass
                            if list_data[0] == 'POST ':
                                # text = requests.post(list_data)
                                # text = text.json()['form']
                                pprint.pprint(list_data)

if __name__ == '__main__':
    context = {'name': 'Алексей', 'year': 1993, 'city': 'Самара'}
    serv = ServerHttp(('127.0.0.1', 8000), context=context, url='index')
    serv.create_view('about', 'about.html', {})
    serv.create_view('contact', 'list_contact.html', {})


    serv.creating_socket(1, 1)
    serv.run_server(time=0.1)
