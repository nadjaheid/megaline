import pandas as pd 
import numpy as np 
from math import factorial 
from scipy import stats as st # Carregando todas as bibliotecas


# ## Carregue os dados

calls = pd.read_csv('/datasets/megaline_calls.csv')
internet = pd.read_csv('/datasets/megaline_internet.csv') 
messages = pd.read_csv('/datasets/megaline_messages.csv')
plans=pd.read_csv('/datasets/megaline_plans.csv')
users=pd.read_csv('/datasets/megaline_users.csv') # Carreguando os arquivos de dados em diferentes DataFrames


# ## Prepare os dados

# ## Planos

plans.info() # Imprimindo as informações gerais/resumidas sobre o DataFrame dos planos

amostra_planos = plans.head() # Imprimindo uma amostra de dados dos planos
print(amostra_planos)



# ## Usuários

users.info() # Imprima as informações gerais/resumidas sobre o DataFrame dos usuários
print()
print(users.isnull().sum())

amostra_usuarios = users.sample(5)# Imprima uma amostra de dados dos usuários
print(amostra_usuarios)


# O conjunto de dados possui 500 entradas (linhas) e 8 colunas.
# A maioria das colunas contém dados não nulos, com exceção da coluna "churn_date", que tem apenas 34 entradas não nulas, indicando a data em que o cliente cancelou o serviço.
# As colunas contêm tipos de dados variados, como int64 para dados numéricos e object para dados de texto (strings).
# Na amostra, a coluna "churn_date" tem valores NaN, indicando que esses clientes não cancelaram o serviço até a última data registrada.
# Como precisamos analisar os clientes ativos, vou excluir as linhas onde há registro de entrada na coluna churn_date.


# A coluna reg_date que representa da data de inscrição foi passada para dados tipo datetime64

users['reg_date'] = pd.to_datetime(users['reg_date'])


users.info()


# ### Enriqueça os dados
#Criei uma máscara booleana para retirar das observações a linhas onde os clientes não estavam ativos, ou seja, aqueles onde a coluna churn_date estava preenchida com a data de encerramento do contrato.

#users = users[~users['churn_date'].notna()]

# imprimindo as informações do dataframe users, para verificar se a exclusão dos clientes inativos fora bem sucedida.
users.info()


# ## Chamadas


calls.info() # Imprimindo as informações gerais/resumidas sobre o DataFrame das chamadas


amostra_chamadas=calls.sample(5) # Imprimindo uma amostra de dados das chamadas
print(amostra_chamadas)


# Não existem dados faltantes. É possível verificar que a coluna call_date não está no formato data e na amostra é possível verificar que a coluna duration não está no formato desejado pela empresa, que considera a duração das chamadas em valor inteiro e arredondado para cima. Sendo assim, é necessário transformar call_date em datetime64, arredondar para cima e transformar em int64 a coluna duration.

# ### Corrija os dados

# Transformando call_date em datetime64.


calls['call_date'] = pd.to_datetime(calls['call_date'])


# ### Enriqueça os dados

# Na variável duration, arredondando para cima e transformando para o formato em int64.


calls['duration'] = np.ceil(calls['duration'])
calls['duration'] = calls['duration'].astype('int64')
print(calls.sample(5))
print()
calls.info()


# ## Mensagens

messages.info() # Imprimindo as informações gerais/resumidas sobre o DataFrame das mensagens

mensagens_amostra = messages.sample(5) # Imprimindo uma amostra dos dados das mensagens
print(mensagens_amostra)


# Não existem dados faltantes, mas a variável message_date precisa ser transformada em datetime64.

# Transformando a variável message_date em datetime64.
messages['message_date'] = pd.to_datetime(messages['message_date'])
messages.info()

# ## Internet

internet.info() # Imprimindo as informações gerais/resumidas sobre o DataFrame da internet


internet_amostra=internet.sample(5)#  Imprimindo uma amostra de dados para o tráfego da internet
print(internet_amostra)


# Não existem dados faltantes. A coluna session_date pode ser passada para datetime64. A coluna mb_used será posteriormente arredondada, quando for feita a soma total mensal. 

# Coluna session_date sendo tranformada em dados dos tipo datetime64.

internet['session_date'] = pd.to_datetime(internet['session_date'])
internet.info()


# ## Estude as condições dos planos

