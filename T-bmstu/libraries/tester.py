#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import tkinter
from tkinter import messagebox
import tkinter.font
import tkinter.filedialog
import urllib.request
from urllib.request import HTTPError
import subprocess
import zipfile
import shutil
import webbrowser
import smtplib

def compare_files(answer,output):
    checking = checking_listbox.get(checking_listbox.curselection())
    command=""
    if checking == "BINARY":
        command="cmp " + answer + " " + output
    elif checking == "TEXT":
        command="diff --text -q" + answer + " " + output
    elif checking == "SCAN":
        command="diff -wbq " + answer + " " + output
    elif checking == "INTEGER":
        command="diff -wbq " + answer + " " + output
        with open(answer) as fp:
            text = fp.read()
            text = text.replace("\n","")
            text = text.replace("\t","")
            text = text.replace("\r","")
            text = text.replace(" ","")
            try:
                number_answer = int(text,base=36)
            except:
                messagebox.showinfo("Error in checking", "Запрещено использовать эту стратегию проверки.\nЗамените на другую")
                return False
        with open(output) as fp:
            text = fp.read()
            text = text.replace("\n","")
            text = text.replace("\t","")
            text = text.replace("\r","")
            text = text.replace(" ","")
            try:
                number_output = int(text,base=36)
            except:
                messagebox.showinfo("Error in checking", "Запрещено использовать эту стратегию проверки.\nЗамените на другую")
                return False
        if number_answer != number_output:
            return False
    elif checking == "FLOAT":
        command="diff -wbq " + answer + " " + output
        with open(answer) as fp:
            text = fp.read()
            text = text.replace("\n","")
            text = text.replace("\t","")
            text = text.replace("\r","")
            text = text.replace(" ","")
            try:
                number_answer = float(text)
            except:
                messagebox.showinfo("Error in checking", "Запрещено использовать эту стратегию проверки.\nЗамените на другую")
                return False
        with open(output) as fp:
            text = fp.read()
            text = text.replace("\n","")
            text = text.replace("\t","")
            text = text.replace("\r","")
            text = text.replace(" ","")
            try:
                number_output = float(text)
            except:
                messagebox.showinfo("Error in checking", "Запрещено использовать эту стратегию проверки.\nЗамените на другую")
                return False
        number_dec=len(str(number_answer-int(number_answer)).split('.')[1])
        number_output=round(number_output,number_dec)
        if number_answer != number_output:
            return False
    process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output, error = process.communicate()
    output = output.decode()
    error = error.decode()
    if output!="":
        return False
    else:
        return True

def error_and_right(answer,output):
    print("Правильный ответ:")
    with open(answer) as fp:
        for line in fp:
            print(line,end="")
    print("")
    print("Полученный ответ:")
    with open(output) as fp:
        for line in fp:
            print(line,end="")
    return None

