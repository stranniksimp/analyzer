from flask import Flask, render_template, request, socket

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