# O plano Surf possue um pacote de dados, mensagens e minutos menor, sendo mais barato que o plano Ultimate, que possui um pacote maior de dados. Entretanto, quando o cliente ultrapassa o limite de uso contratado, pagará mais caro por cada produto utilizado adicionalmente no pacote surf do que no pacote Ultimate. 

print(plans.head()) # Imprimindo as condições do plano 


# ## Agregue os dados por usuário
# 
# [Agora, como os dados estão limpos, agregue os dados por usuário por período para ter apenas um registro por usuário por período. Isso vai facilitar muito a análise posterior.]

# Calculando o número de chamadas feitas por cada usuário por mês e salvando o resultado.
#Adicionando uma coluna de mês
calls['month'] = calls['call_date'].dt.to_period('M') 

# Calculando a quantidade de chamadas feitas por usuário por mês
chamadas_por_mes = calls.groupby(['user_id', 'month']).size().reset_index(name='num_calls')

# Exibindo o resultado
print(chamadas_por_mes)

# Salvando o resultado
chamadas_por_mes.to_csv('chamadas_por_mes.csv', index=False)

# Calculando a quantidade de minutos gastos por cada usuário por mês e salvando o resultado.

#Adicionando uma coluna de mês
calls['month'] = calls['call_date'].dt.to_period('M')

# Calculando a quantidade de minutos gastos por usuário por mês
min_mes = calls.groupby(['user_id', 'month'])['duration'].sum().reset_index(name='total_min')

# Exibindo o resultado
print(min_mes)

# Salvando o resultado
min_mes.to_csv('min_mes.csv', index=False)

# Calculando o número de mensagens enviadas por cada usuário por mês e salvando o resultado.

# Adicionando uma coluna de mês
messages['month'] = messages['message_date'].dt.to_period('M')

# Calculando o número de mensagens por usuário por mês
sms_por_mes = messages.groupby(['user_id', 'month']).size().reset_index(name='num_sms')

# Exibindo o resultado
print(sms_por_mes)

# Salvando o resultado
sms_por_mes.to_csv('sms_por_mes.csv', index=False)

# Calculando o volume de tráfego de internet usado por cada usuário por mês e salvando o resultado.

# Adicionando uma coluna de mês
internet['month'] = pd.to_datetime(internet['session_date']).dt.to_period('M')

# Calculando o volume de tráfego por usuário por mês
trafego_mensal = internet.groupby(['user_id', 'month'])['mb_used'].sum().reset_index(name='trafego_mb')

# Arredondando o valor do tráfego mensal para cima e transformando em int64, conforme instrução inicial
trafego_mensal['trafego_mb'] = np.ceil(trafego_mensal['trafego_mb'])
trafego_mensal['trafego_mb'] = trafego_mensal['trafego_mb'].astype('int64')

# Exibindo o resultado
print(trafego_mensal)

# Salvando o resultado
trafego_mensal.to_csv('trafego_mensal.csv', index=False)


# Dados agregados em um DataFrame para que um registro nele represente o que um usuário unívoco consumiu em um determinado mês.

# Juntando os dados de chamadas, minutos, mensagens e internet com base em user_id e month
# Usei a função merge
merged_data = pd.merge(chamadas_por_mes, min_mes, on=['user_id', 'month'], how='outer')
merged_data = pd.merge(merged_data, sms_por_mes, on=['user_id', 'month'], how='outer')
merged_data = pd.merge(merged_data, trafego_mensal, on=['user_id', 'month'], how='outer')

#juntei a coluna plan, para saber qual o plano de cada usuário
merged_data = pd.merge(merged_data, users[['user_id', 'plan']], on='user_id', how='left')

# Mostrando o novo dataframe
print(merged_data)

# Salvando o resultado
merged_data.to_csv('merged_data.csv', index=False)
merged_data.info()
plans.info()

# Adicionando as informações sobre o plano


# Mesclando as informações do plano com base na coluna 'plan'
merged_data = pd.merge(merged_data, plans[['plan_name', 'minutes_included', 'messages_included', 'mb_per_month_included', 
                                           'usd_per_minute', 'usd_per_message', 'usd_per_gb', 'usd_monthly_pay']], 
                       left_on='plan', right_on='plan_name', how='left')

# Mostrando como ficou essa junção
print(merged_data)

# Salvando o resultado
merged_data.to_csv('merged_data.csv', index=False)

