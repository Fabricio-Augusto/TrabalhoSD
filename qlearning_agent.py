import numpy as np
import os
import random

class AgenteQLearning:
    def __init__(self, acoes, taxa_aprendizado=0.1, desconto=0.9, epsilon=0.1, intervalo_salvamento=50):
        self.acoes = acoes  # Lista de ações possíveis
        self.q_table = {}  # Tabela Q para armazenar os valores Q
        self.taxa_aprendizado = taxa_aprendizado
        self.desconto = desconto
        self.epsilon = epsilon
        self.intervalo_salvamento = intervalo_salvamento
        self.contador_requests = 0
        self.carregar_modelo()

    def _obter_chave_estado(self, estado):
        """Gera uma chave única para o estado."""
        return str(estado)

    def escolher_acao(self, estado):
        """Escolhe uma ação com base na política ɛ-greedy."""
        chave_estado = self._obter_chave_estado(estado)
        if chave_estado not in self.q_table:
            self.q_table[chave_estado] = {acao: 0 for acao in self.acoes}

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.acoes)
        return max(self.q_table[chave_estado], key=self.q_table[chave_estado].get)

    def atualizar_q(self, estado_antigo, acao, recompensa, estado_novo):
        """Atualiza o valor Q usando a equação do Q-Learning."""
        chave_antiga = self._obter_chave_estado(estado_antigo)
        chave_nova = self._obter_chave_estado(estado_novo)
        
        if chave_antiga not in self.q_table:
            self.q_table[chave_antiga] = {acao: 0 for acao in self.acoes}
        if chave_nova not in self.q_table:
            self.q_table[chave_nova] = {acao: 0 for acao in self.acoes}

        q_atual = self.q_table[chave_antiga][acao]
        q_futuro = max(self.q_table[chave_nova].values())  # Melhor ação futura

        self.q_table[chave_antiga][acao] = q_atual + self.taxa_aprendizado * (
            recompensa + self.desconto * q_futuro - q_atual
        )

        # Incrementar o contador de requests e salvar se necessário
        self.contador_requests += 1
        if self.contador_requests >= self.intervalo_salvamento:
            self.salvar_modelo()
            self.contador_requests = 0

    def salvar_modelo(self, caminho="modelo_qlearning.npy"):
        """Salva a tabela Q em um arquivo."""
        print('Salvando Modelo')
        np.save(caminho, self.q_table)

    def carregar_modelo(self, caminho="modelo_qlearning.npy"):
        """Carrega a tabela Q de um arquivo."""
        if os.path.exists(caminho):
            self.q_table = np.load(caminho, allow_pickle=True).item()
            print(f"Modelo carregado com sucesso de {caminho}.")
        else:
            print(f"Arquivo de modelo {caminho} não encontrado. Iniciando com Q-table vazia.")

    def tratar_acao_impossivel(self, estado_atual, acao):
        """Trata ações impossíveis e escolhe uma ação alternativa."""
        estamina = estado_atual['estamina_inimigo']
        novaAcao = None

        if acao.startswith("bloqueando") and estamina == 0:
            self.q_table[self._obter_chave_estado(estado_atual)][acao] = -1000
            novaAcao = self.escolher_acao(estado_atual)
        elif (acao.startswith("esquiva_esq_10") or acao.startswith("ataque_leve")) and estamina <= 1:
            self.q_table[self._obter_chave_estado(estado_atual)][acao] = -1000 
            novaAcao = self.escolher_acao(estado_atual)
        elif acao.startswith("ataque_pesado") and estamina <= 2:
            self.q_table[self._obter_chave_estado(estado_atual)][acao] = -1000
            novaAcao = self.escolher_acao(estado_atual)
        
        if novaAcao is None:
            return acao
        else:
            return self.tratar_acao_impossivel(estado_atual, novaAcao)
