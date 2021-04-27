import matplotlib
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("movie.csv")
sd = pd.read_csv("rating.csv")

df.columns
sd.columns

df = df.loc[:,["movieId", "title"]]
sd = sd.loc[:, ["userId","movieId","rating"]]

# Sistema de recomendação de filmes - Movie Lens
dados = pd.merge(df, sd)
dados = dados.iloc[:9000000, :]

def recomendacao_filmes(filmes):
    filmes = dados.pivot_table(index = ["userId"],columns = ["title"],values = "rating")
    return filmes
    
def filmes_recomendacao(filmes2):
    filmes_recomendacao = pivot_table["Bad Boys (1995)"]
    filmes_recomendacao_simil = pivot_table.corrwith(filmes_recomendacao)
    filmes_recomendacao_simil = filmes_recomendacao_simil.sort_values(ascending = False)
    filmes_recomendacao_simil
    return

recomendacao_filmes = filmes_recomendacao_simil.head(10)
recomendacao_filmes

filmes_recomendacao = pivot_table["Ace Ventura: When Nature Calls (1995)"]
filmes_recomendacao_simil = pivot_table.corrwith(filmes_recomendacao)
filmes_recomendacao_simil = filmes_recomendacao_simil.sort_values(ascending = False)

recomendacao_filmes = filmes_recomendacao_simil.head(10)
recomendacao_filmes

















