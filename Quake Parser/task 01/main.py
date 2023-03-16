import re
import json


def parse(filepath):
    file = open(filepath, "r")

    parse_object = dict()
    current_game_id = 0

    for line in file:
        initgame = re.search("^(\s)*[0-9]+:[0-9]+ InitGame:", line)
        kill = re.search("^(\s)*[0-9]+:[0-9]+ Kill:\s[0-9]+\s[0-9]+\s[0-9]+:\s", line)
        if initgame is not None:
            current_game_id += 1
            parse_object[f"game_{current_game_id}"] = { "total_kills": 0, "players": list(), "kills": dict() }
        elif kill is not None:
            parse_object[f"game_{current_game_id}"]["total_kills"] += 1

            line = line[kill.end():-1]
            killer = line.split(" killed ")[0]
            victim = line.split(" killed ")[1].split(" by ")[0]
            
            if victim not in parse_object[f"game_{current_game_id}"]["players"]:
                parse_object[f"game_{current_game_id}"]["players"].append(victim)
                parse_object[f"game_{current_game_id}"]["kills"][victim] = 0
            
            if killer == "<world>":
               parse_object[f"game_{current_game_id}"]["kills"][victim] -= 1             

            if killer != "<world>" and killer not in parse_object[f"game_{current_game_id}"]["players"]:
                parse_object[f"game_{current_game_id}"]["players"].append(killer)
                parse_object[f"game_{current_game_id}"]["kills"][killer] = 0

            if killer != "<world>":     
                parse_object[f"game_{current_game_id}"]["kills"][killer] += 1
                
    file.close()

    with open("output.json", "w") as outfile:
        json.dump(parse_object, outfile, indent=4)

    return parse_object



if __name__ == '__main__':
    parse('games.log')
