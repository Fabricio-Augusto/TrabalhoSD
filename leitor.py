import numpy as np
import os

def carregar_e_exportar_modelo(caminho_modelo="modelo_qlearning.npy", caminho_exportacao="modelo_qlearning.txt"):
    # Carregar a tabela Q do arquivo
    if os.path.exists(caminho_modelo):
        q_table = np.load(caminho_modelo, allow_pickle=True).item()
        
        with open(caminho_exportacao, "w") as arquivo_txt:
            for estado, acoes in q_table.items():
                arquivo_txt.write(f"Estado: {estado}\n")
                for acao, valor in acoes.items():
                    arquivo_txt.write(f"  Ação: {acao} -> Valor Q: {valor}\n")
                arquivo_txt.write("\n")
                
        print(f"Modelo exportado com sucesso para {caminho_exportacao}")
    else:
        print(f"Arquivo {caminho_modelo} não encontrado.")

# Exemplo de uso
carregar_e_exportar_modelo()
