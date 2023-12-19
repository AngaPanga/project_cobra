from abc import ABC, abstractmethod


class ChampionShipABC(ABC):
    ZERO = 0
    ONE = 1

    def __init__(self,
                 name_championship,
                 organization,
                 start_date,
                 end_date,
                 discipline,
                 place_championship,
                 judge,
                 secretary,
                 category,
                 count_player,
                 system_championship,
                 dict_players,
                 max_tour):
        self._name_championship = name_championship
        self._organization = organization
        self._start_date = start_date
        self._end_date = end_date
        self._discipline = discipline
        self._place_championship = place_championship
        self._judge = judge
        self._secretary = secretary
        self._dict_players = dict_players
        self._tour = self.ZERO
        self._get_tour = self.ZERO
        self._category = category
        self._count_player = count_player
        self._system_championship = system_championship
        self._max_tour = max_tour
        self._history_meetings = {}
        self._status_results = True
        self._finish = False

    # Создание пар
    @abstractmethod
    def coefficient(self):
        pass

    @abstractmethod
    def plr_vs_plr(self):
        pass

    @property
    def name_championship(self):
        return self._name_championship

    @property
    def organization(self):
        return self._organization

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def discipline(self):
        return self._discipline

    @property
    def place_championship(self):
        return self._place_championship

    @property
    def judge(self):
        return self._judge

    @property
    def secretary(self):
        return self._secretary

    @property
    def category(self):
        return self._category

    @property
    def count_player(self):
        return self._count_player

    @property
    def system_championship(self):
        return self._system_championship

    # возращение статуса результатов
    @property
    def status_results(self):
        return self._status_results

    # возращение значения тура
    @property
    def tour(self):
        return self._tour

    @property
    def get_tour(self):
        return self._get_tour

    @get_tour.setter
    def get_tour(self, step):
        self._get_tour = step

    # создание нового тура
    def create_tour(self):
        if self._tour <= self._max_tour:
            if self._status_results:
                self._tour += self.ONE
                self._get_tour = self._tour
                self._history_meetings[self._tour] = self.plr_vs_plr()
                self._status_results = False

    # ввод резульатов
    def input_result(self, results):
        if self._tour <= self._max_tour:
            dict_meeting = self._history_meetings[self._tour]
            for num, meeting in dict_meeting.items():
                if len(meeting) > 1:
                    meeting[self.ZERO].score += results[num]['score'][self.ZERO]
                    meeting[self.ZERO].points += results[num]['points'][self.ZERO]
                    meeting[self.ZERO].input_pvp(
                        meeting[self.ONE].user_num, (results[num]['score'][self.ZERO],
                                                     results[num]['points'][self.ZERO]))
                    meeting[self.ONE].score += results[num]['score'][self.ONE]
                    meeting[self.ONE].points += results[num]['points'][self.ONE]
                    meeting[self.ONE].input_pvp(
                        meeting[self.ZERO].user_num, (results[num]['score'][self.ONE],
                                                      results[num]['points'][self.ONE]))
                else:
                    meeting[self.ZERO].score += results[num]['score'][self.ZERO]
            self._status_results = True
            self.coefficient()

    # возращение списка встреч
    def list_meetings(self):
        if self._tour in self._history_meetings.keys():
            return self._history_meetings[self._tour]

    # возращениие словаря игроков
    @property
    def dict_players(self):
        return self._dict_players

    @property
    def max_tour(self):
        return self._max_tour

    def sorted_players(self):
        place = 1
        sort_result_list = []
        sort_list_players = sorted(self.dict_players.values(), key=lambda x: x.sort_key, reverse=True)
        for el in sort_list_players:
            sort_result_list.append(
                [place, el.user_num,el.full_name, el.score, el.player_coefficient, el.points, el.rate]
            )
            place += 1
        return sort_result_list

    def last_input(self):
        if self._tour == self._max_tour:
            if self._status_results:
                # self._history_meetings[self._tour] = self.plr_vs_plr()
                self._status_results = False

    @property
    def get_meeting(self):
        return self._history_meetings[self._get_tour]

    @property
    def finish(self):
        return self._finish

    @finish.setter
    def finish(self, change):
        self._finish = change
