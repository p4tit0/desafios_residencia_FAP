import json


def read_parsed_log(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        print(json.dumps(data, indent=4))
        
        return data


def print_rank(data):
    # -----
    # cria um dicionario para armazenar o ranking
    ranking = dict()

    # -----
    # itera por cada partida
    for game in data.values():

        # -----
        # itera por cada jogador e modifica sua pontuação no ranking 
        for player, kills in game["kills"].items():
            if player not in ranking.keys():
                ranking[player] = 0
            ranking[player] += kills
    # -----
    # organiza o ranking em ordem decrescente
    sorted_ranking = sorted(ranking.items(), key=lambda x:x[1], reverse=True)

    # -----
    # exibe o ranking
    print()
    print("\033[1;3;4;7;33m -=-=-=- RANKING -=-=-=- \033[0m")
    i = 1
    for player, kills in sorted_ranking:
        match i:
            case 1:
                print("\033[1;38;5;220m", end="")
            case 2:
                print("\033[1;38;5;250m", end="")
            case 3:
                print("\033[1;38;5;172m", end="")
            case _:
                print("\033[37m", end="")
        print(f"{i:02d}º --> {player} : {kills}")
        print("\033[0m", end="")
        i += 1
            



if __name__ == '__main__':
    data = read_parsed_log('output.json')
    print_rank(data)
    input("Press Enter to exit...")