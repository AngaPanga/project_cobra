class Player:
    ZERO = 0
    ONE = 1
    START_RATE = 1000  # стартовый рейтинг

    def __init__(self, name, sirname, second_name,  # u_num,
                 date=None,
                 club=None,
                 city=None,
                 level=ZERO,
                 rate=START_RATE):
        self.__u_num = None  # номер игрока
        self.__name = name  # имя
        self.__sirname = sirname  # фамилия
        self.__second_name = second_name  # отчество
        self.__date = date  # дата рождения
        self.__city = city  # город
        self.__level = level  # разряд игрока
        self.__rate = rate  # рейтинг игрока
        self.__club = club  # клуб игрока
        self.__score = self.ZERO  # баллы игрока
        self.__dict_pvp = {}  # словарь игрок и результат встречи
        self.__coefficient = self.ZERO  # коэфициент позиции в таблице
        self.__sum_points = self.ZERO # сумма всех набранных очков
        self.__outsider = True

    @staticmethod
    def create_player(data):
        if len(data) > 7:
            if data[7].isdigit():
                data[7] = int(data[7])
            else:
                data[7] = 1000
        if len(data) > 6:
            if data[6].isdigit():
                data[6] = int(data[6])
            else:
                data[6] = 0
        return Player(*data)

    def player_tuple(self):
        return (self.__name, self.__sirname, self.__second_name,
                self.__date, self.__club, self.__city,
                self.__level, self.__rate)

    def __str__(self):
        return f'{self.__u_num}. ' \
               f'{self.__sirname} ' \
               f'{self.__name} ' \
               f'{self.__second_name} ' \
               f'{self.__score}' \
               f'{self.__dict_pvp}'

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score

    @property
    def user_num(self):
        return self.__u_num

    @user_num.setter
    def user_num(self, num):
        self.__u_num = num

    @property
    def full_name(self):
        return self.__sirname + " " + self.__name + " " + self.__second_name

    def short_name(self):
        return self.__sirname + ' ' + \
               self.__name[self.ZERO].upper() + '. ' + \
               self.__second_name[self.ZERO].upper() + '. '

    def input_pvp(self, num_user, result):
        self.__dict_pvp[num_user] = result

    @property
    def pvp(self):
        return self.__dict_pvp

    @property
    def player_coefficient(self):
        return self.__coefficient

    @player_coefficient.setter
    def player_coefficient(self, coefficient):
        self.__coefficient = coefficient

    @property
    def points(self):
        return self.__sum_points

    @points.setter
    def points(self, point):
        self.__sum_points = point

    @property
    def rate(self):
        return  self.__rate

    @property
    def sort_key(self):
        return self.__score, self.__coefficient, self.__sum_points, (-1 * self.__rate)

    @property
    def outsider(self):
        return self.__outsider

    @outsider.setter
    def outsider(self, change):
        self.__outsider = change
