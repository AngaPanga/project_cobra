# -- coding: utf-8 --
import csv
import os
from math import log2
from tkinter import Tk, Menu, Button, Spinbox, CENTER, IntVar, END, VERTICAL, RIGHT, Y, BOTH, E, W, LEFT, X, Toplevel, \
    NORMAL, DISABLED, Text, HORIZONTAL, TOP, StringVar
# from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, askyesno
from tkinter.ttk import Combobox, Treeview, Frame, Notebook, Style, Label, Entry, Scrollbar

from data.manual import manual_dict
from models.Player import Player
from models.championsihp.circcmpship import CircChampionShip
from models.championsihp.swests_system import SwedenChampionship
from models.save_load_file_csp import save_championship, load_championship, load_backup, save_backup


class General:
    COLUMNS = {'name': ("Имя", 130),
               'surname': ("Фамилия", 130),
               'second_name': ("Отчество", 130),
               'date': ("Дата рождения", 110),
               'club': ("Клуб", 120),
               'city': ("Город", 120),
               'level': ("Разряд", 60),
               'rate': ("Рейтинг", 70)
               }
    HISTORY_COLUMNS = {'number_meeting': ("№", 40),
                       'name_1': ("Игрок 1", 200),
                       'empty': (" ", 5),
                       'name_2': ("Игрок 2", 200),
                       'score': ("Баллы", 60),
                       'points': ("Счет", 90),
                       }
    COLUMNS_RESULT = {'num_place': ("Место", 30),
                      'num_player': ("№ уч-ка", 70),
                      'fullname': ("ФИО", 300),
                      'score': ("Баллы", 65),
                      'buh': ("Коэф-т", 65),
                      'full_score': ("Очки", 60),
                      'rate': ("Рейтинг", 75)
                      }

    def __init__(self):
        self.frame = None
        self.data = {}
        self.championship = None
        self.save_status = True
        self.window = Tk()
        self.window.title('Программа жеребъевки')
        self.start_window()
        self.window.protocol("WM_DELETE_WINDOW", self.exit_gen_window)
        self.window.mainloop()

    @staticmethod
    def _error_input():
        showerror(title="Ошибка", message="Заполните обязательные поля")

    @staticmethod
    def _error_length(position):
        showerror(title="Ошибка", message=f'Недопустимое число символов в {position}')

    def exit_gen_window(self):
        if self.save_status:
            self.window.destroy()
        else:
            if askyesno(title="Выход", message="Выйти из программы без сохранения?"):
                self.window.destroy()

    def start_window(self):
        def load_backup_championship():
            self.championship = load_backup()
            self.base_window()

        main_menu = Menu()
        self.window.config(menu=main_menu)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = Frame(self.window)
        create_championship = Button(self.frame, font="Courier 24 bold", text="создать турнир",
                                     command=self.information_championship)
        create_championship.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        download_championship = Button(self.frame, text="загрузить турнир", font="Courier 24 bold",
                                       command=self.load_command)
        download_championship.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        recover_championship = Button(self.frame, text="восстановить турнир", font="Courier 24 bold",
                                      command=load_backup_championship)
        recover_championship.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        calculate_rate = Button(self.frame, text="рассчитать рейтинг", font="Courier 24 bold", )
        calculate_rate.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        finish = Button(self.frame, text="завершить", font="Courier 24 bold", command=self.window.destroy)
        finish.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        self.frame.pack(anchor=CENTER, expand=1)

    def information_championship(self):
        def input_data():
            if name_entry.get() == '' or \
                    organization_entry.get() == '' or \
                    discipline_entry.get() == '' or \
                    judge_entry.get() == '' or \
                    secretary_entry.get() == '':
                self._error_input()
            elif len(name_entry.get()) > 80:
                self._error_length('Название турнира')
            elif len(organization_entry.get()) > 50:
                self._error_length('Организация')
            elif len(discipline_entry.get()) > 30:
                self._error_length('Дисциплина')
            elif len(place_entry.get()) > 50:
                self._error_length('Место проведения')
            elif len(judge_entry.get()) > 50:
                self._error_length('Главный судья')
            elif len(secretary_entry.get()) > 50:
                self._error_length('Секретарь')
            elif len(start_date_entry.get()) > 20 or len(end_date_entry.get()) > 20:
                self._error_length('Дата')
            else:
                self.data['name_championship'] = name_entry.get()
                self.data['organization'] = organization_entry.get()
                self.data['start_date'] = start_date_entry.get()
                self.data['end_date'] = end_date_entry.get()
                self.data['discipline'] = discipline_entry.get()
                self.data['place_championship'] = place_entry.get()
                self.data['judge'] = judge_entry.get()
                self.data['secretary'] = secretary_entry.get()
                self.parameters_championship()

        self.frame.destroy()
        self.frame = Frame(self.window)
        self.window.title('Информация о турнире')
        title = Label(self.frame, text="Предварительная информация о турнире", font="Courier 18 bold", )
        title.grid(row=0, column=0, sticky="nsew", columnspan=4, padx=2, pady=2)
        # Название турнира
        name_csp = Label(self.frame, text="* Название турнира:", font="Courier 16 bold", anchor="e")
        name_csp.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        name_entry = Entry(self.frame, font="Courier 16 bold")
        name_entry.grid(row=1, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        # Организация
        organization = Label(self.frame, text="* Организация:", font="Courier 16 bold", anchor="e")
        organization.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        organization_entry = Entry(self.frame, font="Courier 16 bold")
        organization_entry.grid(row=2, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        # Даты
        start_date = Label(self.frame, text="Дата начала:", font="Courier 16 bold", anchor="e")
        start_date.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        start_date_entry = Entry(self.frame, width=16, font="Courier 16 bold")
        start_date_entry.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
        end_date = Label(self.frame, text="Дата окончания:", font="Courier 16 bold", anchor="e")
        end_date.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
        end_date_entry = Entry(self.frame, width=16, font="Courier 16 bold")
        end_date_entry.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)
        # дисциплина
        discipline = Label(self.frame, text="* Дисциплина:", font="Courier 16 bold", anchor="e")
        discipline.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        discipline_entry = Entry(self.frame, font="Courier 16 bold")
        discipline_entry.grid(row=4, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        # Место проведения
        place = Label(self.frame, text="Место проведения:", font="Courier 16 bold", anchor="e")
        place.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
        place_entry = Entry(self.frame, font="Courier 16 bold")
        place_entry.grid(row=5, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        # Главный судья
        judge = Label(self.frame, text="* Главный судья:", font="Courier 16 bold", anchor="e")
        judge.grid(row=6, column=0, sticky="nsew", padx=2, pady=2)
        judge_entry = Entry(self.frame, font="Courier 16 bold")
        judge_entry.grid(row=6, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        # Секретарь
        secretary = Label(self.frame, text="* Секретарь:", font="Courier 16 bold", anchor="e")
        secretary.grid(row=7, column=0, sticky="nsew", padx=2, pady=2)
        secretary_entry = Entry(self.frame, font="Courier 16 bold")
        secretary_entry.grid(row=7, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        # Назад/Далее
        back_button = Button(self.frame, text="Назад", font="Courier 16 bold", command=self.start_window)
        back_button.grid(row=8, column=0, sticky="nsew", columnspan=2, padx=2, pady=2)
        next_button = Button(self.frame, text="Далее", font="Courier 16 bold", command=input_data)
        next_button.grid(row=8, column=2, sticky="nsew", columnspan=2, padx=2, pady=2)
        self.frame.pack(anchor=CENTER, expand=1)

    def parameters_championship(self):
        def hand_input():
            if not count_players.get().isdigit() or category_box.get() == '':
                self._error_input()
            else:
                self.data['count_player'] = int(count_players.get())
                self.data['category'] = category_box.get()
                self.players_input()

        def download_input():
            if category_box.get() == '':
                self._error_input()
            else:
                self.data['category'] = category_box.get()
                self.download_file_players()

        def selected(event):
            selection = input_change.get()
            if selection == "Ввод списка участников":
                next_button.config(command=hand_input)
                count_label.grid(row=6, column=0, sticky="we", columnspan=3, padx=2, pady=4)
                count_players.grid(row=6, column=3, sticky="e", padx=2, pady=4)
            else:
                next_button.config(command=download_input)
                count_label.grid_forget()
                count_players.grid_forget()
            next_button.grid(row=7, column=2, sticky="nsew", columnspan=2, padx=2, pady=4)

        self.frame.destroy()
        self.window.title('Параметры')
        self.frame = Frame(self.window)
        parameters_label = Label(self.frame, text="Параметры турнира", font="Courier 16 bold")
        parameters_label.grid(row=0, column=0, sticky="nsew", columnspan=4, padx=2, pady=4)
        # Количество участников
        count_label = Label(self.frame, text="Количество участников:", font="Courier 16 bold", anchor="e")
        count_players = Spinbox(self.frame, font="Courier 16 bold", from_=3, to=200, width=4)
        # Уровень турнира
        category = Label(self.frame, text="Уровень турнира:", font="Courier 16 bold")
        category.grid(row=2, column=0, sticky="w", columnspan=2, padx=2, pady=4)
        category_list = ["Местный уровень", "Городской уровень", "Региональный уровень",
                         "Окружной уровень", "Федеральный уровень"]
        category_box = Combobox(self.frame, font="Courier 16 bold", values=category_list, state="readonly")
        category_box.grid(row=3, column=0, sticky="ew", columnspan=4, padx=2, pady=4)
        # Ручной ввод/Загрузить
        input_label = Label(self.frame, text="Выберите способ ввода участников:", font="Courier 16 bold")
        input_label.grid(row=4, column=0, sticky="w", columnspan=4, padx=2, pady=4)
        change_list = ["Ввод списка участников", "Загрузить список участников из файла"]
        input_change = Combobox(self.frame, font="Courier 16 bold", values=change_list, state="readonly")
        input_change.grid(row=5, column=0, sticky="ew", columnspan=4, padx=2, pady=4)
        input_change.bind("<<ComboboxSelected>>", selected)
        # Назад/Далее
        back_button = Button(self.frame, text="Назад", font="Courier 16 bold", command=self.information_championship)
        back_button.grid(row=7, column=0, sticky="nsew", columnspan=2, padx=2, pady=4)
        next_button = Button(self.frame, text="Далее", font="Courier 16 bold")
        self.frame.pack(anchor=CENTER, expand=1)

    def players_input(self):
        number_player = IntVar()
        number_player.set(1)
        list_players = []

        def read_data_player():
            if number_player.get() <= self.data['count_player']:
                temp_dict = {}
                if name_entry.get() == '' or surname_entry.get() == '' or second_name_entry.get() == '':
                    self._error_input()
                else:
                    temp_dict['name'] = name_entry.get()
                    name_entry.delete(0, END)
                    temp_dict['sirname'] = surname_entry.get()
                    surname_entry.delete(0, END)
                    temp_dict['second_name'] = second_name_entry.get()
                    second_name_entry.delete(0, END)
                    if date_entry.get() != '':
                        temp_dict['date'] = date_entry.get()
                        date_entry.delete(0, END)
                    if club_entry.get() != '':
                        temp_dict['club'] = club_entry.get()
                        club_entry.delete(0, END)
                    if city_entry.get() != '':
                        temp_dict['city'] = city_entry.get()
                        city_entry.delete(0, END)
                    if level_entry.get() != '' and level_entry.get().isdigit():
                        if 0 < int(level_entry.get()) < 5:
                            temp_dict['level'] = int(level_entry.get())
                            level_entry.delete(0, END)
                    if rate_entry.get() != '' and rate_entry.get().isdigit():
                        if 900 < int(rate_entry.get()) < 5000:
                            temp_dict['rate'] = int(rate_entry.get())
                            rate_entry.delete(0, END)
                    list_players.append(Player(**temp_dict))
                    number_player.set(number_player.get() + 1)
                    table.insert("", END, values=list_players[-1].player_tuple())
                    if number_player.get() > self.data['count_player']:
                        next_button.grid(row=9, column=2, sticky="nsew", columnspan=2, padx=2, pady=2)
                        add_player.destroy()
                        profile_label.destroy()
                        self.data['list_players'] = list_players
                    else:
                        profile_label.config(text=f"Анкета участника № {number_player.get()}")

        self.frame.destroy()
        self.window.title('Ввод данных участников')
        self.frame = Frame(self.window)
        frame_1 = Frame(self.frame)
        frame_2 = Frame(self.frame, padding=[5, 10, 5, 0])
        # 1-й фрейм заполнения данных
        profile_label = Label(frame_1, text=f"Анкета участника № {number_player.get()}", font="Courier 12 bold")
        profile_label.grid(row=0, column=0, sticky="nsew", columnspan=4, padx=2, pady=2)
        name = Label(frame_1, text="* Имя:", anchor="e", font="Courier 12 bold")
        name.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        name_entry = Entry(frame_1, font="Courier 12 bold")
        name_entry.grid(row=1, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        surname = Label(frame_1, text="* Фамилия:", anchor="e", font="Courier 12 bold")
        surname.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        surname_entry = Entry(frame_1, font="Courier 12 bold")
        surname_entry.grid(row=2, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        second_name = Label(frame_1, text="* Отчество:", anchor="e", font="Courier 12 bold")
        second_name.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        second_name_entry = Entry(frame_1, font="Courier 12 bold")
        second_name_entry.grid(row=3, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        date = Label(frame_1, text="Дата рождения:", anchor="e", font="Courier 12 bold")
        date.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        date_entry = Entry(frame_1, font="Courier 12 bold")
        date_entry.grid(row=4, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        club = Label(frame_1, text="Клуб:", anchor="e", font="Courier 12 bold")
        club.grid(row=5, column=0, sticky="nsew", padx=2, pady=2)
        club_entry = Entry(frame_1, font="Courier 12 bold")
        club_entry.grid(row=5, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        city = Label(frame_1, text="Город:", anchor="e", font="Courier 12 bold")
        city.grid(row=6, column=0, sticky="nsew", padx=2, pady=2)
        city_entry = Entry(frame_1, font="Courier 12 bold")
        city_entry.grid(row=6, column=1, sticky="nsew", columnspan=3, padx=2, pady=2)
        level = Label(frame_1, text="Разряд:", anchor="e", font="Courier 12 bold")
        level.grid(row=7, column=0, sticky="nsew", padx=2, pady=2)
        level_entry = Entry(frame_1, width=3, font="Courier 12 bold")
        level_entry.grid(row=7, column=1, sticky="nsew", padx=2, pady=2)
        rate = Label(frame_1, text="Рейтинг:", anchor="e", font="Courier 12 bold")
        rate.grid(row=7, column=2, sticky="nsew", padx=2, pady=2)
        rate_entry = Entry(frame_1, width=5, font="Courier 12 bold")
        rate_entry.grid(row=7, column=3, sticky="nsew", padx=2, pady=2)
        # Добавить участника
        add_player = Button(frame_1, text="Добавить участника", font="Courier 12 bold", command=read_data_player)
        add_player.grid(row=8, column=0, sticky="nsew", columnspan=4, padx=2, pady=2)
        # Назад/Далее
        back_button = Button(frame_1, text="Назад", font="Courier 12 bold", command=self.parameters_championship)
        back_button.grid(row=9, column=0, sticky="nsew", columnspan=2, padx=2, pady=2)
        next_button = Button(frame_1, text="Далее", font="Courier 12 bold", command=self.championship_system)

        # упаковка фрейма слева
        frame_1.pack(side='left')
        # Полоса прокрутки
        scrollbar = Scrollbar(frame_2, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        # определяем столбцы
        table = Treeview(frame_2, columns=tuple(self.COLUMNS.keys()), show="headings")
        style = Style()
        style.configure("Treeview", font=(None, 11))
        style.configure("Treeview.Heading", font=(None, 11))
        table.pack(fill=BOTH, expand=1)
        table.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=table.yview)

        # настраиваем ширину столбца
        # определяем заголовки
        # добавляем данные
        for key, value in self.COLUMNS.items():
            table.heading(key, text=value[0])
            table.column(key, width=value[1], stretch=True)

        # упаковка фрейма справа
        frame_2.pack(side='right', fill=BOTH, expand=1)
        # упаковка общего фрейма
        self.frame.pack(anchor=CENTER, expand=1, fill=BOTH)

    def download_file_players(self):
        file_name = StringVar()
        file_name.set('')

        def check():
            file_name.set(askopenfilename())
            if file_name.get() != '':
                lbl.grid(row=2, column=0, columnspan=2, padx=2, pady=2)
                lbl.config(text=os.path.basename(file_name.get()))

        def download_list_players():
            list_players = []
            with open(file_name.get(), "r", newline="", encoding="utf8") as file:
                reader = csv.reader(file)
                for row in reader:
                    row.pop(-1)
                    table.insert("", END, values=row)
                    list_players.append(Player.create_player(row))
            self.data['list_players'] = list_players
            self.data['count_player'] = len(list_players)
            next_button.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)

        self.frame.destroy()
        self.frame = Frame(self.window)
        self.window.title('Загрузка списка участников')
        frame_1 = Frame(self.frame)
        frame_2 = Frame(self.frame, padding=[5, 10, 5, 0])
        title = Label(frame_1, text="Загрузка списка участников:", font="Courier 12 bold")
        title.grid(row=0, column=0, sticky="nsew", columnspan=2, padx=2, pady=2)
        check_file = Button(frame_1, text="Выбрать файл", font="Courier 12 bold", command=check)
        check_file.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=2, pady=2)
        lbl = Label(frame_1, font="Courier 12 bold")
        download_button = Button(frame_1, text="Загрузить", font="Courier 12 bold", command=download_list_players)
        download_button.grid(row=3, column=0, sticky="nsew", columnspan=2, padx=2, pady=2)
        back_button = Button(frame_1, text="Назад", font="Courier 12 bold", command=self.parameters_championship)
        back_button.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        next_button = Button(frame_1, text="Далее", font="Courier 12 bold",
                             command=self.championship_system)
        # Полоса прокрутки
        scrollbar = Scrollbar(frame_2, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        # определяем столбцы
        table = Treeview(frame_2, columns=tuple(self.COLUMNS.keys()), show="headings")
        style = Style()
        style.configure("Treeview", font=(None, 11))
        style.configure("Treeview.Heading", font=(None, 11))
        table.pack(fill=BOTH, expand=1)
        table.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=table.yview)
        # настраиваем ширину столбца
        # определяем заголовки
        for key, value in self.COLUMNS.items():
            table.heading(key, text=value[0])
            table.column(key, width=value[1], stretch=True)
        frame_1.pack(side='left')
        frame_2.pack(side='right', fill=BOTH, expand=1)
        self.frame.pack(anchor=CENTER, expand=1, fill=BOTH)

    def championship_system(self):
        def next_step():
            if system_box.get() == "Швейцарская система":
                self.data['max_tour'] = int(tour_entry.get())
            self.data['system_championship'] = system_box.get()
            self._create_championship()

        def selected(event):
            selection = system_box.get()
            if selection == "Швейцарская система":
                tour.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
                tour_entry.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
            else:
                tour.grid_remove()
                tour_entry.grid_remove()
            next_button.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)

        self.frame.destroy()
        self.window.title("Настройки турнира")
        self.frame = Frame(self.window)
        title = Label(self.frame, text="Выберите систему проведения турнира:", font="Courier 12 bold")
        title.grid(row=0, column=0, sticky="nsew", columnspan=2, padx=2, pady=2)
        # выбор системы
        system_championship = ["Круговая система", "Швейцарская система"]
        system_box = Combobox(self.frame, font="Courier 12 bold", values=system_championship, state="readonly")
        system_box.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=2, pady=2)
        system_box.bind("<<ComboboxSelected>>", selected)
        tour = Label(self.frame, text="Количество туров:", font="Courier 12 bold", anchor="e")
        start_num = log2(self.data['count_player']) // 1 + 1
        tour_entry = Spinbox(self.frame, from_=start_num, to=start_num * 2, width=3)
        next_button = Button(self.frame, text="Далее", font="Courier 12 bold", command=next_step)
        back_button = Button(self.frame, text="Назад", font="Courier 12 bold", command=self.parameters_championship)
        back_button.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        self.frame.pack(anchor=CENTER, expand=1)

    def _create_championship(self):
        if self.data['system_championship'] == "Круговая система":
            self.championship = CircChampionShip.create_circle_championship(self.data.copy())
        if self.data['system_championship'] == "Швейцарская система":
            self.championship = SwedenChampionship.create_sweden_championship(self.data.copy())
        self.championship.create_tour()
        self.championship.coefficient()
        save_backup(self.championship)
        self.save_status = False
        self.base_window()

    def base_window(self):
        def load_start_menu():
            if self.save_status:
                self.start_window()
            else:
                if askyesno(title="Переход", message="Выйти в главное меню без сохранения?"):
                    self.start_window()

        def download_championship():
            if self.save_status:
                self.load_command()
            else:
                if askyesno(title="Переход", message="Выйти в главное меню без сохранения?"):
                    self.load_command()

        main_menu = Menu()
        main_menu.option_add("*tearOff", False)  # FALSE
        # подменю для Файл
        file_menu = Menu()
        file_menu.add_command(label="Сохранить турнир", font="Courier 12 bold", command=self.save_command)
        file_menu.add_command(label="Загрузить турнир", font="Courier 12 bold", command=download_championship)
        file_menu.add_command(label="Главное меню", font="Courier 12 bold", command=load_start_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", font="Courier 12 bold", command=self.exit_gen_window)
        # подменю для Правка
        edit_menu = Menu()
        edit_menu.add_command(label="Редактировать данные о турнире", font="Courier 12 bold")
        edit_menu.add_command(label="Изменить участника", font="Courier 12 bold")
        edit_menu.add_command(label="Редактировать результаты встречи", font="Courier 12 bold")

        info_menu = Menu()
        info_menu.add_command(label="Инструкция", font="Courier 12 bold", command=General.instruction)

        # набор эелементов верхней панели
        main_menu.add_cascade(label="Файл", font="Courier 12 bold", menu=file_menu)
        main_menu.add_cascade(label="Правка", font="Courier 12 bold", menu=edit_menu)
        main_menu.add_cascade(label="Сервис", font="Courier 12 bold")
        main_menu.add_cascade(label="Информация", font="Courier 12 bold", menu=info_menu)
        # построить меню
        self.window.config(menu=main_menu)

        if self.frame is not None:
            self.frame.destroy()
        self.frame = Frame(self.window)
        # создаем набор вкладок
        notebook = Notebook(self.frame)
        notebook.pack(expand=True, fill=BOTH)
        # создаем фреймы
        frame1 = Frame(notebook)
        frame2 = Frame(notebook)
        frame3 = Frame(notebook)
        frame1.pack(side=TOP, fill=X, expand=True)
        frame2.pack(expand=True)
        frame3.pack(expand=True)

        self.notebook_one(frame1)
        self.notebook_two(frame2)
        self.notebook_three(frame3)

        notebook.add(frame1, text="Информация о турнире")
        notebook.add(frame2, text="Список пар")
        notebook.add(frame3, text="Итоговый список участников")
        self.frame.pack(fill=BOTH, expand=1)

    def notebook_one(self, frame1):
        name_csp = Label(frame1, text=f'«{self.championship.name_championship}»', font="Courier 30 bold")
        name_csp.config(anchor='c', wraplength=700)
        if self.championship.finish:
            count_tour = Label(frame1, text='🏆', font="Courier 100 bold")
        else:
            count_tour = Label(frame1, text=self.championship.tour, font="Courier 100 bold")
        tour_lbl = Label(frame1, text=" ТУР ", font="Courier 50 bold")
        organization = Label(frame1, text=self.championship.organization, font="Courier 28 bold")
        disc_lbl = Label(frame1, text=self.championship.discipline, font="Courier 22 bold")
        category_lbl = Label(frame1, text=self.championship.category, font="Courier 22 bold")
        place_lbl = Label(frame1, text="Место проведения:", font="Courier 22 bold")
        city_lbl = Label(frame1, text=self.championship.place_championship, font="Courier 22 bold")
        title_judge_lbl = Label(frame1, text="Главный судья:", font="Courier 22 bold")
        judge_lbl = Label(frame1, text=self.championship.judge, font="Courier 22 bold")
        title_secretary_lbl = Label(frame1, text="Секретарь:", font="Courier 22 bold")
        secretary_lbl = Label(frame1, text=self.championship.secretary, font="Courier 22 bold")
        system_csp_lbl = Label(frame1, text=self.championship.system_championship, font="Courier 22 bold")
        dates_lbl = Label(frame1, text="Даты проведения турнира:", font="Courier 22 bold")
        date_start_lbl = Label(frame1, text=f'с {self.championship.start_date} - '
                                            f'по {self.championship.end_date}', font="Courier 22 bold")
        count_players_lbl = Label(frame1, text="Количество участников:", font="Courier 22 bold")
        count_lbl = Label(frame1, text=self.championship.count_player, font="Courier 22 bold")
        count_tour_lbl = Label(frame1, text="Количество туров:", font="Courier 22 bold")
        max_tour_lbl = Label(frame1, text=self.championship.max_tour, font="Courier 22 bold")

        name_csp.grid(column=0, row=0, columnspan=2, sticky=W, padx=15, pady=15)
        count_tour.grid(column=2, row=0, columnspan=2)
        tour_lbl.grid(column=2, row=1, columnspan=2, rowspan=2, padx=15)
        organization.grid(column=0, row=1, columnspan=2, sticky=W, padx=15)
        disc_lbl.grid(column=0, row=2, columnspan=2, sticky=W, padx=15)
        category_lbl.grid(column=0, row=3, sticky=W, padx=15)
        system_csp_lbl.grid(column=0, row=4, sticky=E, padx=15)
        place_lbl.grid(column=0, row=5, sticky=E, padx=15)
        city_lbl.grid(column=1, row=5, sticky=W, padx=5)
        title_judge_lbl.grid(column=0, row=6, sticky=E, padx=15)
        judge_lbl.grid(column=1, row=6, sticky=W, columnspan=2, padx=5)
        title_secretary_lbl.grid(column=0, row=7, sticky=E, padx=15)
        secretary_lbl.grid(column=1, row=7, sticky=W, columnspan=2, padx=5)
        dates_lbl.grid(column=0, row=8, sticky=E, padx=15)
        date_start_lbl.grid(column=1, row=8, columnspan=3, sticky=W, padx=5)
        count_players_lbl.grid(column=0, row=9, sticky=E, padx=15)
        count_lbl.grid(column=1, row=9, sticky=W, padx=5)
        count_tour_lbl.grid(column=0, row=10, sticky=E, padx=15)
        max_tour_lbl.grid(column=1, row=10, sticky=W, padx=5)

    def notebook_two(self, frame2):
        def next_history():
            if self.championship.get_tour < self.championship.tour:
                self.championship.get_tour += 1
                tour_label.config(text=f' {self.championship.get_tour} ТУР ')
                if self.championship.get_tour == self.championship.tour and not self.championship.finish:
                    history_frame.pack_forget()
                    frame_table.pack()
                    buttons_packs()
                else:
                    buttons_forgets()
                    frame_table.pack_forget()
                    history_table_view()
                    history_frame.pack()

        def preview_history():
            if self.championship.get_tour > 1:
                self.championship.get_tour -= 1
                tour_label.config(text=f' {self.championship.get_tour} ТУР ')
                buttons_forgets()
                frame_table.pack_forget()
                history_table_view()
                history_frame.pack()

        def history_table_view():
            history_table.delete(*history_table.get_children())
            for key_dict, val in self.championship.get_meeting.items():
                if len(val) > 1:
                    history_table.insert("", END,
                                         values=(key_dict, val[0].short_name(), '-', val[1].short_name(),
                                                 f'{val[0].pvp[val[1].user_num][0]} - '
                                                 f'{val[1].pvp[val[0].user_num][0]}',
                                                 f'{val[0].pvp[val[1].user_num][1]} - '
                                                 f'{val[1].pvp[val[0].user_num][1]}',
                                                 ))
                else:
                    history_table.insert("", END, values=(key_dict, val[0].short_name(), '-', '', '2 - 0'))

        def buttons_packs():
            if not self.championship.finish and not self.championship.status_results:
                input_result.pack()
            if self.championship.status_results:
                if self.championship.max_tour != self.championship.tour:
                    create_new_tour.pack()
                else:
                    last_result_btn.pack()
                    create_new_tour.pack_forget()

        def buttons_forgets():
            input_result.pack_forget()
            create_new_tour.pack_forget()
            last_result_btn.pack_forget()

        def input_results_local():
            if self.championship.max_tour > self.championship.tour:
                input_result.pack_forget()
                create_new_tour.pack()
            else:
                input_result.pack_forget()
                last_result_btn.pack()
            self.input_results()

        def input_last_results():
            self.championship.last_input()
            self.championship.finish = True
            self.save_status = False
            self.base_window()

        def create_next_tour():
            self.championship.create_tour()
            save_backup(self.championship)
            self.save_status = False
            self.base_window()

        # Список встреч
        title_meetings = Label(frame2, text="Список встреч", font="Courier 25 bold")
        title_meetings.pack()
        frame_title = Frame(frame2)
        preview_tour_button = Button(frame_title, text="◄", font="Arial 16 bold", command=preview_history)
        preview_tour_button.grid(row=0, column=0, padx=3, pady=2)
        tour_label = Label(frame_title, text=f' {self.championship.tour} ТУР ', font="Courier 22 bold")
        tour_label.grid(row=0, column=1, padx=3, pady=2)
        next_tour_button = Button(frame_title, text="►", font="Arial 16 bold", command=next_history)
        next_tour_button.grid(row=0, column=2, padx=3, pady=2)
        frame_title.pack()
        # ---------------------------------
        frame_table = Frame(frame2)
        scrollbar = Scrollbar(frame_table, orient=VERTICAL)
        meetings_columns = ('number_meting', 'player_1', 'num_player_1', 'dash', 'num_player_2', 'player_2')
        meetings_table = Treeview(frame_table, columns=meetings_columns, show="headings")
        meetings_table.pack(side=LEFT, fill=X)
        scrollbar.pack(side=LEFT, fill=Y)

        meetings_table.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=meetings_table.yview)
        # определяем заголовки
        meetings_table.heading("number_meting", text="№")
        meetings_table.heading("player_1", text="Игрок 1")
        meetings_table.heading("num_player_1", text="№ уч-ка")
        meetings_table.heading("num_player_2", text="№ уч-ка")
        meetings_table.heading("player_2", text="Игрок 2")
        # настраиваем столбцы
        meetings_table.column("number_meting", width=30, anchor='c', stretch=True)
        meetings_table.column("player_1", width=210, anchor='c', stretch=True)
        meetings_table.column("num_player_1", width=70, anchor='c', stretch=True)
        meetings_table.column("num_player_2", width=70, anchor='c', stretch=True)
        meetings_table.column("player_2", width=230, anchor='c', stretch=True)
        meetings_table.column("dash", width=10, anchor='c', stretch=True)
        style = Style()
        style.configure("Treeview", font=(None, 12))
        style.configure("Treeview.Heading", font=(None, 12))
        # добавляем данные
        for key, value in self.championship.list_meetings().items():
            if len(value) > 1:
                meetings_table.insert("", END, values=(key, value[0].short_name(), value[0].user_num, '-',
                                                       value[1].user_num, value[1].short_name()))
            else:
                meetings_table.insert("", END, values=(key, value[0].short_name(), value[0].user_num, '-',))
        # -------------------------------------
        history_frame = Frame(frame2)
        scrollbar = Scrollbar(history_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        history_table = Treeview(history_frame, columns=tuple(self.HISTORY_COLUMNS.keys()), show="headings", height=15)
        history_table.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=history_table.yview)
        style = Style()
        style.configure("Treeview", font=(None, 12))
        style.configure("Treeview.Heading", font=(None, 12))
        for key, value in self.HISTORY_COLUMNS.items():
            history_table.heading(key, text=value[0])
            history_table.column(key, width=value[1], anchor='c', stretch=True)
        history_table.pack(side=LEFT, fill=X)
        # ---------------------------------------------------
        input_result = Button(frame2, text='Ввести результаты встреч', font="Courier 16 bold",
                              command=input_results_local)
        create_new_tour = Button(frame2, text='Создать следующий тур', font="Courier 16 bold",
                                 command=create_next_tour)
        last_result_btn = Button(frame2, text='Применить результат', font="Courier 16 bold",
                                 command=input_last_results)
        if self.championship.finish:
            history_table_view()
            history_frame.pack()
        else:
            frame_table.pack()
            buttons_packs()

    def notebook_three(self, frame3):
        title_results = Label(frame3, text="Итоговая таблица результатов", font="Courier 16 bold")
        title_results.pack()
        frame_table = Frame(frame3)
        scrollbar = Scrollbar(frame_table, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        result_table = Treeview(frame_table, columns=tuple(self.COLUMNS_RESULT.keys()), show="headings", height=20)
        result_table.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=result_table.yview)
        style = Style()
        style.configure("Treeview", font=(None, 12))
        style.configure("Treeview.Heading", font=(None, 12))
        result_table.pack(side=LEFT)
        # определяем заголовки и столбцы
        for key, value in self.COLUMNS_RESULT.items():
            result_table.heading(key, text=value[0])
            result_table.column(key, width=value[1], anchor='c', stretch=True)
        for el in self.championship.sorted_players():
            result_table.insert("", END, values=tuple(el))
        frame_table.pack()

    def input_results(self):
        number_meeting = IntVar()
        number_meeting.set(1)
        dict_meetings = self.championship.list_meetings()
        data_results = {}
        all_results = {}

        def exit_window():
            self.base_window()
            result_window.grab_release()
            result_window.destroy()

        def input_all_results():
            self.championship.input_result(all_results.copy())
            self.save_status = False
            result_window.destroy()

        def input_step_one():
            if number_meeting.get() <= len(dict_meetings):
                title_lbl.config(text=f"Ввод результата встречи № {number_meeting.get()}")
                name_2.grid_forget()
                entry_point_1.delete(0, END)
                entry_point_2.delete(0, END)
                entry_point_1.grid_forget()
                entry_point_2.grid_forget()
                label_entry_point_1.grid_forget()
                label_entry_point_2.grid_forget()
                win_label.grid_forget()
                abr_win_label.grid_forget()
                teh_win.grid_forget()
                win_button.grid_forget()
                abr_win_button.grid_forget()
                teh_win_button.grid_forget()
                entry_button.grid_forget()
                result_label.grid_forget()
                next_button.grid_forget()
                name_1.config(text=dict_meetings[number_meeting.get()][0].short_name())
                if len(dict_meetings[number_meeting.get()]) > 1:
                    name_2.config(text=dict_meetings[number_meeting.get()][1].short_name())
                    name_2.grid(row=1, column=3, padx=2, pady=2, )
                    entry_point_1.grid(row=1, column=1, padx=2, pady=2, )
                    entry_point_2.grid(row=1, column=2, padx=2, pady=2, )
                    entry_button.grid(row=2, column=1, columnspan=2, padx=2, pady=2)
                else:
                    data_results['score'] = (2, 0)
                    all_results[number_meeting.get()] = data_results.copy()
                    number_meeting.set(number_meeting.get() + 1)
                    input_step_one()
            else:
                title_lbl.config(text="Общие результаты")
                name_1.grid_forget()
                name_2.grid_forget()
                entry_point_1.grid_forget()
                entry_point_2.grid_forget()
                label_entry_point_1.grid_forget()
                label_entry_point_2.grid_forget()
                win_label.grid_forget()
                abr_win_label.grid_forget()
                teh_win.grid_forget()
                win_button.grid_forget()
                abr_win_button.grid_forget()
                teh_win_button.grid_forget()
                entry_button.grid_forget()
                result_label.grid_forget()
                cancel_button.grid_forget()
                next_button.grid_forget()
                frame_table.grid(row=5, column=0, columnspan=4)
                exit_btn.grid(row=10, column=0, columnspan=2, padx=2, pady=2, sticky='we')
                input_results_btn.grid(row=10, column=2, columnspan=2)
                table_input_results.pack(side=LEFT, fill=BOTH, expand=1)
                scrollbar.pack(side=RIGHT, fill=Y)
                for key, val in dict_meetings.items():
                    if len(val) > 1:
                        table_input_results.insert("", END, values=(
                            key, val[0].short_name(), all_results[key]['score'], all_results[key]['points'],
                            val[1].short_name()))
                    else:
                        table_input_results.insert("", END, values=(
                            key, val[0].short_name(), all_results[key]['score']))

        def input_step_two():
            if entry_point_1.get().isdigit() and entry_point_2.get().isdigit():
                data_results['points'] = (int(entry_point_1.get()), int(entry_point_2.get()))
                label_entry_point_1.grid(row=1, column=1, padx=2, pady=2)
                label_entry_point_2.grid(row=1, column=2, padx=2, pady=2)
                label_entry_point_1.config(text=entry_point_1.get())
                label_entry_point_2.config(text=entry_point_2.get())
                entry_point_1.grid_forget()
                entry_point_2.grid_forget()
                entry_button.grid_forget()
                win_label.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky='we')
                abr_win_label.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky='we')
                teh_win.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky='we')
                win_button.grid(row=3, column=2, padx=2, pady=2, sticky='we')
                abr_win_button.grid(row=4, column=2, padx=2, pady=2, sticky='we')
                teh_win_button.grid(row=5, column=2, padx=2, pady=2, sticky='we')
                win_label.config(text="Игрок 1 победил -")
                abr_win_label.config(text="Игрок 1, присуждённая победа -")
                teh_win.config(text="Игрок 1, техническая победа -")
                win_button.config(text="3 - 1")
                abr_win_button.config(text="2 - 1")
                teh_win_button.config(text="2 - 0")
                if data_results['points'][0] < data_results['points'][1]:
                    win_label.config(text="Игрок 2 победил -")
                    abr_win_label.config(text="Игрок 2, присуждённая победа -")
                    teh_win.config(text="Игрок 2, техническая победа -")
                    win_button.config(text="1 - 3")
                    abr_win_button.config(text="1 - 2")
                    teh_win_button.config(text="0 - 2")
            else:
                input_step_one()

        def input_step_three_win():
            if data_results['points'][0] > data_results['points'][1]:
                data_results['score'] = (3, 1)
                result_label.config(text='3 - 1')
            else:
                data_results['score'] = (1, 3)
                result_label.config(text='1 - 3')
            input_step_four()

        def input_step_three_award_win():
            if data_results['points'][0] > data_results['points'][1]:
                data_results['score'] = (2, 1)
                result_label.config(text='2 - 1')
            else:
                data_results['score'] = (1, 2)
                result_label.config(text='1 - 2')
            input_step_four()

        def input_step_three_teh_win():
            if data_results['points'][0] > data_results['points'][1]:
                data_results['score'] = (2, 0)
                result_label.config(text='2 - 0')
            else:
                data_results['score'] = (0, 2)
                result_label.config(text='0 - 2')
            input_step_four()

        def input_step_four():
            win_label.grid_forget()
            abr_win_label.grid_forget()
            teh_win.grid_forget()
            win_button.grid_forget()
            abr_win_button.grid_forget()
            teh_win_button.grid_forget()
            result_label.grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky='we')
            next_button.grid(row=6, column=2, columnspan=2, padx=2, pady=2, sticky='we')

        def save_results():
            all_results[number_meeting.get()] = data_results.copy()
            number_meeting.set(number_meeting.get() + 1)
            data_results.clear()
            input_step_one()

        result_window = Toplevel()
        result_window.attributes("-topmost", True)
        result_window.title('Ввод результатов')
        result_window.grab_set()
        title_lbl = Label(result_window, font="Courier 12 bold")
        title_lbl.grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky='we')
        name_1 = Label(result_window, font="Courier 12 bold")
        name_1.grid(row=1, column=0, padx=2, pady=2, sticky='we')
        name_2 = Label(result_window, font="Courier 12 bold")
        entry_point_1 = Entry(result_window, font="Courier 12 bold", width=4)
        entry_point_2 = Entry(result_window, font="Courier 12 bold", width=4)
        label_entry_point_1 = Label(result_window, font="Courier 12 bold")
        label_entry_point_2 = Label(result_window, font="Courier 12 bold")
        entry_button = Button(result_window, text="Ввод результата", font="Courier 12 bold", command=input_step_two)
        win_label = Label(result_window, font="Courier 12 bold")
        abr_win_label = Label(result_window, font="Courier 12 bold")
        teh_win = Label(result_window, font="Courier 12 bold")
        win_button = Button(result_window, font="Courier 12 bold", command=input_step_three_win)
        abr_win_button = Button(result_window, font="Courier 12 bold", command=input_step_three_award_win)
        teh_win_button = Button(result_window, font="Courier 12 bold", command=input_step_three_teh_win)
        result_label = Label(result_window, font="Courier 12 bold")
        cancel_button = Button(result_window, text="Сбросить", font="Courier 12 bold", command=input_step_one)
        cancel_button.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky='we')
        next_button = Button(result_window, text="След. пара", font="Courier 12 bold", command=save_results)
        frame_table = Frame(result_window)
        scrollbar = Scrollbar(frame_table, orient=VERTICAL)
        list_columns = ('number_meting', 'name_1', 'score', 'points', 'name_2')
        table_input_results = Treeview(frame_table, columns=list_columns, show="headings")
        table_input_results.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=table_input_results.yview)
        table_input_results.heading('number_meting', text='№')
        table_input_results.heading('name_1', text='Игрок 1')
        table_input_results.heading('score', text='Баллы')
        table_input_results.heading('points', text='Счёт')
        table_input_results.heading('name_2', text='Игрок 2')
        table_input_results.column('number_meting', width=30, anchor='c', stretch=True)
        table_input_results.column('name_1', width=150, anchor='c', stretch=True)
        table_input_results.column('score', width=50, anchor='c', stretch=True)
        table_input_results.column('points', width=60, anchor='c', stretch=True)
        table_input_results.column('name_2', width=150, anchor='c', stretch=True)
        style = Style()
        style.configure("Treeview", font=(None, 11))
        style.configure("Treeview.Heading", font=(None, 11))
        exit_btn = Button(result_window, text="Выйти без сохранения", font="Courier 12 bold", command=exit_window)
        input_results_btn = Button(result_window, text="Внести результаты",
                                   font="Courier 12 bold", command=input_all_results)
        input_step_one()
        result_window.protocol("WM_DELETE_WINDOW", exit_window)
        result_window.mainloop()

    def save_command(self):
        self.save_status = save_championship(self.championship)

    def load_command(self):
        self.championship = load_championship()
        if self.championship is not None:
            self.base_window()

    @staticmethod
    def instruction():
        TREE_HEADS = [
            ("", "start_menu", "Главное меню", True),
            ("start_menu", "create", "Создать турнир"),
            ("start_menu", "download", "Загрузить турнир"),
            ("start_menu", "backup", "Восстановить турнир"),
            ("create", "info_csp", "Информация о турнире"),
            ("info_csp", "parameters", "Настройки турнира"),
            ("parameters", "hand_input", "Ввод данных"),
            ("parameters", "download_file", "Загрузка данных"),
            ("parameters", "systems", "Настройки турнира"),
            ("", "base_window", "Окно турнира", True),
            ("base_window", "notebook_one", "Информация о турнире"),
            ("base_window", "notebook_two", "Список пар"),
            ("base_window", "notebook_three", "Итоговый список участников"),
            ("notebook_two", "input_results", "Ввод результатов встреч"),
        ]

        def exit_inst():
            inst_window.grab_release()
            inst_window.destroy()

        def rewrite_text(key):
            text.configure(state=NORMAL)
            text.replace('1.0', END, manual_dict[key])
            text.configure(state=DISABLED)

        def select(event):
            rewrite_text(tree.selection()[0])

        inst_window = Toplevel()
        inst_window.title("Инструкция")
        inst_window.attributes("-topmost", True)
        inst_window.grab_set()
        inst_window.geometry("700x300")

        title_inst = Label(inst_window, text=" Инструкция по использованию программы", font="Arial 18 bold")
        title_inst.pack(anchor="w")

        frame_tree = Frame(inst_window)
        scrollbar_v = Scrollbar(frame_tree, orient=VERTICAL)
        scrollbar_v.pack(side=RIGHT, fill=Y)
        scrollbar_h = Scrollbar(frame_tree, orient=HORIZONTAL)
        tree = Treeview(frame_tree, show="tree")
        tree.column('#0', width=285)
        tree.config(xscrollcommand=scrollbar_h.set, yscrollcommand=scrollbar_v.set)
        scrollbar_v.config(command=tree.yview)
        scrollbar_h.config(command=tree.xview)
        tree.pack(fill=BOTH, expand=1)
        frame_tree.pack(side=LEFT, fill=BOTH, pady=10, padx=5)

        frame_text = Frame(inst_window)
        text = Text(frame_text, font="Times 16")
        text.pack(fill=BOTH, expand=1)
        scroll = Scrollbar(inst_window, command=text.yview)
        text.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y, pady=10)
        frame_text.pack(side=LEFT, fill=BOTH, expand=1, pady=10, padx=5)

        for el in TREE_HEADS:
            size_elements = len(el)
            if size_elements == 4:
                tree.insert(el[0], END, iid=el[1], text=el[2], open=el[3], )
            else:
                tree.insert(el[0], END, iid=el[1], text=el[2])

        tree.bind("<<TreeviewSelect>>", select)

        inst_window.protocol("WM_DELETE_WINDOW", exit_inst)
        inst_window.mainloop()