print(merged_data.isnull().sum())


# Juntei todas as informações necessárias à análise dos gastos mensais de cada usuário em um único dataframe, usando o comando merge. Neste dataframe estáo contidos os total de minutos das chamadas, o total de sms enviados, o total de tráfego de internet em Mb, bem como as informações de cada plano, conforme cada usuário contratou.
# Como algumas células apresentam valor NaN, é preciso substituir por 0, para não dar erro no momento de calcular a receita.

# Preencher NaN com 0 antes de calcular a receita
merged_data.fillna(0, inplace=True)


# Cálculo da receita mensal para cada usuário. Quando a diferença entre o uso do cliente e o contratado for positivo,
# será cobrada a taxa adicional do plano mais a mensalidade, caso contrário, será cobrada apenas a mensalidade.
merged_data['revenue'] = (
    (np.maximum(merged_data['total_min'] - merged_data['minutes_included'], 0) * merged_data['usd_per_minute']) +
    (np.maximum(merged_data['num_sms'] - merged_data['messages_included'], 0) * merged_data['usd_per_message']) +
    (np.maximum((merged_data['trafego_mb'] - merged_data['mb_per_month_included']) / 1024, 0) * merged_data['usd_per_gb']) +
    merged_data['usd_monthly_pay']
)

# Exibindo o resultado
print(merged_data[['user_id', 'month', 'revenue']])

#imprimindo as estatística descritivas da coluna revenue

print(merged_data['revenue'].describe())


merged_data[merged_data['revenue'].isna()]


# ## Estude o comportamento do usuário

# 

# ### Chamadas


# Comparando a duração média das chamadas de cada plano para cada mês distinto. Criando um gráfico de barras para visualizá-lo.

import matplotlib.pyplot as plt
import seaborn as sns

# Calculando a duração média das chamadas para cada plano e mês
duracao_media_por_plano = merged_data[merged_data['plan'] != 0].groupby(['plan', 'month'])['total_min'].mean().reset_index()

# Criando um gráfico de barras
plt.figure(figsize=(12, 6))
sns.barplot(x='month', y='total_min', hue='plan', data=duracao_media_por_plano)
plt.title('Duração Média das Chamadas por Plano e Mês')
plt.xlabel('Mês')
plt.ylabel('Duração Média das Chamadas (minutos)')
plt.legend(title='Plano')
plt.show()



# Comparando o número de minutos de que os usuários de cada plano necessitam a cada mês. Construindo um histograma.

# Calculando o número total de minutos por plano e mês
total_minutes_por_plano = merged_data[merged_data['plan'] != 0].groupby(['plan', 'month'])['total_min'].sum().reset_index()

# Criando um histograma
plt.figure(figsize=(10, 6))
for plano in total_minutes_por_plano['plan'].unique():
    dados_plano = total_minutes_por_plano[total_minutes_por_plano['plan'] == plano]
    plt.hist(dados_plano['total_min'], bins=30, alpha=0.7, label=plano)

plt.title('Distribuição do Número de Minutos por Plano e Mês')
plt.xlabel('Número Total de Minutos')
plt.ylabel('Frequência')
plt.legend()
plt.show()


# Ao criar este histograma, notei que pode haver a presença de outliers, assim, fiz um gráfico de boxplot
# Confirmando minha suspeita, removi os outliers e criei um novo histograma, que ficou bem mais aprazível
# Também filtrei as entradas onde plan estava zero, para não criar um terceiro gráfico.

# Filtrar entradas onde o plano não é 0
merged_data_filtered = merged_data[merged_data['plan'] != 0]

# Criação um boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='plan', y='total_min', data=merged_data_filtered)
plt.title('Boxplot do Número de Minutos por Plano')
plt.xlabel('Plano')
plt.ylabel('Número Total de Minutos')
plt.show()

# Identificando os limites superior e inferior usando o método IQR
Q1 = merged_data_filtered['total_min'].quantile(0.25)
Q3 = merged_data_filtered['total_min'].quantile(0.75)
IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Removendo os outliers
merged_data_no_outliers = merged_data_filtered[(merged_data_filtered['total_min'] >= lower_limit) & (merged_data_filtered['total_min'] <= upper_limit)]