def test_program():
    global test_url
    global args_flag
    global file_flag
    global compile_flag
    if compile_flag==False:
        messagebox.showinfo("Error", "Проведите компиляцию вашего кода!")
        return None
    if test_url.get()!="":
        magic_url=test_url.get()
    else:
        try:
            magic_url = urllib.request.urlopen(test_url_const).readline().decode()
            magic_lines = urllib.request.urlopen(test_url_const).read().decode().splitlines()
            magic_url=magic_url.replace("T-BMSTU",t_bmstu_ip.get())
            program=file_path.get()[file_path.get().rfind("/")+1:]
            program=program[:program.find(".")]
            program_low = program.lower()
            test_string=""
            for s in filter (lambda x: program in x, magic_lines):
                test_string = s
            for s in filter (lambda x: program_low in x, magic_lines):
                test_string = s
            if test_string == "":
                messagebox.showinfo("Error", "Возникла неизвестная ошибка\nУкажите правильное имя\n"
                                            "или введите ссылку на тесты")
            else:
                test_string=test_string.split(";")[1:]
                magic_url=magic_url.replace("AAA",test_string[2])
                magic_url=magic_url.replace("BBB",test_string[1])
                magic_url=magic_url.replace("CCC",test_string[0])
                magic_url=magic_url.replace("\n","")
        except HTTPError as e:
            messagebox.showinfo("Test", "Неизвестная ошибка про попытке к github.com")
            print(e.reason)
    test_number = 1
    while True:
        try:
            if file_flag==True and language_choose.get()==0:
                test_url1 = magic_url + str(test_number) + ".main.c"
                try:
                    elem_h = magic_url + "elem.h"
                    header = urllib.request.urlopen(elem_h).read().decode()
                    with open("elem.h",mode="w") as file:
                        file.write(header)
                except:
                    elem_h = ""
                answer_url = magic_url + str(test_number) +".a"
            elif args_flag==True and language_choose.get()==0:
                test_url1 = magic_url + str(test_number) + ".arg"
                if program == "frame":
                    answer_url = magic_url + str(test_number) +".exact.a"
                else:
                    answer_url = magic_url + str(test_number) +".a"
            elif file_flag==True and language_choose.get()==1:
                if program=="textstats":
                    textstats_url = magic_url + "textstats.hpp"
                    textstats_hpp = urllib.request.urlopen(textstats_url).read().decode()
                    with open("textstats.hpp",mode="w") as file:
                        file.write(textstats_hpp)
                    test_url_cpp = magic_url + "test.cpp"
                    test_cpp = urllib.request.urlopen(test_url_cpp).read().decode()
                    with open("test.cpp",mode="w") as file:
                        file.write(test_cpp)
                    if test_number<10:
                        test_url1 = magic_url + "0" + str(test_number)
                        answer_url = test_url1 + ".a"
                    else:
                        test_url1 = magic_url + str(test_number)
                        answer_url = test_url1 + ".a"
                elif program=="spellchecker":
                    count_big_url = magic_url + "count_big.txt"
                    count_big = urllib.request.urlopen(count_big_url).read().decode()
                    with open("count_big.txt",mode="w") as file:
                        file.write(count_big)
                    test_url1 = magic_url + str(test_number)
                    answer_url = test_url1 + ".a"
                elif program=="supercalc":
                    test_url_cpp = magic_url + str(test_number) +".test.cpp"
                    test_cpp = urllib.request.urlopen(test_url_cpp).read().decode()
                    with open("test.cpp",mode="w") as file:
                        file.write(test_cpp)
                    test_url1 = magic_url + str(test_number)
                    answer_url = test_url1 + ".a"
            elif file_flag==True and language_choose.get()==2:
                if (test_string[5].find("++")!=-1 and program!="SparseSet") or test_number!=1:
                    if test_string[5].find("+++")!=-1:
                        hintable = magic_url + "Hintable.java"
                        header2 = urllib.request.urlopen(hintable).read().decode()
                        with open("Hintable.java",mode="w") as file:
                            file.write(header2)
                        stub = magic_url + str(test_number) + ".Stub.java"
                        header3 = urllib.request.urlopen(stub).read().decode()
                        with open("Stub.java",mode="w") as file:
                            file.write(header3)
                        assert_java = magic_url + str(test_number) + ".Assert.java"
                        header = urllib.request.urlopen(assert_java).read().decode()
                        with open("Assert.java",mode="w") as file:
                            file.write(header)
                    else:
                        assert_java = magic_url + "Assert.java"
                        header = urllib.request.urlopen(assert_java).read().decode()
                        with open("Assert.java",mode="w") as file:
                            file.write(header)
                    test_url1 = magic_url + str(test_number) + ".Test" + str(test_number) + ".java"
                    answer_url = magic_url + str(test_number) + ".a"
                elif program=="SparseSet":
                    vertex = magic_url + "1.Vertex.java"
                    header = urllib.request.urlopen(vertex).read().decode()
                    with open("Vertex.java",mode="w") as file:
                        file.write(header)
                    hintable = magic_url + "Hintable.java"
                    header2 = urllib.request.urlopen(hintable).read().decode()
                    with open("Hintable.java",mode="w") as file:
                        file.write(header2)
                    test_url1 = magic_url + str(test_number) + ".Test" + str(test_number) + ".java"
                    answer_url = magic_url + str(test_number) + ".a"
                else:
                    test_url1 = magic_url + str(test_number) + ".Test.java"
                    answer_url = magic_url + str(test_number) + ".a"
            elif args_flag==True and language_choose.get()==2:
                test_url1 = magic_url + str(test_number) + ".arg"
                answer_url = magic_url + str(test_number) +".a"
            else:
                test_url1 = magic_url + str(test_number)
                answer_url = test_url1 + ".a"
            try:
                test = urllib.request.urlopen(test_url1).read().decode()
            except:
                test_url1=test_url1.replace("Test1.java","EratostheneSieve.java")
                test = urllib.request.urlopen(test_url1).read().decode()
                test_url1=test_url1.replace(".EratostheneSieve.java","")
                value = urllib.request.urlopen(test_url1).read().decode()
            answer = urllib.request.urlopen(answer_url).read().decode()
        except HTTPError as connection_error:
            code=connection_error.code
            if code==404:
                messagebox.showinfo("Test", "Все тесты пройдены!")
                break
            else:
                messagebox.showinfo("Test", "Неизвестная ошибка про попытке к соединению\n" + "Номер теста " + str(test_number))
        if file_flag == False:
            test_file = open("test.txt", "w")
        elif language_choose.get()==0:
            test_file = open("test.c", "w")
        elif language_choose.get()==1:
            test_file = open("test.txt", "w")
        elif language_choose.get()==2 and test_string[5].find("+++")!=-1:
            test_file = open("Test" + str(test_number) + ".java", "w")
        elif language_choose.get()==2 and test_string[5].find("++")!=-1 and (test_number!=1 or program=="SkipList"):
            test_file = open("Test" + str(test_number) + ".java", "w")
        elif language_choose.get()==2 and test_string[5].find("++")!=-1:
            test_file = open("EratostheneSieve.java", "w")
            test_file2 = open("test.txt","w")
            test_file2.write(value)
            test_file2.close()
        elif language_choose.get()==2:
            test_file = open("Test.java", "w")
        answer_file = open("answer.txt","w")
        test_file.write(test)
        answer_file.write(answer)
        test_file.close()
        answer_file.close()
        if language_choose.get()==0 and file_flag == True:
            os.system("cp " + file_path.get() + " " + file_path.get()[file_path.get().rfind("/")+1:])
            if elem_h:
                command = "gcc " + file_path.get()[file_path.get().rfind("/")+1:] + " test.c elem.h && valgrind -q ./a.out"
            else:
                command = language_string.get() + "test.c && valgrind -q ./a.out"
        elif language_choose.get()==0 and args_flag == True:
            command = "valgrind -q ./a.out " + test
        elif language_choose.get()==1 and file_flag == True:
            os.system("cp " + file_path.get() + " " + file_path.get()[file_path.get().rfind("/")+1:])
            if program=="textstats":
                command = "g++ textstats.hpp textstats.cpp test.cpp -std=c++11 && valgrind -q ./a.out <test.txt"
            elif program=="spellchecker":
                command = "g++ spellchecker.cpp -std=c++11 && ./a.out <test.txt"
            elif program=="supercalc":
                command = "g++ supercalc.hpp test.cpp -std=c++11 && valgrind -q ./a.out <test.txt"
        elif language_choose.get()==0 or language_choose.get()==1:
            command = "valgrind -q ./a.out <test.txt"
        elif language_choose.get()==2 and args_flag == True:
            os.system("cd " + os.getcwd())
            command = "java -cp " + os.getcwd() + " " + file_path.get()[file_path.get().rfind("/")+1:file_path.get().rfind(".")] + " " + test
            files=test.split(" ")
            files[0]=files[0].replace(".","_")
            files[1]=files[1].replace(".","_")
            files[1]=files[1].replace("\n","")
            if (os.path.exists(os.getcwd() + "/"+ files[0])) and (os.path.exists(os.getcwd() + "/"+ files[1])):
                shutil.rmtree(os.getcwd() + "/"+ files[0])
                shutil.rmtree(os.getcwd() + "/"+ files[1])
            urllib.request.urlretrieve(magic_url + str(test_number) +"." + files[0] + ".zip","1.zip")
            urllib.request.urlretrieve(magic_url + str(test_number) +"." + files[1] + ".zip","2.zip")
            zip1 = zipfile.ZipFile("1.zip")
            zip1.extractall(os.getcwd())
            zip2 = zipfile.ZipFile("2.zip")
            zip2.extractall(os.getcwd())
        elif language_choose.get()==2 and file_flag == True:
            if test_string[5].find("++")!=-1:
                if program=="SparseSet":
                    if test_number==1:
                        command = "javac " + os.getcwd() + "/Test" + str(test_number) + ".java " + os.getcwd() + "/" + program + ".java "
                        command += os.getcwd() + "/Hintable.java " + os.getcwd() + "/Vertex.java && java -cp " + os.getcwd() + " " + " Test" + str(test_number)
                    else:
                        command = "javac " + os.getcwd() + "/Test" + str(test_number) + ".java " + os.getcwd() + "/" + program + ".java "
                        command += os.getcwd() + "/Hintable.java " + os.getcwd() + "/Assert.java "
                        command += os.getcwd() + "/Stub.java && java -cp " + os.getcwd() + " " + " Test" + str(test_number)
                else:
                    os.system("cd " + os.getcwd())
                    if test_number!=1 or program=="SkipList":
                        command = "javac " + os.getcwd() + "/Test" + str(test_number) + ".java " + os.getcwd() + "/" + program + ".java "
                        command += os.getcwd() + "/Assert.java && java -cp " + os.getcwd() + " " + " Test" + str(test_number)
                    else:
                        command = "javac " + os.getcwd() + "/EratostheneSieve.java " + os.getcwd() + "/" + program + ".java "
                        command += os.getcwd() + "/Assert.java && java -cp " + os.getcwd() + " " + " EratostheneSieve <test.txt"
            else:
                os.system("cd " + os.getcwd())
                command = "javac " + os.getcwd() + "/Test.java " + os.getcwd() + "/" + program + ".java && java -cp " + os.getcwd() + " " + " Test"
        elif language_choose.get()==2:
            os.system("cd " + os.getcwd())
            command = "java -cp " + os.getcwd() + " " + file_path.get()[file_path.get().rfind("/")+1:file_path.get().rfind(".")] + " " + "<test.txt"
        elif language_choose.get()==3 or language_choose.get()==4 or language_choose.get()==5:
            command = language_string.get() + " <test.txt"
        elif language_choose.get()==6:
            messagebox.showinfo("Test","Временно возникли проблемы")
            break
        try:
            process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            output, error = process.communicate(timeout=int(timeout_.get()))
            output = output.decode()
        #    print(output)
            error = error.decode()
        except:
            messagebox.showerror("Test", "Превышен лимит по времени:\nограничение -- " + str(int(timeout_.get())) + " с\n в тесте №" + str(test_number))
            compile_flag=False
            break
        if error != "" and (language_choose.get()==0 or language_choose.get()==1):
            messagebox.showerror("Test", "valgrind показывает ошибки в тесте " + str(test_number))
            compile_flag=False
            print(error)
            break
        elif error != "" and error.find("-Xlint:unchecked")==-1:
            messagebox.showerror("Test", "Неизвестная ошибка в тесте " + str(test_number))
            compile_flag=False
            print(error)
            break
        output_file = open("output.txt", "w")
        if language_choose.get()==4:
            output=output.replace("guile> ","")
            print(output,end="")
        output_file.write(output)
        output_file.close()
        if compare_files("answer.txt","output.txt") == False:
            messagebox.showerror("Test", "Неправильный ответ для теста № " + str(test_number))
            compile_flag=False
            error_and_right("answer.txt","output.txt")
            break
        test_number +=1

