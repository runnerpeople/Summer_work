#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
import os
import os.path
import subprocess
import requests
import logging.handlers
import configparser

import uuid
import json

from transliterate import translit

config = configparser.ConfigParser()
config.read('config.ini')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'tmp')

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_FILE_EXTENSION"] = ["scm"]
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = config['server']['secret_key']


@app.errorhandler(500)
def handle_error(error):
    app.logger.error(str(error))
    return json.dumps({"status": 'Ошибка', "errorMessage": 'Обратитесь к админу'}, ensure_ascii=False)


app.register_error_handler(500, handle_error)

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = logging.handlers.RotatingFileHandler('server.log', maxBytes=100 * 1024 * 1024, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

url_test = {
    "dz3": config['test']['dz3'],
    "lab4_5": config['test']['lab4_5'],
    "lab4_6": config['test']['lab4_6'],
    "dz4_1": config['test']['dz4_1'],
    "dz4_2": config['test']['dz4_2'],
    "dz4_3": config['test']['dz4_3'],
    "other": None
}

# dictionary login:number_tests
ignore_test = {
    "ivanov_g": [8, 9, 10],
    # code here
}


def is_allowed_file(filename, allowed_extensions):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]
    return ext in allowed_extensions


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        values = request.values
        if 'name' not in values \
                or 'surname' not in values \
                or values['name'].strip() == '' \
                or values['surname'].strip() == '':
            return json.dumps({"status": 'Ошибка',
                               "errorMessage": 'Неверно заполнено имя/фамилия. Проверьте еще раз'
                               },
                              ensure_ascii=False)

        login_str = translit(values['surname'].lower(), 'ru', reversed=True) + "_" + translit(values['name'].lower(),
                                                                                              'ru', reversed=True)[0]
        session['login'] = login_str
        app.logger.warning("Student %s authorized. Login - %s" % (values['surname'] + " " + values['name'],
                                                                  login_str))

        apple_script = "osascript -e 'tell application \"Notes\"\n" \
                       "set noteName to get name of the first note\n" \
                       "set bodyNote to get body of note noteName\n" \
                       "set body of note noteName to bodyNote & \"%s\"\n" \
                       "end tell'" % (values['surname'] + " " + values['name'] + " " + values['group'])
        os.system(apple_script)
        return redirect(url_for("send_page"))


@app.route('/pass', methods=['GET'])
def send_page():
    if not session.get('login'):
        return json.dumps({"status": "Ошибка", "error": "Пройдите авторизацию ещё раз"}, ensure_ascii=False)
    return render_template('test.html')


@app.route('/sendFile', methods=['POST'])
def send_file():
    if request.method == 'POST':
        if 'file' not in request.files or len(request.files['file'].filename) == 0:
            return render_template('test.html', json={"status": 'Ошибка', "errorMessage": 'Нет файла'})
        elif 'task' not in request.values:
            return render_template('test.html', json={"status": 'Ошибка', "errorMessage": 'Не выбрана задача'})
        elif not is_allowed_file(request.files['file'].filename, app.config["ALLOWED_FILE_EXTENSION"]):
            return render_template('test.html',
                                   json={"status": 'Ошибка', "errorMessage": 'Данный файл запрещен на сервере'})
        else:
            generated = str(uuid.uuid4()).replace('-', '')
            file = request.files['file']

            app.logger.warning("%s generate uuid (%s) for task %s." % (session.get('login'),
                                                                       generated, request.values['task']))

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], request.values['task'], generated + ".scm"))
            return redirect(url_for("test_task", task=request.values['task'], uuid=generated))


@app.route('/test', methods=['GET'])
def test_task():
    if not session.get('login'):
        return json.dumps({"status": "Ошибка", "error": "Пройдите авторизацию ещё раз"}, ensure_ascii=False)
    task = request.args.get('task')
    uuid_task = request.args.get('uuid')
    if task is None:
        return render_template('test.html', json={"status": 'Ошибка', "errorMessage": 'Не выбрана задача'})
    elif uuid_task is None:
        return render_template('test.html', json={"status": 'Ошибка', "errorMessage": 'Не введен uuid задачи'})
    elif not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], task, uuid_task + ".scm")):
        return render_template('test.html', json={"status": 'Ошибка', "errorMessage": 'Введите правильный uuid'})
    elif url_test[task] is None:
        extension = ".scm"
        file = os.path.join("tmp", task, uuid_task + extension)
        os.rename(file, os.path.join("tmp", task, session.get("login") + ".scm"))
        return render_template('test.html', json={"status": 'Неизвестно',
                                                  "errorMessage": 'Тестирование этой задачи происходит через '
                                                                  'преподавателя'})
    else:
        test_number = 8 if task == "dz3" else 1
        extension = ".scm"
        file = os.path.join("tmp", task, uuid_task + extension)
        while True:
            while session.get("login") in ignore_test and test_number in ignore_test[session.get("login")]:
                test_number += 1

            if requests.get(url_test[task] + "/" + str(test_number)).status_code == 404 and test_number != 1:
                app.logger.warning("%s %s\n All tests is success" % (session.get('login'), file))
                os.rename(file, os.path.join("tmp", task, session.get("login") + ".scm"))
                return render_template('test.html', json={"status": 'Успех', "message": 'Все тесты пройдены!'})
            elif requests.get(url_test[task] + "/" + str(test_number)).status_code == 404 and test_number == 1:
                return render_template('test.html', json={"status": 'Ошибка', "message": 'Обратитесь позднее'})

            with open("tmp/test-%s.txt" % uuid_task, mode='w') as file_test:
                test = requests.get(url_test[task] + "/" + str(test_number)).text
                file_test.write(test)
            with open("tmp/answer-%s.txt" % uuid_task, mode='w') as file_test:
                answer = requests.get(url_test[task] + "/" + str(test_number) + ".a").text
                file_test.write(answer)

            command = "guile  --no-auto-compile -l " + file + " <tmp/test-%s.txt | grep '$1'" % uuid_task

            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                           executable="/bin/zsh")
                output, error = process.communicate(timeout=5)
                output = output.decode()
                output = output.replace("$1 = ", "").replace("\n", "")
                error = error.decode()
                app.logger.info("%s %s\n Output for file - %s,\n error for file - %s" % (session.get('login'),
                                                                                            file, output, error))
            except:
                os.rename(file, os.path.join("tmp", task, uuid_task + "-" + session.get("login") + ".scm"))
                return render_template('test.html', json={"status": 'Ошибка', "errorMessage": 'Превышен лимит по '
                                                                                              'времени в тесте №' +
                                                                                              str(test_number),
                                                          "test": test})
            if answer.strip().replace("\n", "") != output.strip().replace("\n", ""):
                app.logger.warning("%s %s\n Test №%d, %s %s" % (session.get('login'), file, test_number, answer,
                                                                output))
                app.logger.warning("%s %s\n Command: %s" % (session.get('login'), file, command))
                os.rename(file, os.path.join("tmp", task, uuid_task + "-" + session.get("login") + ".scm"))
                return render_template('test.html',
                                       json={"status": 'Ошибка', "errorMessage": 'Неправильный ответ для теста № ' +
                                                                                 str(test_number),
                                             "test": test, "answer": answer})
            test_number += 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=False, threaded=True)
