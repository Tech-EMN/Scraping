from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from flasgger import Swagger, swag_from
import atexit

from query_scrapp import get_video_id

app = Flask(__name__)
swagger = Swagger(app)

# Definindo as funções para as tarefas
def tarefa_1():
    get_video_id()
    print("Tarefa 1 executada")

def tarefa_2():
    print("Tarefa 2 executada")

def tarefa_3():
    print("Tarefa 3 executada")

# Configurando o scheduler
scheduler = BackgroundScheduler()

# Adicionando as tarefas para rodar a cada 1 minuto
#scheduler.add_job(func=tarefa_1, trigger="interval", minutes=1, id="tarefa_1")
scheduler.add_job(func=tarefa_2, trigger="interval", minutes=1, id="tarefa_2")
scheduler.add_job(func=tarefa_3, trigger="interval", minutes=1, id="tarefa_3")

# Iniciando o scheduler
scheduler.start()

# Certifique-se de que o cron seja parado quando a aplicação for encerrada
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def home():
    return "Servidor Flask com múltiplos Cron Jobs!"

@app.route('/executar_tarefa', methods=['POST'])
@swag_from({
    'tags': ['Tarefas'],
    'description': 'Executa uma tarefa específica com base no nome fornecido.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'tarefa': {
                        'type': 'string',
                        'description': 'Nome da tarefa a ser executada',
                        'example': 'tarefa_1'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Tarefa executada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'mensagem': {
                        'type': 'string',
                        'example': 'tarefa_1 executada com sucesso'
                    }
                }
            }
        },
        400: {
            'description': 'Erro na requisição',
            'schema': {
                'type': 'object',
                'properties': {
                    'erro': {
                        'type': 'string',
                        'example': 'Tarefa \'tarefa_1\' não existe'
                    }
                }
            }
        }
    }
})
def executar_tarefa():
    data = request.get_json()
    
    if not data or 'tarefa' not in data:
        return jsonify({"erro": "Parâmetro 'tarefa' é necessário"}), 400

    tarefa = data['tarefa']

    if tarefa == "tarefa_1":
        tarefa_1(data['url'])
    elif tarefa == "tarefa_2":
        tarefa_2()
    elif tarefa == "tarefa_3":
        tarefa_3()
    else:
        return jsonify({"erro": f"Tarefa '{tarefa}' não existe"}), 400

    return jsonify({"mensagem": f"{tarefa} executada com sucesso"}), 200

if __name__ == "__main__":
    # Expondo o servidor no localhost na porta 3000
    app.run(host="0.0.0.0", port=3000)
