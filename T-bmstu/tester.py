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

def compare_files(answer,output):
    command="diff -wbq " + answer + " " + output
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

def test_program(event):
    global test_url
    global args_flag
    global file_flag
    if test_url.get()!="":
        magic_url=test_url.get()
    else:
        try:
            magic_url = urllib.request.urlopen(test_url_const).readline().decode()
            magic_lines = urllib.request.urlopen(test_url_const).read().decode().splitlines()
            magic_url=magic_url.replace("T-BMSTU",t_bmstu_ip.get())
            program=file_path.get()[file_path.get().rfind("/")+1:]
            program=program[:program.find(".")]
            test_string=""
            for s in filter (lambda x: program in x, magic_lines):
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
            else:
                test_url1 = magic_url + str(test_number)
                answer_url = test_url1 + ".a"
            test = urllib.request.urlopen(test_url1).read().decode()
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
        else:
            test_file = open("test.c", "w")
        answer_file = open("answer.txt","w")
        test_file.write(test)
        answer_file.write(answer)
        test_file.close()
        answer_file.close()
        if language_choose.get()==0 and file_flag == True:
            if elem_h:
                command = language_string.get() + "test.c elem.h && valgrind -q ./a.out"
            else:
                command = language_string.get() + "test.c && valgrind -q ./a.out"
        elif language_choose.get()==0 and args_flag == True:
            command = "valgrind -q ./a.out " + test
        elif language_choose.get()==0 or language_choose.get()==1:
            command = "valgrind -q ./a.out <test.txt"
        elif language_choose.get()==2:
            os.system("cd " + os.getcwd())
            command = "java -cp " + os.getcwd() + " " + file_path.get()[file_path.get().rfind("/")+1:file_path.get().rfind(".")] + " " + "<test.txt"
        elif language_choose.get()==3 or language_choose.get()==4 or language_choose.get()==5:
            command = language_string.get()
        elif language_choose.get()==6:
            messagebox.showinfo("Test","Временно возникли проблемы")
            break
        # time_limit
        try:
            process_ = subprocess.call(command,timeout=10,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        except subprocess.TimeoutExpired:
            messagebox.showerror("Test", "Превышен лимит по времени:\nограничение -- 10 с\n в тесте №" + str(test_number))
            break
        process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        output, error = process.communicate()
        output = output.decode()
        error = error.decode()
        if error != "" and language_choose.get()==0 or language_choose.get()==1:
            messagebox.showerror("Test", "valgrind показывает ошибки в тесте " + str(test_number))
            print(error)
            break
        elif error != "":
            messagebox.showerror("Test", "Неизвестная ошибка в тесте " + str(test_number))
            print(error)
            break
        output_file = open("output.txt", "w")
        output_file.write(output)
        output_file.close()
        if compare_files("answer.txt","output.txt") == False:
            messagebox.showerror("Test", "Неправильный ответ для теста № " + str(test_number))
            error_and_right("answer.txt","output.txt")
            break
        test_number +=1

def compile_program(event):
    global file_flag
    global args_flag
    magic_lines = urllib.request.urlopen(test_url_const).read().decode().splitlines()
    program=file_path.get()[file_path.get().rfind("/")+1:]
    program=program[:program.find(".")]
    test_string=""
    for s in filter (lambda x: program in x, magic_lines):
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
    else:
        messagebox.showerror("Compile", "Компиляция не была проведена. Возникла ошибка")
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

def create_choose_language(list,v):
   buttons=[]
   for text,value in list:
       new_button = tkinter.Radiobutton(frame1,text=text,value=value,variable=v,command=compile_string_2)
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
        language_string.set("guile-1.8 -l" + str(file_path.get()) + " ")
        # have some problem #
    elif language_choose.get()==5:
        language_string.set("ruby " + str(file_path.get()) + " ")
    elif language_choose.get()==6:
        messagebox.showinfo("Choose language", "Временно недоступно")



# Example #
test_url_const = "https://raw.githubusercontent.com/runnerpeople/Summer_work/master/T-bmstu/tests.txt"

wnd = tkinter.Tk()
wnd.geometry("625x250")
wnd.title("T-bmstu tester")
frame1=tkinter.Frame(wnd)
frame1.pack(fill="both",expand="Yes")
language_list=[("C",0),("C++",1),("Java",2),("Python",3),("Scheme",4),("Ruby",5),("Pascal",6)]

# Boolean Flag
args_flag = False
file_flag = False


# String, int vars and Initialize #
t_bmstu_ip=tkinter.StringVar()
t_bmstu_ip.set("http://195.19.40.181:3386")
file_path=tkinter.StringVar()
file_path.set(str(os.getcwd()))
test_url=tkinter.StringVar()
language_string = tkinter.StringVar()
language_string.set("gcc " + str(os.getcwd()) + " ")
language_choose=tkinter.IntVar()

# Labels #
info_label=tkinter.Label(frame1,text="Автоматический тестер решения задач в системе тестирования T-bmstu")
t_bmstu_label=tkinter.Label(frame1,text="Сайт t-bmstu(изменен с 2015 г.):",width=30)
language_label=tkinter.Label(frame1,text="Выберите один из языков программирования")
file_label=tkinter.Label(frame1,text="Укажите путь к файлу")
test_url_label=tkinter.Label(frame1,text="Введите ссылку на тесты\n (если возникнет неизвестная ошибка)")
compile_label = tkinter.Label(frame1,text="Строка компиляции для bash")
author_name=tkinter.Label(frame1,text="by George Great")

# Entries #
t_bmstu_entry=tkinter.Entry(frame1,width=40,textvariable=t_bmstu_ip)
file_entry=tkinter.Entry(frame1,width=40,textvariable=file_path)
compile_string = tkinter.Entry(frame1,width=40,textvariable=language_string)
test_url_entry=tkinter.Entry(frame1,textvariable=test_url,width=40)

# Buttons #

compile_button=tkinter.Button(frame1,text="Compile")
file_button=tkinter.Button(frame1,text="Выбери директорию",command=choose_directory)
compile_button.bind("<Button-1>",compile_program)
test_button=tkinter.Button(frame1,text="Test!")
test_button.bind("<Button-1>",test_program)
buttons=create_choose_language(language_list,language_choose)


# Packing #
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
test_button.grid(row=9,column=2)
compile_button.grid(row=9,column=3)
author_name.grid(row=10,column=1,columnspan=4)

wnd.mainloop()