def compile_program():
    global file_flag
    global args_flag
    magic_lines = urllib.request.urlopen(test_url_const).read().decode().splitlines()
    program=file_path.get()[file_path.get().rfind("/")+1:]
    program=program[:program.find(".")]
    program_low = program.lower()
    test_string=""
    for s in filter (lambda x: program in x, magic_lines):
        test_string = s
    for s in filter (lambda x: program_low in x, magic_lines):
        test_string = s
    if test_string == "":
        messagebox.showinfo("Error", "Возникла неизвестная ошибка\nУкажите правильное имя\n")
        return None
    test_string=test_string.split(";")[1:]
    file_flag = False
    args_flag = False
    if test_string[5].find("+")!=-1:
        file_flag = True
    elif test_string[4].find("+")!=-1:
        args_flag = True
    if compile_string.get().find("javac")!=-1:
        os.system("cp " + file_path.get() + " " + file_path.get()[file_path.get().rfind("/")+1:])
        os.system("cd " + os.getcwd())
        language_string.set("javac " + file_path.get()[file_path.get().rfind("/")+1:])
    if compile_string.get().find("python3")!=-1 or compile_string.get().find("ruby")!=-1 or compile_string.get().find("guile")!=-1:
        messagebox.showinfo("Compile", "Компиляция не нужна для выбранного языка")
        return None
    if file_flag:
        messagebox.showinfo("Compile", "Компиляция и тестирование программы\n выполняется непосредственно при тесте программы")
        return None
    process = subprocess.Popen(compile_string.get(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output, error = process.communicate()
    error = error.decode()
    if error == "":
        messagebox.showinfo("Compile", "Компиляция прошла удачно!")
        compile_flag=True
    else:
        messagebox.showerror("Compile", "Компиляция не была проведена. Возникла ошибка")
        compile_flag=False
        print(error)

def choose_directory():
    directory_path = tkinter.filedialog.askopenfilename(initialdir="/home/",title="Выберите файл для компиляции")
    old_directory = file_path.get()
    if directory_path:
        file_path.set(directory_path)
        old_compile = language_string.get()
        new_compile = old_compile.replace(old_directory,directory_path)
        language_string.set(new_compile)
    return None

def create_choose_language(frame,list,v):
   buttons=[]
   for text,value in list:
       new_button = tkinter.Radiobutton(frame,text=text,value=value,variable=v,command=compile_string_2)
       buttons.append(new_button)
   return buttons

def compile_string_2():
    if language_choose.get()==0:
        language_string.set("gcc " + str(file_path.get()) + " ")
    elif language_choose.get()==1:
        language_string.set("g++ " + str(file_path.get()) + " " + "-std=c++11")
    elif language_choose.get()==2:
        language_string.set("javac " + str(file_path.get()) + " ")
    elif language_choose.get()==3:
        language_string.set("python3 " + str(file_path.get()) + " ")
    elif language_choose.get()==4:
        language_string.set("guile-1.8 -l " + str(file_path.get()) + " ")
    elif language_choose.get()==5:
        language_string.set("ruby " + str(file_path.get()) + " ")
    elif language_choose.get()==6:
        messagebox.showinfo("Choose language", "Временно недоступно")

def timeout_change():
    changing=("ограничение -- " + str(int(timeout_.get())) + " c")
    timeout_label2.config(text=changing)
    return None

def t_bmstu_window():
    def changing_ip():
        if t_bmstu_ip2.get():
            t_bmstu_ip.set(t_bmstu_ip2.get())
    new_window = tkinter.Toplevel()
    new_window.geometry("260x100")
    new_window.title("T-bmstu ip")
    t_bmstu_ip2 = tkinter.StringVar()
    t_bmstu_ip2.set(t_bmstu_ip.get())
    t_bmstu_label2=tkinter.Label(new_window,text="Сайт t-bmstu(изменен с 2015 г.):",width=30)
    t_bmstu_entry2=tkinter.Entry(new_window,width=40,textvariable=t_bmstu_ip2)
    ok_button = tkinter.Button(new_window,text="Change")
    ok_button.bind("<Button-1>",lambda event:changing_ip())
    quit_button = tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    t_bmstu_label2.pack()
    t_bmstu_entry2.pack()
    info_label=tkinter.Label(new_window,text="Укажите работающий(!) сервер\nтестирования T-bmstu")
    info_label.pack()
    ok_button.pack(side=tkinter.LEFT)
    quit_button.pack(side=tkinter.LEFT)


def test_url_window():
    def changing_url():
        test_url.set(test_url2.get())
    new_window = tkinter.Toplevel()
    new_window.geometry("330x160")
    new_window.title("Test url")
    test_url2 = tkinter.StringVar()
    test_url2.set(test_url.get())
    test_url_label2=tkinter.Label(new_window,text="Введите ссылку на тесты\n (если возникнет неизвестная ошибка):",width=30)
    test_url_entry2=tkinter.Entry(new_window,width=40,textvariable=test_url2)
    ok_button = tkinter.Button(new_window,text="Change")
    ok_button.bind("<Button-1>",lambda event:changing_url())
    quit_button = tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    test_url_label2.pack()
    test_url_entry2.pack()
    info_label=tkinter.Label(new_window,text="В связи с неизвестными ошибками,\nследует заполнять это поле ссылкой на тесты.\n"
                                             "Но это должно выполняться автоматически\n(вычисляется адрес с помощью некоторой таблицы)")
    info_label.pack()
    ok_button.pack(side=tkinter.LEFT)
    quit_button.pack(side=tkinter.LEFT)

def compile_string_window():
    def changing_compile():
        if language_string2.get():
            language_string.set(language_string2.get())
    new_window = tkinter.Toplevel()
    new_window.geometry("420x120")
    new_window.title("Compile string")
    language_string2 = tkinter.StringVar()
    language_string2.set(language_string.get())
    language_string_label2=tkinter.Label(new_window,text="Строка компиляции для bash",width=30)
    language_string_entry2=tkinter.Entry(new_window,width=50,textvariable=language_string2)
    ok_button = tkinter.Button(new_window,text="Change")
    ok_button.bind("<Button-1>",lambda event:changing_compile())
    quit_button = tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    language_string_label2.pack()
    language_string_entry2.pack()
    info_label=tkinter.Label(new_window,text="Пропишите строку компиляция для определенного языка\n программирования, дополняя его ключами.\n"
                                             "Например, -O3, -Wall, -Xlint:unchecked, -std=c++11")
    info_label.pack()
    ok_button.pack(side=tkinter.LEFT)
    quit_button.pack(side=tkinter.LEFT)

def language_choose_window():
    new_window = tkinter.Toplevel()
    new_window.geometry("220x220")
    new_window.title("Language choose")
    buttons = create_choose_language(new_window,language_list,language_choose)
    language_choose_label2=tkinter.Label(new_window,text="Выберите один \n из языков программирования,\nна котором выполнена программа",width=30)
    quit_button = tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    language_choose_label2.pack()
    for button in buttons:
        button.pack()
    quit_button.pack()


def timeout_window():
    def changing_timeout():
        timeout_.set(timeout_spinbox.get())
        timeout_change()
    new_window = tkinter.Toplevel()
    new_window.geometry("220x120")
    new_window.title("Timeout of the task")
    timeout_label2=tkinter.Label(new_window,text="Укажите предел по времени",width=30)
    timeout_spinbox = tkinter.Spinbox(new_window,from_=1,to=20)
    ok_button = tkinter.Button(new_window,text="Change")
    ok_button.bind("<Button-1>",lambda event:changing_timeout())
    quit_button = tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    timeout_label2.pack()
    timeout_spinbox.pack()
    info_label=tkinter.Label(new_window,text="Для всех задач, установлен\nопределенный предел по времени\nУкажите его.")
    info_label.pack()
    ok_button.pack(side=tkinter.LEFT)
    quit_button.pack(side=tkinter.LEFT)

def checking_window():
    def create_checking_strategy(frame,list,v):
        buttons=[]
        for text,value in list:
            new_button = tkinter.Radiobutton(frame,text=text,value=value,variable=v,command=choose_strategy)
            buttons.append(new_button)
        return buttons
    def choose_strategy():
        changing = "Вы выбрали\nспособ проверки\n"
        if checking2.get()==0:
            checking_listbox.activate(index=0)
            changing += "SCAN"
        elif checking2.get()==1:
            checking_listbox.activate(index=1)
            changing += "BINARY"
        elif checking2.get()==2:
            checking_listbox.activate(index=2)
            changing += "TEXT"
        elif checking2.get()==3:
            checking_listbox.activate(index=3)
            changing += "INTEGER"
        elif checking2.get()==4:
            checking_listbox.activate(index=4)
            changing += "FLOAT"
        changing2 = changing.replace("\n", " ")
        checking_label2.config(text=changing)
        checking2_label.config(text=changing2)
    new_window = tkinter.Toplevel()
    new_window.geometry("300x220")
    new_window.title("Checking strategy")
    checking2=tkinter.IntVar()
    buttons = create_checking_strategy(new_window,[("SCAN","0"),("BINARY","1"),("TEXT","2"),("INTEGER","3"),("FLOAT","4")],checking2)
    language_choose_label2=tkinter.Label(new_window,text="Укажите способ проверки",width=30)
    info_label=tkinter.Label(new_window,text="Также для всех задач, установлен\n определенный способ проверки задачи")
    info_label.pack()
    quit_button = tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    language_choose_label2.pack()
    for button in buttons:
        button.pack()
    quit_button.pack()
    checking2_label = tkinter.Label(new_window,text="Вы выбрали способ проверки SCAN")
    checking2_label.pack()
    return None

def checking_change():
    checking = checking_listbox.get(checking_listbox.curselection())
    changing = "Вы выбрали\nспособ проверки\n"
    if checking=="SCAN":
        changing += "SCAN"
        checking_label2.config(text=changing)
    elif checking=="BINARY":
        changing += "BINARY"
        checking_label2.config(text=changing)
    elif checking=="TEXT":
        changing += "TEXT"
        checking_label2.config(text=changing)
    elif checking=="INTEGER":
        changing += "INTEGER"
        checking_label2.config(text=changing)
    elif checking=="FLOAT":
        changing += "FLOAT"
        checking_label2.config(text=changing)
    return None

def tasks_window():
    global buffer
    buffer=None
    def number_term():
        checking = term_listbox.get(term_listbox.curselection())
        subject_listbox.delete(0,tkinter.END)
        if checking.find("Первый")!=-1:
            subject_listbox.insert(tkinter.END,"Алгоритмы и структуры данных")
            subject_listbox.insert(tkinter.END,"Основы информатики")
        elif checking.find("Второй")!=-1:
            subject_listbox.insert(tkinter.END,"Языки и методы программирования")
            subject_listbox.insert(tkinter.END,"Дискретная математика")
        return None
    def subject_term():
        global buffer
        checking = subject_listbox.get(subject_listbox.curselection())
        module_listbox.delete(0,tkinter.END)
        if checking.find("Языки и методы")==-1:
            module_listbox.insert(tkinter.END,"Первый модуль")
            module_listbox.insert(tkinter.END,"Второй модуль")
            module_listbox.insert(tkinter.END,"Третий модуль")
            module_listbox.config(height=3)
        elif checking.find("Языки и методы")!=-1:
            module_listbox.insert(tkinter.END,"Первый модуль")
            module_listbox.insert(tkinter.END,"Второй модуль")
            module_listbox.config(height=2)
        buffer = checking
        return None
    def tasks_module():
        checking = buffer
        checking2 = module_listbox.get(module_listbox.curselection())
        tasks_listbox.delete(0,tkinter.END)
        task_url_const = test_url_const.replace("tests","tasks")
        task = urllib.request.urlopen(task_url_const).read().decode()
        task = task.split("###")
        if checking.find("Алгоритмы")!=-1:
            if checking2.find("Первый")!=-1:
                tasks=task[0]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=18)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
            elif checking2.find("Второй")!=-1:
                tasks=task[1]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=21)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
            elif checking2.find("Третий")!=-1:
                tasks=task[2]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=14)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
        elif checking.find("Основы")!=-1:
            if checking2.find("Первый")!=-1:
                tasks=task[3]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=15)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
            elif checking2.find("Второй")!=-1:
                tasks=task[4]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=16)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
            elif checking2.find("Третий")!=-1:
                tasks=task[5]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=7)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
        elif checking.find("Языки")!=-1:
            if checking2.find("Первый")!=-1:
                tasks=task[6]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=12)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
            elif checking2.find("Второй")!=-1:
                tasks=task[7]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=3)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
        elif checking.find("Дискретная")!=-1:
            if checking2.find("Первый")!=-1:
                tasks=task[8]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=7)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
            elif checking2.find("Второй")!=-1:
                tasks=task[9]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=6)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
            elif checking2.find("Третий")!=-1:
                tasks=task[10]
                tasks=tasks.replace("\n","").replace("\'","").replace("\"","").split(";")
                tasks_listbox.config(height=4)
                for task in tasks:
                    tasks_listbox.insert(tkinter.END,task)
        return None
    def tasks_html():
        task_url_const = test_url_const.replace("tests","tasks")
        task = urllib.request.urlopen(task_url_const).read().decode()
        task = task.replace("###","").replace("\n","").replace("\'","").replace("\"","").split(";")
        choose = tasks_listbox.get(tasks_listbox.curselection())
        text = urllib.request.urlopen(test_url_const).read().decode().splitlines()
        text_url = text[0].replace("T-BMSTU",t_bmstu_ip.get())
        test_string=text[task.index(choose)+2].split(";")[1:]
        text_url=text_url.replace("AAA",test_string[2]).replace("BBB",test_string[1])
        text_url=text_url.replace("CCC",test_string[0]).replace("\n","").replace("tests/","text/text.html")
        urllib.request.urlretrieve(text_url,"test.html")
        return None
    def open_url():
        if messagebox.askokcancel("Exception","Вы согласны прочитать условие задачи?"):
            webbrowser.open("file://" + os.getcwd() + "/test.html")
            quit()
        return None
    new_window = tkinter.Toplevel()
    new_window.geometry("500x550")
    new_window.title("Сonditions of the task")
    info_label=tkinter.Label(new_window,text="Вы можете прочитать условия задач,\nуказав название задачи\n"
                                             "Действовать строго(!) по цифрам")
    info_label.grid(row=1,column=1,columnspan=2)
    term_label=tkinter.Label(new_window,text="1.Укажите номер семестра")
    term_label.grid(row=2,column=1)
    term_listbox=tkinter.Listbox(new_window,height=2,width=40,selectmode=tkinter.SINGLE)
    term_listbox.insert(tkinter.END,"Первый семестр")
    term_listbox.insert(tkinter.END,"Второй семестр")
    term_listbox.bind('<<ListboxSelect>>',lambda event:number_term())
    term_listbox.grid(row=2,column=2)
    subject_label=tkinter.Label(new_window,text="2.Выберите предмет")
    subject_label.grid(row=3,column=1)
    subject_listbox=tkinter.Listbox(new_window,height=2,width=40,selectmode=tkinter.SINGLE)
    subject_listbox.bind('<<ListboxSelect>>',lambda event:subject_term())
    subject_listbox.grid(row=3,column=2)
    module_label=tkinter.Label(new_window,text="3.Укажите номер модуля")
    module_label.grid(row=4,column=1)
    module_listbox=tkinter.Listbox(new_window,height=3,width=40,selectmode=tkinter.SINGLE)
    module_listbox.bind('<<ListboxSelect>>',lambda event:tasks_module())
    module_listbox.grid(row=4,column=2)
    tasks_label=tkinter.Label(new_window,text="4.Выберите задачу")
    tasks_label.grid(row=5,column=1)
    tasks_listbox=tkinter.Listbox(new_window,height=1,width=40,selectmode=tkinter.SINGLE)
    tasks_listbox.bind('<<ListboxSelect>>',lambda event:tasks_html())
    tasks_listbox.grid(row=5,column=2)
    view_button = tkinter.Button(new_window,text="View",command=open_url)
    view_button.grid(row=6,column=1)
    quit_button = tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    quit_button.grid(row=6,column=2)

