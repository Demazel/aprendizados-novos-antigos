# Documentação do Projeto: Análise de Dados MovieLens (data_release)

Este arquivo responde aos itens descritos no "Passo 11 - Montar o Dashboard" conforme as instruções, documentando os insights principais extraídos dos dados e descrevendo o projeto em formato textual, uma vez que a criação visual do dashboard não foi requerida.

## 1. Visualizações Incluídas (Resultados da Análise)

### 1.1 Evolução de Ratings ao Longo do Tempo
A análise temporal mostrou o volume de avaliações agregadas mensalmente (`year_month`). Há flutuações, indicando engajamento consistente ao longo dos anos registrados na base. Em meses de pico recentes (como abril de 2024), observamos volumes acima de 30.000 avaliações por mês.

### 1.2 Ranking de Filmes
Foram criadas duas óticas principais para o ranking:

**Top 5 Filmes Mais Populares (Maior volume de avaliações):**
1. The Shawshank Redemption (1994)
2. The Matrix (1999)
3. Inception (2010)
4. The Dark Knight (2008)
5. Fight Club (1999)

**Top 5 Filmes com Melhor Avaliação (Qualidade - Mín. 100 avaliações):**
1. The Shawshank Redemption (1994) - Nota: 4.10
2. Dune: Part Two (2024) - Nota: 4.09
3. Pulp Fiction (1994) - Nota: 4.09
4. Parasite (2019) - Nota: 4.07
5. Fight Club (1999) - Nota: 4.06

### 1.3 Atividade de Usuários
Os usuários mostram níveis muito distintos de engajamento na plataforma:
- **Média de avaliações por usuário:** 463.13
- **Mediana de avaliações por usuário:** 147 (indicando que a maior parte dos usuários avalia muito menos que a média, que é puxada para cima por heavy-users)
- **Máximo de avaliações de um único usuário:** 48.127 (um heavy-user extremo)

### 1.4 Análise por Gênero
Agrupando as avaliações pelos gêneros dos filmes, os mais consumidos e suas notas médias são:
1. **Drama**: 822.886 avaliações (Nota média: 3.13)
2. **Comedy**: 654.323 avaliações (Nota média: 2.87)
3. **Action**: 571.475 avaliações (Nota média: 3.04)
4. **Thriller**: 507.934 avaliações (Nota média: 3.10)
5. **Adventure**: 450.897 avaliações (Nota média: 3.08)
*(Observação: Gêneros como Crime possuem menos volume, mas notas médias significativamente maiores, como 3.23)*

### 1.5 Heatmap de Atividade
A distribuição de avaliações por dia da semana e hora do dia nos monstra o padrão de comportamento de uso:
- A segunda-feira costuma ter, de madrugada (ex: 0h), um volume de atividade (10.073 avaliações na amostra) consideravelmente superior aos mesmos horários da sexta-feira (7.223), sinalizando possível engajamento residual do fim de semana expandindo para o início da semana.

### 1.6 Scatter de Popularidade vs Qualidade
Há uma correlação de Pearson positiva fraca a moderada: **0.2273**.
Isso indica que **popularidade e qualidade tendem a subir juntas**, mas não garantem uma proporção direta perfeita. Filmes muito conhecidos tendem a agradar uma audiência ampla, enquanto filmes obscuros podem ter variância alta (love-it-or-hate-it).

## 2. Documentação do Projeto

### 2.1 Arquitetura do Pipeline
1. **Origem dos Dados:** Foram ingeridos os arquivos CSV fornecidos nativamente no diretório `data_release`:
   - `movies.csv`: Dicionário contendo dados categóricos dos filmes (`movieId`, `title`, `genres`).
   - `user_rating_history.csv`: Tabela fatos com todas as avaliações dos usuários (`userId`, `movieId`, `rating`, `tstamp`).
2. **Transformação e Processamento (ETL):** Foi desenvolvido um script Python (`analyze.py`) utilizando a biblioteca Pandas para tratar os dados de timestamp, gerar as quebras de data/hora (mês, dia da semana, hora) cruciais para dados de atividade e cruzar bases.
3. **Agregação:** Realizar as contagens quantitativas (`count`, `mean`, `size`) para responder às métricas de negócio listadas no painel.

### 2.2 Passos de Execução
1. Carregamento dos dataframes brutos usando Pandas (`pd.read_csv`).
2. Formatação da coluna transacional `tstamp` para formato DateTime nativo do Python (para os cálculos de cronologia e mapas de calor).
3. Separação de datas em metadados (`year_month`, `day_of_week`, `hour`).
4. Extração de múltiplos gêneros (um filme tem `Action|Adventure`) separando-os via função `str.split()` do Pandas + `.explode()` para não poluir o agrupamento.
5. Agrupamento (GroupBy) a nível User (para atividade), MovieId (para popularidade/qualidade) e Temporal/Gênero. E também uso de Crosstab para a matriz dimensional.

### 2.3 Queries Principais
O modelo equivalente em SQL / Pandas das operações essenciais extraídas pelo pipeline analítico:
- **Evolução de Ratings:** `SELECT FORMAT(tstamp, 'YYYY-MM'), COUNT(*) FROM ratings GROUP BY 1` (*pd.groupby('year_month').size()*)
- **Ranking / Popularidade:** `SELECT movieId, AVG(rating), COUNT(rating) FROM ratings GROUP BY movieId`
- **Atividade User:** `SELECT userId, COUNT(*) FROM ratings GROUP BY userId`
- **Análise Gênero:** Join entre `movies` e `ratings` com explode, `GROUP BY genero`.
- **Scatter (Pearson):** `corr()` no Pandas nas agregações de avaliação (contagem de avaliações e média delas por ID do filme).

### 2.4 Prints do Dashboard
Conforme os requerimentos da solicitação, "Não é necessário fazer um dashboard", logo não há prints fidedignos em anexo. Como alternativa, imagine a transposição dos dados sumarizados da "Seção 1" do documento na seguinte disposição num BI:
- *Topo*: Cartões (Scorecards) listando métricas consolidadas (Total de Usuários, Média de Ratings por Usuário = 463).
- *Centro / Superior*: Gráfico de linhas apontando os ratings mês a mês, permitindo entender a tração de engajamento ao longo do tempo.
- *Lateral*: Gráfico de barras horizontais rankeando filmes; Scatterplot evidenciando a concentração dos filmes em relação a quantidade X nota (Média = Eixo Y, Volumetria = Eixo X).
- *Fundo*: Heatmap clássico 7x24 que cruza dia da semana com a hora (cores fortes nas madrugadas de domingo para segunda).
