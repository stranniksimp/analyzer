from flask import Flask, render_template, requests, socket, time, ssl, subprocess

app = Flask(__name__, template_folder='templates')


@app.route('/', methods = ['GET', 'POST'])

def index():
    if request.method == 'POST':
        username = request.form['username']
        return 'Здравствуйте' + username + '!'
    return render_template('index.html')

@app.route('/register')
def register():
        return render_template('register.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)


# Для оценки скорости загрузки страницы с использованием библиотеки Requests
def load_time(url):
    start = time.time()
    response = requests.get(url)
    end = time.time()

    load_time = end - start
    return load_time

if __name__ == "__main__":
    url = "https://www.example.com"
    page_load = load_time(url)
    print(f"Время загрузки страницы {url}: {page_load} секунд")


# Сканирование портов
print('Результаты сканирования локального компьютера:')
def scan_ports():


 target = 'localhost'
 num_ports = 1000



 for port in range(1, num_ports + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            result = sock.connect_ex((target, port))
            if result == 0:
              print(f"Порт {port} открыт")


          sock.close()
        except socket.error:
        pass

scan_ports()

domain_name = 'example.com'

# Получение IP-адреса для указанного доменного имени
ip_address = socket.gethostbyname(domain_name)
print(f'IP-адрес для доменного имени {domain_name}: {ip_address}')

# Получение списка IP-адресов для указанного доменного имени
ip_addresses = socket.gethostbyname_ex(domain_name)
print(f'Список IP-адресов для доменного имени {domain_name}: {ip_addresses}')

# Получение имени хоста для указанного IP-адреса
host_name = socket.gethostbyaddr(ip_address)
print(f'Имя хоста для IP-адреса {ip_address}: {host_name}')


from cryptography import x509
from cryptography.hazmat.backends import default_backend

url = input("Укажите веб-сайт (www.example.com): ") # адрес ресурса
try:
 # Устанавливаем соединение с сервером по порту 443 (стандартный порт HTTPS)

 connection = ssl.create_default_context().wrap_socket(
 socket.socket(socket.AF_INET, socket.SOCK_STREAM),
 server_hostname=url,
 )
 connection.connect((url, 443))

 # Получаем информацию о сертификате
 certificate_data = connection.getpeercert(binary_form=True)

 # Используем cryptography для анализа сертификата
 cert = x509.load_der_x509_certificate(certificate_data,
default_backend())

 # Выводим информацию о сертификате
 print(f"Информация о SSL-сертификате для {url}:\n")
 print(f"Владелец: {cert.issuer.rfc4514_string()}")
 print(f"Действителен с {cert.not_valid_before} до {cert.not_valid_after}")
 print(f"Алгоритм подписи: {cert.signature_algorithm_oid._name}")
except Exception as e:
 print(f"Ошибка при выполнении запроса: {e}")

# Выполнение пинга с помощью библиотеки subprocess
 def ping(host):
    result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
    return 'Успех!' if result.returncode == 0 else 'Ошибка!'

print(ping('example.com'))
