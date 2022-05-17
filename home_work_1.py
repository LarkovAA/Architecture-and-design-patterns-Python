import select
import socket
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

    def __init__(self, ADDRES:tuple, index='index.html', url='', context:dict={}):
        self.ADDRES = ADDRES
        self.list_client = []
        self.views = []
        self.index = index
        self.url = url
        self.context = context
        self.views.append([self.url, self.index, self.context])

    def creating_socket(self, number_max_connections, time):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.ADDRES)
        self.sock.listen(number_max_connections)
        self.sock.settimeout(time)

    def create_view(self, url, template, context:dict):
        self.views.append([url, template, context])

    def change_view(self, what, which_url, on_what_url):
        if what == 'url':
            for url in self.views:
                if which_url == url[0]:
                    url[0] = on_what_url
        if what == 'template':
            for url in self.views:
                if which_url == url[1]:
                    url[1] = on_what_url
        if what == 'context':
            for url in self.views:
                if which_url == url[2]:
                    url[2] = on_what_url

    def run_server(self, time=0):
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
                list_reader, list_write, list_error = select.select(self.list_client, self.list_client, [], time)
            except Exception:
                pass
            for iwtd in list_reader:
                try:
                    data = iwtd.recv(1024).decode()
                except:
                    pass
                else:
                    for owtd in list_write:
                        list_data = data.split('/')
                        if iwtd == owtd:
                            for date in self.views:
                                if date[0] == self.url:
                                    url = ' HTTP'
                                    temp = date[1]
                                    context = date[2]
                                else:
                                    url = f'{date[0]} HTTP'
                                    temp = date[1]
                                    context = date[2]
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
                                        break
                                except:
                                    pass


if __name__ == '__main__':
    comtext = {'name': 'Алексей', 'year': 1993, 'city': 'Самара'}
    serv = ServerHttp(('127.0.0.1', 8000), context=comtext)
    serv.create_view('about', 'about.html', {})

    serv.creating_socket(1, 1)
    serv.run_server(time=0.1)