def help_window():
    new_window = tkinter.Toplevel()
    new_window.geometry("750x450")
    new_window.title("Help")
    info_url = test_url_const.replace("tests","info")
    info_text = urllib.request.urlopen(info_url).read().decode()
    scrollbar_ = tkinter.Scrollbar(new_window,orient=tkinter.VERTICAL)
    scrollbar_.pack(fill=tkinter.Y,side=tkinter.RIGHT,expand=tkinter.FALSE)
    info_label=tkinter.Text(new_window,wrap=tkinter.WORD,yscrollcommand=scrollbar_.set)
    info_label.insert(1.0,info_text)
    info_label.pack(side=tkinter.LEFT,expand=tkinter.YES,fill=tkinter.BOTH)
    info_label.config(state=tkinter.DISABLED)
    scrollbar_.config(command=info_label.yview)
    return None

def about_window():
    def destroy():
        new_window.destroy()
    new_window = tkinter.Toplevel()
    new_window.geometry("410x150")
    new_window.title("About...")
    version_url = test_url_const.replace("tests","version")
    version_text = urllib.request.urlopen(version_url).read().decode()
    info_label=tkinter.Text(new_window)
    info_label.insert(1.0,version_text)
    info_label.pack(side=tkinter.LEFT,expand=tkinter.YES,fill=tkinter.BOTH)
    info_label.config(state=tkinter.DISABLED)
    quit_button = tkinter.Button(info_label,text="Quit",command=destroy)
    info_label.window_create(tkinter.END,window=quit_button)
    return None