# Criando um histograma sem outliers
plt.figure(figsize=(10, 6))
sns.histplot(x='total_min', hue='plan', data=merged_data_no_outliers, bins=30, kde=True)
plt.title('Histograma do Número de Minutos por Plano (Sem Outliers)')
plt.xlabel('Número Total de Minutos')
plt.ylabel('Contagem')
plt.show()


# Calculando a média e a variável da duração da chamada para raciocinar se os usuários de diferentes planos possuem comportamentos diferentes em suas chamadas.


# Calculando a média e a variação da duração mensal das chamadas

# Agrupando por mês e tipo de plano, calculando a média e a variância da duração das chamadas
duration_stats = merged_data[merged_data['plan'] != 0].groupby(['month', 'plan'])['total_min'].agg(['mean', 'var']).reset_index()

# Exibindo os resultados
print(duration_stats)


# Fazendo um diagrama de caixa para visualizar a distribuição da duração mensal das chamadas

# Ordenando os meses de maneira crescente, pois a primeira vez que fiz o boxplot o eixo x ficou desordenado
order = merged_data['month'].sort_values().unique()

# Criando um boxplot com orientação vertical
plt.figure(figsize=(10, 6))
sns.boxplot(x='month', y='total_min', data=merged_data, orient='v', order=order)
plt.title('Distribuição da Duração Mensal das Chamadas')
plt.xlabel('Mês')
plt.ylabel('Duração Total (minutos)')
plt.xticks(rotation=45, ha='right')
plt.show()


# Aparentemente, os usuários do plano surf utilizam mais minutos de chamada no primeiro semestre do que os usuários do plano ultimate. Sendo que no segundo semestre ambos flutuam, de maneira levemente crescente, em torno dos 400 minutos, em média. A variância da média de chamadas do plano ultimate é ligeiramente maior do que do plano surf, levando a crer que os usuários do plano surf, usam em média, 400 minutos por mês, de maneira mais consistente.


# Filtrar entradas onde o plano não é 0
merged_data_filtered = merged_data[merged_data['plan'] != 0]

# Criar um gráfico de barras
plt.figure(figsize=(15, 7))
sns.barplot(x='month', y='num_sms', hue='plan', data=merged_data_filtered, order=order, edgecolor='black')
plt.title('Número de Mensagens Enviadas por Plano a Cada Mês')
plt.xlabel('Mês')
plt.ylabel('Número de Mensagens')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Plano')
plt.show()

# Criar um boxplot
plt.figure(figsize=(20, 7))
sns.boxplot(x='month', y='num_sms', hue='plan', data=merged_data_filtered, order=order)
plt.title('Distribuição do Número de Mensagens por Plano a Cada Mês')
plt.xlabel('Mês')
plt.ylabel('Número de Mensagens')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Plano')
plt.show()


# calculando a média e a variância da variável mensagens
sms_stats = merged_data[merged_data['plan'] != 0].groupby(['month', 'plan'])['num_sms'].agg(['mean', 'var']).reset_index()

# Exibindo os resultados
print(sms_stats)



# Com relação às mensagens, os usuários do plano ultimate tendem a trocar, em média, mais mensagens do que os usuários do plano surf. Mesmo que de maneira crescente para ambos ao longo do segundo semestre.

# ### Internet

# Filtrar entradas onde o plano não é 0
merged_data_filtered = merged_data[merged_data['plan'] != 0]

# Criar um gráfico de barras
plt.figure(figsize=(15, 8))
sns.barplot(x='month', y='trafego_mb', hue='plan', data=merged_data_filtered, order=order)
plt.title('Quantidade de Tráfego de Internet por Plano a Cada Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Tráfego (MB)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Plano')
plt.show()


plt.figure(figsize=(15, 8))
sns.boxplot(x='month', y='trafego_mb', hue='plan', data=merged_data_filtered, order=order)
plt.title('Distribuição do Tráfego de Internet por Plano a Cada Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Tráfego (MB)')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Plano')
plt.show()

# calculando a média e a variância da variável internet
internet_stats = merged_data[merged_data['plan'] != 0].groupby(['month', 'plan'])['trafego_mb'].agg(['mean', 'var']).reset_index()

# Exibindo os resultados
print(internet_stats)


# Os usuários de ambos os planos tendem a usar mais tráfego de internet no segundo semestre. Entretanto, os usuários do plano ultimate tendem a usar mais internet durante todo o ano. Percebe-se que no mês de janeiro, ambos os usuários reduzem drasticamente o uso de internet.

