# работаю со своим index.html
# делаю так, шоб при вводе ссылки и нажатии кнопки проводились все эти сканирования в терминальчике

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Вызвать функцию сканирования портов
        scan_ports()
        return 'Сканирование портов завершено'
    return render_template('miku.html')

def scan_ports():
    target = 'localhost'
    num_ports = 1000

    print('Результаты сканирования локального компьютера:')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