def version_window():
    new_window = tkinter.Toplevel()
    new_window.geometry("710x600")
    new_window.title("Version")
    version_url = test_url_const.replace("tests.txt","ChangeLog")
    version_text = urllib.request.urlopen(version_url).read().decode()
    scrollbar_ = tkinter.Scrollbar(new_window,orient=tkinter.VERTICAL)
    scrollbar_.pack(fill=tkinter.Y,side=tkinter.RIGHT,expand=tkinter.FALSE)
    version_label=tkinter.Text(new_window,wrap=tkinter.WORD,yscrollcommand=scrollbar_.set)
    version_label.insert(1.0,version_text)
    version_label.pack(side=tkinter.LEFT,expand=tkinter.YES,fill=tkinter.BOTH)
    version_label.config(state=tkinter.DISABLED)
    scrollbar_.config(command=version_label.yview)
    return None

def contact_window():
    def show_password():
        if password_intvar.get()==1:
            password_entry.config(show="")
        else:
            password_entry.config(show="*")
    def send_email():
        message= "\r\n".join(["From: " + user_var.get(),"To: runnerpeople@gmail.com","Subject: Help",
                              "",message_text.get(1.0,tkinter.END)])
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user_var.get(), password_var.get())
            server.sendmail(user_var.get(), "runnerpeople@gmail.com", message)
            server.close()
            messagebox.showinfo("Сообщение","Сообщение было отправлено!\nОжидайте ответа")
        except:
            messagebox.showerror("Сообщение","Сообщение не было отправлено!\nОшибка внутренняя")
        return None
    new_window = tkinter.Toplevel()
    new_window.geometry("300x400")
    new_window.title("Contact Us")
    info_label=tkinter.Label(new_window,text="Поддерживается только gmail(!)")
    info_label.grid(row=1,column=1,columnspan=2)
    user_label=tkinter.Label(new_window,text="Укажите свою почту")
    user_var = tkinter.StringVar()
    user_var.set("example@gmail.com")
    user_entry=tkinter.Entry(new_window,textvariable=user_var)
    user_label.grid(row=2,column=1)
    user_entry.grid(row=2,column=2)
    password_label=tkinter.Label(new_window,text="Введите пароль")
    password_var = tkinter.StringVar()
    password_var.set("example")
    password_entry=tkinter.Entry(new_window,textvariable=password_var,show="*")
    password_label.grid(row=3,column=1)
    password_entry.grid(row=3,column=2)
    password_intvar = tkinter.IntVar()
    password_checkbutton=tkinter.Checkbutton(new_window,text="Показать пароль",variable=password_intvar,command=show_password)
    password_checkbutton.grid(row=4,column=2)
    message_label=tkinter.Label(new_window,text="Сообщение")
    message_text=tkinter.Text(new_window,width=22,height=15)
    message_text.insert(1.0,"Hello world!")
    message_label.grid(row=5,column=1)
    message_text.grid(row=5,column=2)
    send_button=tkinter.Button(new_window,text="Send",command=send_email)
    quit_button=tkinter.Button(new_window,text="Quit",command=new_window.destroy)
    send_button.grid(row=6,column=1)
    quit_button.grid(row=6,column=2)
    return None