# ## Receita

# Como se pode ver nas estatística abaixo, os adeptos do plano ultimate estão concentrados na receita de 70, não consumindo além da franquia do plano (75 por cento dos usuários pagam apenas a mensalidade e a média se aproxima da mediana). No plano surf, apesar de alguns clientes oferecerem uma receita muito alta, por ultrapassarem os limites do plano, a variabilidade é bem maior, sendo a média superior à mediana (57 contra 37). 


estatisticas = merged_data[merged_data['plan'] != 0].groupby('plan')['revenue'].describe()
print(estatisticas)


# Passo 2: Identifique os limites superior e inferior usando o método IQR
Q1 = merged_data['revenue'].quantile(0.25)
Q3 = merged_data['revenue'].quantile(0.75)
IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Passo 3: Remova os outliers
merged_data_no_outliers = merged_data_filtered[(merged_data_filtered['revenue'] >= lower_limit) & (merged_data_filtered['revenue'] <= upper_limit)]

# Histograma sem outliers
plt.figure(figsize=(12, 6))
sns.histplot(data=merged_data_no_outliers, x='revenue', hue='plan', bins=30, kde=True)
plt.title('Histograma da Receita Mensal por Plano (Sem Outliers)')
plt.xlabel('Receita Mensal (USD)')
plt.ylabel('Frequência')
plt.legend(title='Plano', labels=['surf', 'ultimate'])
plt.show()


# Boxplot sem outliers
plt.figure(figsize=(12, 6))
sns.boxplot(x='plan', y='revenue', data=merged_data_no_outliers)
plt.title('Boxplot da Receita Mensal por Plano (Sem Outliers)')
plt.xlabel('Plano')
plt.ylabel('Receita Mensal (USD)')
plt.show()


# Apesar dos clientes da conta ultimate não costumarem ultrapassar os limites do plano, não oferencendo receitas adicionais à operadora, existe uma concentração de receita a partir de 70 por usuário. No plano surf, mesmo que alguns clientes ultrapassem em muito os seus planos de dados e acabem por pagar mais do que se estivessem no plano Ultimate, estão muito mais concentrados em torno da sua mensalidade de 20. 

# ## Teste hipóteses estatísticas

# Abaixo , testa-se a hipótese de que as receitas médias dos usuários dos planos de chamadas Ultimate e Surf são diferentes.
# 
# Hipótese Nula (H0): As receitas médias dos usuários dos planos de chamadas Ultimate e Surf são iguais.
# 
# Hipótese Alternativa (H1): As receitas médias dos usuários dos planos de chamadas Ultimate e Surf são diferentes.
# 
# Teste Estatístico: Teste t de Student para duas amostras independentes.
# 
# α = 0.05

# Como o p-valor é menor do que 0.05, podemos rejeitar a hipótese nula. Isso sugere que há evidências suficientes para afirmar que a receita média dos usuários dos planos Ultimate e Surf é estatisticamente diferente.

# Teste as hipóteses
# Separando os dados
revenue_surf = merged_data.loc[merged_data['plan_name'] == 'surf', 'revenue']
revenue_ultimate = merged_data.loc[merged_data['plan_name'] == 'ultimate', 'revenue']

# Realizar teste de igualdade de variâncias (Bartlett's Test)
bartlett_test = st.bartlett(revenue_surf, revenue_ultimate)

# Verificar o resultado do teste de igualdade de variâncias
if bartlett_test.pvalue > 0.05:
    equal_var = True
    print("Variâncias iguais (p-value =", bartlett_test.pvalue, ")")
else:
    equal_var = False
    print("Variâncias diferentes (p-value =", bartlett_test.pvalue, ")")

# Realizar teste t de Student para amostras independentes
results = st.ttest_ind(revenue_surf, revenue_ultimate, equal_var=False)

# Exibir o valor-p
print('p-value:', results.pvalue)


# Testando abaixo a hipótese de que a receita média dos usuários da área de NY-NJ difere dos usuários das demais regiões.
# 
# H0: A receita média dos usuários da área de NY-NJ é igual à receita média dos usuários de outras regiões.
# 
# H1: A receita média dos usuários da área de NY-NJ difere da receita média dos usuários de outras regiões.
# 
# α = 0.05

