from random import sample

NUM_ONE = 1


def create_dict_players(list_players):
    number_player = NUM_ONE
    dict_players = {}
    new_list_players = sample(list_players, len(list_players))
    for player in new_list_players:
        dict_players[number_player] = player
        player.user_num = number_player
        number_player += NUM_ONE
    return dict_players