# Magic_table #
test_url_const = "https://raw.githubusercontent.com/runnerpeople/Summer_work/master/T-bmstu/tests.txt"

wnd = tkinter.Tk()
wnd.geometry("625x350")
wnd.title("T-bmstu tester")
wnd.resizable(width=tkinter.FALSE, height=tkinter.FALSE)
frame1=tkinter.Frame(wnd)
frame1.pack(fill="both",expand="Yes")
language_list=[("C",0),("C++",1),("Java",2),("Python",3),("Scheme",4),("Ruby",5),("Pascal",6)]

# Boolean Flag
args_flag = False
file_flag = False
compile_flag = False


# String, int, double vars and Initialize #
t_bmstu_ip=tkinter.StringVar()
t_bmstu_ip.set("http://195.19.40.181:3386")
file_path=tkinter.StringVar()
file_path.set(str(os.getcwd()))
test_url=tkinter.StringVar()
language_string = tkinter.StringVar()
language_string.set("gcc " + str(os.getcwd()) + " ")
language_choose=tkinter.IntVar()
timeout_ = tkinter.DoubleVar()
checking = tkinter.StringVar()

# Menu #

menubar = tkinter.Menu(frame1,relief=tkinter.FLAT)
filemenu = tkinter.Menu(menubar,tearoff=0)
filemenu.add_command(label="Open...", command=choose_directory)
filemenu.add_separator()
filemenu.add_command(label="Compile", command=compile_program)
filemenu.add_command(label="Test", command=test_program)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=wnd.quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = tkinter.Menu(menubar, tearoff=0)
editmenu.add_command(label="T-bmstu", command=t_bmstu_window)
editmenu.add_command(label="Test_url", command=test_url_window)
editmenu.add_separator()
editmenu.add_command(label="Bash_compile", command=compile_string_window)
editmenu.add_command(label="Choose_language", command=language_choose_window)
editmenu.add_separator()
editmenu.add_command(label="Timeout", command=timeout_window)
editmenu.add_command(label="Checking strategy", command=checking_window)
menubar.add_cascade(label="Edit", menu=editmenu)
offlinemenu = tkinter.Menu(menubar, tearoff=0)
offlinemenu.add_command(label="Tasks", command=tasks_window)
menubar.add_cascade(label="Offline", menu=offlinemenu)
helpmenu = tkinter.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=help_window)
helpmenu.add_command(label="Contact us", command=contact_window)
helpmenu.add_command(label="Version", command=version_window)
helpmenu.add_command(label="About...", command=about_window)
menubar.add_cascade(label="Help", menu=helpmenu)


