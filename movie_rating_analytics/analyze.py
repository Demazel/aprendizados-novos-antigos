import pandas as pd
import numpy as np
import os
from datetime import datetime

base_dir = r'c:\Users\benja\Desktop\aprendizados-novos-antigos\data_release'

print("Loading data...")
movies = pd.read_csv(os.path.join(base_dir, 'movies.csv'))
ratings = pd.read_csv(os.path.join(base_dir, 'user_rating_history.csv'))

print("Processing timestamps...")
ratings['datetime'] = pd.to_datetime(ratings['tstamp'])
ratings['year_month'] = ratings['datetime'].dt.to_period('M').astype(str)
ratings['day_of_week'] = ratings['datetime'].dt.day_name()
ratings['hour'] = ratings['datetime'].dt.hour

# 1. Evolução de ratings ao longo do tempo (evolution of ratings over time)
print("\n--- Evolução de ratings ao longo do tempo (Ratings por Mês) ---")
evolution = ratings.groupby('year_month').size()
print(evolution.head(3))
print("...")
print(evolution.tail(3))

# 2. Ranking de filmes (Top 5 por quantidade de ratings e melhores ratings com min 100 avaliações)
movie_stats = ratings.groupby('movieId').agg(
    count=('rating', 'count'),
    mean_rating=('rating', 'mean')
).reset_index()
movie_stats = movie_stats.merge(movies, on='movieId', how='left')

print("\n--- Ranking de Filmes (Top 5 populares) ---")
top_popular = movie_stats.sort_values('count', ascending=False).head(5)
print(top_popular[['title', 'count', 'mean_rating']])

print("\n--- Ranking de Filmes (Top 5 melhor avaliados, min 100 ratings) ---")
top_rated = movie_stats[movie_stats['count'] >= 100].sort_values('mean_rating', ascending=False).head(5)
print(top_rated[['title', 'count', 'mean_rating']])

# 3. Atividade de usuários (Top 5 users and basic stats)
print("\n--- Atividade de Usuários ---")
user_activity = ratings.groupby('userId').size()
print(f"Média de avaliações por usuário: {user_activity.mean():.2f}")
print(f"Mediana: {user_activity.median()}, Máximo: {user_activity.max()}")

# 4. Análise por gênero
print("\n--- Análise por Gênero ---")
# Explode genres
movies['genres_list'] = movies['genres'].str.split('|')
movies_exploded = movies.explode('genres_list')
genre_stats = movies_exploded.merge(ratings[['movieId', 'rating']], on='movieId', how='inner')
genre_summary = genre_stats.groupby('genres_list').agg(
    count=('rating', 'count'),
    mean_rating=('rating', 'mean')
).sort_values('count', ascending=False)
print(genre_summary.head(10))

# 5. Heatmap de atividade
print("\n--- Heatmap de Atividade (Amostra de Dia vs Hora) ---")
heatmap = pd.crosstab(ratings['day_of_week'], ratings['hour'])
print(heatmap.iloc[:3, :5])  # Just print a sample for the output

# 6. Scatter de popularidade vs qualidade (Pearson correlation)
print("\n--- Popularidade vs Qualidade ---")
correlation = movie_stats['count'].corr(movie_stats['mean_rating'])
print(f"Correlação de Pearson entre quantidade de avaliações e nota média: {correlation:.4f}")
