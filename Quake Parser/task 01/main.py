import re
import json


def parse(filepath):
    # -----
    # Abre o arquivo
    file = open(filepath, "r")

    parse_object = dict()
    current_game_id = 0

    # -----
    # itera sobre as linhas do arquivo
    for line in file:
        initgame = re.search("^(\s)*[0-9]+:[0-9]+ InitGame:", line)
        kill = re.search("^(\s)*[0-9]+:[0-9]+ Kill:\s[0-9]+\s[0-9]+\s[0-9]+:\s", line)

        # -----
        # para cada início de partida gera uma nova chave no dcionário
        if initgame is not None:
            current_game_id += 1
            parse_object[f"game_{current_game_id}"] = { "total_kills": 0, "players": list(), "kills": dict() }
        
        # -----
        # procura por cada kill no log
        elif kill is not None:
            # -----
            # adiciona à contagem de kill da partida correspondente 
            parse_object[f"game_{current_game_id}"]["total_kills"] += 1

            # -----
            # separa o killer e a vitima
            line = line[kill.end():-1]
            killer = line.split(" killed ")[0]
            victim = line.split(" killed ")[1].split(" by ")[0]
            

            # -----
            # adiciona a vitima à lista de player e ao dicionário de kills caso já não exista
            if victim not in parse_object[f"game_{current_game_id}"]["players"]:
                parse_object[f"game_{current_game_id}"]["players"].append(victim)
                parse_object[f"game_{current_game_id}"]["kills"][victim] = 0
            
            # -----
            # remove 1 kill de cada player morto pelo mapa
            if killer == "<world>":
               parse_object[f"game_{current_game_id}"]["kills"][victim] -= 1             

            # -----
            # adiciona o killer à lista de player e ao dicionário de kills caso já não exista e não seja o mapa
            if killer != "<world>" and killer not in parse_object[f"game_{current_game_id}"]["players"]:
                parse_object[f"game_{current_game_id}"]["players"].append(killer)
                parse_object[f"game_{current_game_id}"]["kills"][killer] = 0

            # -----S
            # adiciona 1 kill a cada killer
            if killer != "<world>":     
                parse_object[f"game_{current_game_id}"]["kills"][killer] += 1
    # -----
    # fecha o arquivo            
    file.close()

    # -----
    # transforma o dicionário "parse_object" em um arquivo json
    with open("output.json", "w") as outfile:
        json.dump(parse_object, outfile, indent=4)

    # -----
    # retorna o relatório do jogo
    return parse_object



if __name__ == '__main__':
    parse('games.log')