# Labels #
info_label=tkinter.Label(frame1,text="Автоматический тестер решения задач в системе тестирования T-bmstu")
t_bmstu_label=tkinter.Label(frame1,text="Сайт t-bmstu(изменен с 2015 г.):",width=30)
language_label=tkinter.Label(frame1,text="Выберите один из языков программирования")
file_label=tkinter.Label(frame1,text="Укажите путь к файлу")
test_url_label=tkinter.Label(frame1,text="Введите ссылку на тесты\n (если возникнет неизвестная ошибка)")
compile_label = tkinter.Label(frame1,text="Строка компиляции для bash")
timeout_label = tkinter.Label(frame1,text="Укажите предел по времени")
timeout_label2 = tkinter.Label(frame1,text="ограничение -- 1 с")
checking_label = tkinter.Label(frame1,text="Укажите способ проверки")
checking_label2 = tkinter.Label(frame1,text="Вы выбрали\nспособ проверки\nSCAN")
author_name=tkinter.Label(frame1,text="by George Great")

# Entries #
t_bmstu_entry=tkinter.Entry(frame1,width=40,textvariable=t_bmstu_ip)
file_entry=tkinter.Entry(frame1,width=40,textvariable=file_path)
compile_string = tkinter.Entry(frame1,width=40,textvariable=language_string)
test_url_entry=tkinter.Entry(frame1,textvariable=test_url,width=40)

