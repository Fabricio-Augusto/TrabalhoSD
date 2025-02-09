from flask import Flask, request, jsonify
from qlearning_agent import AgenteQLearning
import random
import threading

app = Flask(__name__)

acoes = ["esquiva_esq_10", "bloqueando_frente"]
acaoRemover = "esquiva_esq_10"
agente = AgenteQLearning(acoes)
ultimo_estado = None
ultima_acao = None

def restaurar_acao(acao):
    """Adiciona uma ação de volta à lista após 3 segundos."""
    if acao not in acoes:
        acoes.append(acao)
        print(f"Ação {acao} restaurada!")

@app.route('/data', methods=['POST'])
def receber_dados():
    global ultimo_estado, ultima_acao

    dados = request.get_json()
    print('------------ Dados ------------')
    print(dados)
    print('------------ Dados ------------\n')

    # Processamento do estado (exemplo simplificado)
    distancia = dados.get('distancia')
    if distancia <= 230:
        distancia = 0
    elif distancia <= 400:
        distancia = 1
    else:
        distancia = 2

    estaminaPlayer = max(dados.get('estamina_player'), 0)
    if estaminaPlayer >= 50:
        estaminaPlayer = 3
    elif estaminaPlayer >= 20:
        estaminaPlayer = 2
    elif estaminaPlayer >= 10:
        estaminaPlayer = 1
    else:
        estaminaPlayer = 0

    estaminaInimigo =  max(dados.get('estamina_inimigo'), 0)
    if estaminaInimigo >= 50:
        estaminaInimigo = 4
    elif estaminaInimigo >= 20:
        estaminaInimigo = 3
    elif estaminaInimigo >= 10:
        estaminaInimigo = 2
    elif estaminaInimigo >= 0.5:
        estaminaInimigo = 1
    else:
        estaminaInimigo = 0
    
    porcentagemAnim = dados.get('percentual_animacao_player')
    if porcentagemAnim == 3 or porcentagemAnim == 5:
        porcentagemAnim = 4
    elif porcentagemAnim >=6:
        porcentagemAnim = 6

    print('------------ ESTADO USADO NO GAME ------------')
    estado_atual = {
        'distancia': distancia,
        'estamina_player': estaminaPlayer,
        'estamina_inimigo':estaminaInimigo,
        'bloqueio_player': dados.get('bloqueio_player'),
        'animacao_player': dados.get('animacao_player'),
        'percentual_animacao_player': porcentagemAnim,
    }
    print(estado_atual)
    print('------------ ESTADO USADO NO GAME ------------\n')
    
    gameOver = dados.get('game_over', False)

    feedback = {
        "bloqueio_sucesso": dados.get('bloqueio_sucesso', 0),
        "esquiva_sucesso": dados.get('esquiva_sucesso', 0),
        "vida_causada": dados.get('vida_causada', 0),
        "vida_perdida": dados.get('vida_perdida', 0),
        "tempo_sem_dano_causado": dados.get('tempo_sem_dano_causado', 0),
        "tempo_sem_dano_recebido": dados.get('tempo_sem_dano_recebido', 0),
        "estamina_gasta": dados.get('estamina_gasta', 0),
        "estamina_player_retirada": dados.get('estamina_player_retirada', 0)
    }

    print('------------ FEEDBACK ------------')
    print(feedback)
    print('------------ FEEDBACK ------------\n')

    if ultimo_estado is not None and ultima_acao is not None:
        recompensa = (
            feedback["bloqueio_sucesso"] * 100 +
            feedback["esquiva_sucesso"] * 100 +
            feedback["vida_causada"] * 12 -
            feedback["vida_perdida"] * 20 -
            0.02 * feedback["tempo_sem_dano_causado"] -
            feedback["estamina_gasta"] * 1 +
            feedback['estamina_player_retirada']
        )
        print('------------ RECOMPENSA RELACIONADA A ACAO '+ ultima_acao + '------------')
        print(recompensa)
        print('------------ RECOMPENSA RELACIONADA A ACAO '+ ultima_acao + '------------\n')

    # Escolhe uma ação aleatória disponível
    proxima_acao = random.choice(acoes)

    # Se a ação escolhida for "bloqueando_frente", removemos temporariamente e restauramos depois de 3s
    if proxima_acao == acaoRemover:
        acoes.remove(proxima_acao)
        threading.Timer(3.0, restaurar_acao, args=[proxima_acao]).start()

    print('\n\n\n\n')
    print('------------ ACAO ------------')
    print(proxima_acao)
    print('------------ ACAO ------------\n')

    return jsonify({"enemy_action": proxima_acao}), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
