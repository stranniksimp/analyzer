from flask import Flask, render_template, request
import requests
import time
import ssl
import socket
import OpenSSL
import idna
from colorama import Fore, Style
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import colorama
from colorama import Fore, Style


app = Flask(__name__)

def take_screenshot(url):
    print(Fore.YELLOW + "[*]" + Style.RESET_ALL + r" Начинаю создавать скриншот для {url}")
    start_time = time.time()
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запускает браузер в безголовом режиме
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    screenshot = driver.get_screenshot_as_base64()
    driver.quit()
    end_time = time.time()
    print(Fore.GREEN + "[+]" + Style.RESET_ALL + r" Скриншот для {url} создан за {end_time - start_time} секунд")
    return screenshot

def add_protocol(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        print(Fore.YELLOW + "[*]" + Style.RESET_ALL + " Ссылка не содержит протокола, добавляю вручную")
        url = 'https://' + url
    return url

def check_url(url):
    print(Fore.YELLOW + "[*]" + Style.RESET_ALL + " Измеряю время загрузки")
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        load_time = end_time - start_time

        # Время проверки
        load_time_str = f"Время загрузки: {load_time:.3f} секунд"

        # Пинг
        ip = socket.gethostbyname(url.split('/')[2])
        ping_time = ping(ip)
        ping_str = f"Пинг: {ping_time:.3f} мс"

        # DNS параметры
        dns_time = dns_lookup_time(url)
        dns_str = f"Время DNS: {dns_time:.3f} мс"

        # SSL сертификат
        print(Fore.YELLOW + "[*]" + Style.RESET_ALL + " Проверяю SSL сертификат")
        cert = ssl.get_server_certificate((url.split('/')[2], 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        subject = x509.get_subject()
        issued_by = idna.decode(subject.CN.replace('*.', ''))  # Декодируем Punycode с помощью idna
        not_before = datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
        not_after = datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')
        signature_algorithm = x509.get_signature_algorithm().decode('utf-8')
        cert_str = f"SSL сертификат: Действителен\nВладелец: {issued_by}\nДействителен с: {not_before}\nпо {not_after}\nАлгоритм подписи: {signature_algorithm}"


        # IP адреса
        print(Fore.YELLOW + "[*]" + Style.RESET_ALL + " Проверяю IP адреса")
        ip_addresses = socket.gethostbyname_ex(url.split('/')[2])[2]
        ip_str = f"IP адреса: {', '.join(ip_addresses)}"

        return load_time_str, ping_str, dns_str, cert_str, ip_str

    except Exception as e:
        error_str = f"Ошибка: {e}"
        return error_str, "", "", "", ""

def ping(host):
    try:
        print(Fore.YELLOW + "[*]" + Style.RESET_ALL + " Проверяю пинг")
        ip = socket.gethostbyname(host)
        start_time = time.time()
        socket.create_connection((ip, 80), 2)
        end_time = time.time()
        ping_time = (end_time - start_time) * 1000
        return ping_time
    except socket.error:
        return None

def dns_lookup_time(url):
    print(Fore.YELLOW + "[*]" + Style.RESET_ALL + " Проверяю параметры DNS")
    start_time = time.time()
    socket.gethostbyname(url.split('/')[2])
    end_time = time.time()
    dns_time = (end_time - start_time) * 1000
    return dns_time

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = add_protocol(request.form['url'])
        load_time_str, ping_str, dns_str, cert_str, ip_str = check_url(url)
        screenshot = take_screenshot(url)
        return render_template('index.html', load_time=load_time_str, ping=ping_str, dns=dns_str, cert=cert_str, ip=ip_str, screenshot=screenshot or None)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