# Buttons #

compile_button=tkinter.Button(frame1,text="Compile")
file_button=tkinter.Button(frame1,text="Выбери директорию",command=choose_directory)
compile_button.bind("<Button-1>",lambda event:compile_program())
test_button=tkinter.Button(frame1,text="Test!")
test_button.bind("<Button-1>",lambda event:test_program())
buttons=create_choose_language(frame1,language_list,language_choose)

# ListBox #

checking_listbox = tkinter.Listbox(frame1,height=5,selectmode=tkinter.SINGLE)
checking_listbox.insert(tkinter.END, "SCAN")
checking_listbox.insert(tkinter.END, "BINARY")
checking_listbox.insert(tkinter.END, "TEXT")
checking_listbox.insert(tkinter.END, "INTEGER")
checking_listbox.insert(tkinter.END, "FLOAT")
checking_listbox.bind('<<ListboxSelect>>',lambda event:checking_change())

# Scale #

timeout_scale = tkinter.Scale(frame1,variable=timeout_,from_=1,to=20,orient=tkinter.HORIZONTAL,showvalue=0,command=lambda event:timeout_change())

# Packing #
wnd.config(menu=menubar)
info_label.grid(row=1,column=1,columnspan=4)
t_bmstu_label.grid(row=2,column=1)
t_bmstu_entry.grid(row=2,column=2,columnspan=3)
file_label.grid(row=3,column=1)
file_entry.grid(row=3,column=2,columnspan=3)
file_button.grid(row=4,column=2,columnspan=3)
language_label.grid(row=5,column=1)
column_number = 2
flag=False
for button in buttons:
    if column_number == 5:
        row = 6
        column_number=1
        flag=True
    elif flag == False:
        row = 5
    button.grid(row=row,column=column_number)
    column_number+=1
test_url_label.grid(row=7,column=1)
test_url_entry.grid(row=7,column=2,columnspan=3)
compile_label.grid(row=8,column=1)
compile_string.grid(row=8,column=2,columnspan=3)
timeout_label.grid(row=9,column=1)
timeout_scale.grid(row=9,column=2)
timeout_label2.grid(row=9,column=3,columnspan=2)
checking_label.grid(row=10,column=1)
checking_listbox.grid(row=10,column=2,columnspan=2)
checking_label2.grid(row=10,column=4)
test_button.grid(row=11,column=2)
compile_button.grid(row=11,column=3)
author_name.grid(row=12,column=1,columnspan=4)

wnd.mainloop()
