#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import tkinter
from tkinter import messagebox
import tkinter.font
import tkinter.filedialog

def test_program(event):
    print("1")

def compile_program(event):
    print("2")

def choose_directory():
    directory_path = tkinter.filedialog.askopenfilename()
    file_path.set(directory_path)
    return None

def create_choose_language(list,v):
    buttons=[]
    for text,value in list:
        buttons.append(tkinter.Radiobutton(frame1,text=text,value=value,variable=v))
    return buttons

wnd = tkinter.Tk()
wnd.geometry("600x225")
wnd.title("T-bmstu tester")
t_bmstu_ip=tkinter.StringVar()
t_bmstu_ip.set("http://195.19.40.181:3386")
file_path=tkinter.StringVar()
file_path.set(str(os.getcwd()))
frame1=tkinter.Frame(wnd)
frame1.pack(fill="both",expand="Yes")
test_url=tkinter.StringVar()
info_label=tkinter.Label(frame1,text="Автоматический тестер решения задач в системе тестирования T-bmstu")
t_bmstu_label=tkinter.Label(frame1,text="Сайт t-bmstu(изменен с 2015 г.):",width=30)
t_bmstu_entry=tkinter.Entry(frame1,width=40,textvariable=t_bmstu_ip)
file_label=tkinter.Label(frame1,text="Укажите путь к файлу")
file_entry=tkinter.Entry(frame1,width=40,textvariable=file_path)
file_button=tkinter.Button(frame1,text="Выбери директорию",command=choose_directory)
language_label=tkinter.Label(frame1,text="Выберите один из языков программирования")
language_list=[("C",0),("C++",1),("Java",2),("Python",3),("Scheme",4),("Ruby",5),("Pascal",6)]
test_url_label=tkinter.Label(frame1,text="Введите ссылку на тесты\n (если возникнет неизвестная ошибка)")
compile_button=tkinter.Button(frame1,text="Compile")
compile_button.bind("<Button-1>",compile_program)
test_button=tkinter.Button(frame1,text="Test!")
test_button.bind("<Button-1>",test_program)
test_url_entry=tkinter.Entry(frame1,textvariable=test_url,width=40)
author_name=tkinter.Label(frame1,text="by George Great")
language_choose=tkinter.IntVar()
buttons = create_choose_language(language_list,language_choose)
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
test_button.grid(row=8,column=2)
compile_button.grid(row=8,column=3)
author_name.grid(row=9,column=1,columnspan=4)
wnd.mainloop()
