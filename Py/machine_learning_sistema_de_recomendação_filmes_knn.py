# -*- coding: utf-8 -*-
"""Machine_learning_Sistema_de_recomendação_filmes_KNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1khLjywU_z3ihIAeHDbtpK5lCJ19QIioO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregando os dados
# Certifique-se de ajustar o caminho para o arquivo 'ratings.csv'
data = pd.read_csv('/content/ratings.csv')
data

# Vamos criar uma matriz de utilidade usando a função pivot_table do pandas
utilidade = data.pivot_table(index='userId',
                             columns='movieId',
                             values='rating',
                             fill_value=0)
utilidade

# Transformando a matriz de utilidade em uma matriz numpy para trabalhar com o scikit-learn
utilidade_matrix = utilidade.to_numpy()

# Importando biblioteca
from sklearn.metrics.pairwise import cosine_similarity

# Calculando a similaridade do cosseno entre os usuários
similaridade = cosine_similarity(utilidade_matrix)
similaridade

# Importando biblioteca
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

# Lista de valores de k que queremos testar
valores_k = [3, 5, 7, 10, 15]

# Vamos usar a validação cruzada para encontrar o valor ótimo de k
scores = {}
for k in valores_k:
    modelo_knn = KNeighborsRegressor(n_neighbors=k, metric='cosine', algorithm='brute')

    # Calculando o RMSE usando a validação cruzada
    rmse_scores = -cross_val_score(modelo_knn, utilidade_matrix, utilidade_matrix, scoring='neg_mean_squared_error', cv=5)
    scores[k] = np.sqrt(rmse_scores.mean())

# Escolhendo o melhor valor de k com base no RMSE
melhor_k = min(scores, key=scores.get)
print("Valores de k e seus RMSE")
print()
for k, rmse in scores.items():
    print(f"k = {k}, RMSE = {rmse}")

print()
print("Melhor valor de k encontrado:", melhor_k)
print()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# # Importando biblioteca
# from sklearn.neighbors import NearestNeighbors
# 
# # Modelo machine learning - KNN
# # Definindo o número de vizinhos (k) que o algoritmo K-NN usará
# k = 15
# modelo_knn = NearestNeighbors(n_neighbors=k, metric='cosine', algorithm='brute')
# modelo_knn.fit(utilidade_matrix)

# Função para fazer as recomendações para um usuário específico
def fazer_recomendacoes(usuario_id, num_recomendacoes=5):
    if usuario_id >= utilidade_matrix.shape[0]:
        print(f"Usuário de ID {usuario_id} não encontrado nos dados.")
        return []

    usuario_interacoes = utilidade_matrix[usuario_id].reshape(1, -1)

    # Encontrando os k vizinhos mais próximos
    distancias, indices_vizinhos = modelo_knn.kneighbors(usuario_interacoes)

    # Verificando se há vizinhos suficientes para fazer recomendações
    if len(indices_vizinhos[0]) < k:
        print("Não há vizinhos suficientes para fazer recomendações.")
        return []

    # Recomendando filmes com base nos vizinhos mais próximos
    filmes_recomendados = []
    for indice_vizinho in indices_vizinhos[0]:
        filmes_recomendados.extend(np.where(utilidade_matrix[indice_vizinho] > 0)[0])

    # Removendo filmes já interagidos pelo usuário
    filmes_recomendados = set(filmes_recomendados) - set(np.where(utilidade_matrix[usuario_id] > 0)[0])

    # Classificando os filmes recomendados com base na média das avaliações dos vizinhos
    filmes_recomendados = list(filmes_recomendados)
    filmes_recomendados.sort(key=lambda x: np.mean(utilidade_matrix[indices_vizinhos[:, 1]][:, x]), reverse=True)

    return filmes_recomendados[:num_recomendacoes]

# Fazendo recomendações para o usuário de id 0
usuario_id_alvo = 3
recomendacoes = fazer_recomendacoes(usuario_id_alvo)

if len(recomendacoes) > 0:
    # Obtendo os títulos dos filmes recomendados
    filmes = pd.read_csv('/content/movies.csv')  # Certifique-se de ajustar o caminho para o arquivo 'movies.csv'
    titulos_recomendados = filmes[filmes['movieId'].isin(recomendacoes)]['title'].tolist()

    print("Filmes recomendados para o usuário de id", usuario_id_alvo, "são:")
    print()
    for titulo in titulos_recomendados:
        print(titulo)







