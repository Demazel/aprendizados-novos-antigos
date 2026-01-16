import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Parte B: Manipulação e Análise ---

# 1. Carregue o dataset.
csv_path = os.path.join(os.path.dirname(__file__), 'able1.csv')

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em: {csv_path}")
    print("Verifique se o arquivo 'able1.csv' está na mesma pasta do script.")
    exit()
except Exception as e:
    print(f"Erro ao abrir o arquivo: {e}")
    exit()

# Limpar nomes das colunas (remover espaços extras se houver)
df.columns = df.columns.str.strip()

# 2. Trate os dados: Startups com status "Inativa" devem ser excluídas das análises de investimento, 
# mas mantidas em um dataframe separado para análise de falhas.
df_ativa = df[df['status'] == 'Ativa'].copy()
df_inativa = df[df['status'] == 'Inativa'].copy()

print(f"Total de Startups Ativas: {len(df_ativa)}")
print(f"Total de Startups Inativas: {len(df_inativa)}")

# Identificar colunas de notas (começam com um dígito)
score_cols = [col for col in df.columns if col[0].isdigit()]

# 3. Crie uma nova coluna Score_Global contendo a média de todas as notas da startup.
df_ativa['Score_Global'] = df_ativa[score_cols].mean(axis=1)

# 4. Agrupe as colunas por dimensão (ex: média de todas as colunas (média avaliações 1, média avaliações 2…)) para criar uma visão macro.
# Assumindo que o primeiro caractere da coluna indica a dimensão (1 a 8).
for i in range(1, 9):
    dim_cols = [col for col in score_cols if col.startswith(f'{i}.')]
    if dim_cols:
        df_ativa[f'Score_Dim{i}'] = df_ativa[dim_cols].mean(axis=1)

# Imprimir Score Global das top 5 para verificação
print("\nTop 5 Startups por Score Global:")
print(df_ativa[['nome_startup', 'Score_Global']].sort_values(by='Score_Global', ascending=False).head())


# --- Parte C: Visualização de Dados ---

# 1. Gere um Gráfico de Radar (Spider Plot) para a startup de melhor Score_Global entre as ativas.
best_global_startup = df_ativa.loc[df_ativa['Score_Global'].idxmax()]
print(f"\nStartup com Melhor Score Global: {best_global_startup['nome_startup']} (Score: {best_global_startup['Score_Global']:.2f})")

# Preparar dados para o Radar Chart
categories = [f'Dimensão {i}' for i in range(1, 9)]
values = [best_global_startup[f'Score_Dim{i}'] for i in range(1, 9)]
values += values[:1] # Fechar o ciclo

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles, values, color='blue', alpha=0.25)
ax.plot(angles, values, color='blue', linewidth=2)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(['1', '2', '3', '4', '5'], color='gray')
ax.set_ylim(0, 5) # Garantir escala de 0 a 5
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_title(f"Performance da {best_global_startup['nome_startup']} (Melhor Global)", y=1.1)
plt.savefig('radar_chart.png')
print("Gráfico de Radar salvo como 'radar_chart.png'")
# plt.show() # Descomentar se rodar localmente com interface gráfica

# 2. Boxplot (Análise de Setor): Todos os setores
# sectors_to_compare = ['Agri-IoT', 'SmartCity'] # Removendo filtro específico
df_sectors = df_ativa # Usar todas as startups ativas para comparar todos os setores

plt.figure(figsize=(8, 6))
df_sectors.boxplot(column='Score_Global', by='setor', grid=False)
plt.title('Distribuição do Score_Global por Setor')
plt.grid(axis='y', color='gray', linestyle='--', linewidth=0.5 )
plt.suptitle('') # Remove o título automático do pandas
plt.ylabel('Score Global')
plt.xlabel('Setor')
plt.savefig('boxplot_sectors.png')
print("Boxplot salvo como 'boxplot_sectors.png'")
# plt.show()

# Pergunta: Existem outliers?
# Cálculo simples de outliers via IQR para responder programaticamente ou visualmente.
print("\n--- Análise de Outliers ---")
sectors_to_compare = df_sectors['setor'].unique() # Atualizar lista de setores dinamicamente
for setor in sectors_to_compare:
    data = df_sectors[df_sectors['setor'] == setor]['Score_Global']
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    print(f"Setor {setor}: {len(outliers)} outliers encontrados.")
    if len(outliers) > 0:
        print(f"  Valores dos outliers: {outliers.values}")


# --- Parte D: Tomada de Decisão (Insight) ---

print("\n--- Parte D: Tomada de Decisão ---")
# 1. Investir na startup que tenha o melhor equilíbrio entre Performance Técnica (Grupo 1) e Viabilidade Econômica (Grupo 2).
# Grupo 1 (Performance Técnica) = Dimensão 1? O enunciado diz "Performance Técnica (Grupo 1)". 
# Vamos assumir que Dimensão 1 é o Grupo 1 e Dimensão 2 é o Grupo 2 conforme os prefixos das colunas (1.x e 2.x).
# Equilíbrio pode ser interpretado como uma média ponderada ou simplesmente uma alta pontuação em ambas.
# Vamos criar um Score de Recomendação = Média(Score_Dim1, Score_Dim2)

df_ativa['Score_Decisao'] = (df_ativa['Score_Dim1'] + df_ativa['Score_Dim2']) / 2
recommended_startup = df_ativa.loc[df_ativa['Score_Decisao'].idxmax()]

print("Recomendação de Investimento:")
print(f"ID: {recommended_startup['id_startup']}")
print(f"Nome: {recommended_startup['nome_startup']}")
print(f"Justificativa:")
print(f"- Score Grupo 1 (Técnico - Dim 1): {recommended_startup['Score_Dim1']:.2f}")
print(f"- Score Grupo 2 (Econômico - Dim 2): {recommended_startup['Score_Dim2']:.2f}")
print(f"- Média (Equilíbrio): {recommended_startup['Score_Decisao']:.2f}")
print(f"- Score Global: {recommended_startup['Score_Global']:.2f}")
