from flask import Flask, jsonify, request
import json


app = Flask(__name__)
data = {}

@app.route('/matches/<int:id>', methods = ['GET'])
def get_game(id):
    # -----
    # tenta retornar a partida selecionada
    try:
        return jsonify(data[f"game_{id}"])
    # -----
    # Em caso de erro avisa que a partida não foi encontrada
    except:
        return 'Partida não encontrada!', 404


@app.route('/matches', methods=['POST'])
def add_game():
    try:
        # -----
        # acrescenta a partida ao dicionário
        data[f"game_{len(data.keys()) + 1}"] = request.get_json()

        # -----
        # atualiza o arquivo json
        with open("output.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        return 'Partida adicionada com sucesso!'
    except:
        return 'Erro ao adicionar partida!', 400


@app.route('/matches/<int:id>', methods=['PUT'])
def update_game(id):
    # -----
    # verifica se o id é válido
    if 1 > id or id > len(data.keys()) :
        return 'Partida não encontrada!', 400

    try:
        # -----
        # atualiza a partida com o id indicado
        data[f"game_{id}"] = request.get_json()

        # -----
        # atualiza o arquivo json
        with open("output.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        return 'Partida atualizada com sucesso!'
    except:
        return 'Erro ao atualizar partida!', 400


@app.route('/matches/<int:id>', methods=['DELETE'])
def delete_game(id):
    # -----
    # verifica se o id é válido
    if 1 > id or id > len(data.keys()) :
        return 'Partida não encontrada!', 400

    try:
        # -----
        # deleta a partida com o id selecionado e atualiza o id das posteriores
        for i in range(id, len(data.keys()), 1):
            data[f"game_{i}"] = data[f"game_{i+1}"]
        data.pop(f"game_{len(data.keys())}")

        # -----
        # atualiza o arquivo json
        with open("output.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        return 'Partida atualizada com sucesso!'
    except:
        return 'Erro ao atualizar partida!', 400


if __name__ == '__main__':
    # -----
    # tenta ler o arquivo json com o relatório da partida
    try:
        with open("output.json") as json_file:
            data = json.load(json_file)
    # -----
    # Caso não consiga exibe mensagem de erro
    except:
        print("\033[1;31m Erro ao abrir relatório de partidas!\033[0m")
    app.run()