# Os resultados indicam que o teste de igualdade de variâncias (Bartlett's Test) sugere que as variâncias das receitas entre os usuários da área de NY-NJ e os usuários de outras regiões são diferentes(p-value = 0.0103).
# 
# No entanto, o teste t de Student para amostras independentes (com igualdade de variâncias) não mostra evidências suficientes para rejeitar a hipótese nula de que as médias das receitas são iguais (p-value = 0.988).
# 
# Isso significa que, apesar de as variâncias serem diferentes, não há evidências estatísticas significativas para sugerir que as médias das receitas dos usuários da área de NY-NJ diferem dos usuários de outras regiões. Nesse caso, não há motivos para rejeitar a hipótese nula de igualdade das médias.


# Teste as hipóteses

merged_data = pd.merge(merged_data, users[['user_id', 'city']], on='user_id', how='left')

# Criando as amostras
revenue_ny_nj = merged_data.loc[merged_data['city'] == 'New York-Newark-Jersey City, NY-NJ-PA MSA', 'revenue']
revenue_other = merged_data.loc[merged_data['city'] != 'New York-Newark-Jersey City, NY-NJ-PA MSA', 'revenue']

# Realizar teste de igualdade de variâncias (Bartlett's Test)
bartlett_test = st.bartlett(revenue_ny_nj, revenue_other)

# Verificar o resultado do teste de igualdade de variâncias
if bartlett_test.pvalue > 0.05:
    equal_var = True
    print("Variâncias iguais (p-value =", bartlett_test.pvalue, ")")
else:
    equal_var = False
    print("Variâncias diferentes (p-value =", bartlett_test.pvalue, ")")


# Teste t de amostras independentes
results = st.ttest_ind(revenue_ny_nj, revenue_other, equal_var=False)

print('p-value:', results.pvalue)


# ## Conclusão geral
# 
# 

# Uso de Minutos de Chamada:
# 
# Usuários do plano Surf utilizam mais minutos de chamada no primeiro semestre do ano, enquanto ambos os planos flutuam em torno de 400 minutos no segundo semestre.
# A variância da média de chamadas do plano Ultimate é ligeiramente maior, sugerindo que os usuários do plano Surf utilizam, em média, 400 minutos de forma mais consistente.
# 
# Mensagens:
# Usuários do plano Ultimate tendem a trocar mais mensagens em média do que os usuários do plano Surf, com ambas as tendências aumentando ao longo do segundo semestre.
# 
# Tráfego de Internet:
# Ambos os usuários de Surf e Ultimate tendem a usar mais tráfego de internet no segundo semestre, mas os usuários do plano Ultimate utilizam mais internet ao longo do ano.
# 
# Receita:
# No plano Ultimate, a concentração de usuários está na faixa de receita em torno de 70, onde a maioria dos usuários paga apenas a mensalidade.
# No plano Surf, há maior variabilidade na receita, alguns clientes oferecem receita alta ao ultrapassarem os limites do plano.

# Considerando o resultado do teste de hipótese para revenue_surf e revenue_ultimate, que forneceu um valor-p extremamente baixo (p-value: 1.1557348711590938e-21), indica evidências estatísticas suficientes para rejeitar a hipótese nula de que as médias são iguais. Além disso, a observação de variâncias diferentes (p-value = 3.6246061077063376e-296) sugere que as variâncias das duas amostras são estatisticamente diferentes. Entretanto, apesar de as variâncias serem diferentes, não há evidências estatísticas significativas para sugerir que as médias das receitas dos usuários da área de NY-NJ diferem dos usuários de outras regiões
# 
# Recomendações para Publicidade:
# Plano Surf: Dada a variabilidade na receita e a possibilidade de alguns clientes contribuírem com receitas mais altas, a publicidade pode destacar a flexibilidade do plano e os benefícios adicionais ao ultrapassar os limites.
# Plano Ultimate: A concentração de usuários na faixa de $70 sugere que a maioria paga apenas a mensalidade. A publicidade pode enfatizar a estabilidade na receita e os benefícios do plano, como troca de mensagens e uso frequente de internet.
# 
# Portanto, a recomendação seria focar mais na publicidade para o Plano Surf, explorando sua variabilidade e os potenciais ganhos adicionais, enquanto mantendo uma estratégia consistente para o Plano Ultimate, destacando os benefícios do plano e a estabilidade na receita em torno de $70.
