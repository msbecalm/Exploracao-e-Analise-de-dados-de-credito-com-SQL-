
# Exploração e Análise de dados de crédito com SQL

**Descrição dos dados:**

A amostra de dados utilizada contém informações de clientes de um banco e possui as seguintes colunas:

- idade = idade do cliente
- sexo = sexo do cliente (F ou M)
- dependentes = número de dependentes do cliente
- escolaridade = nível de escolaridade do cliente
- salario_anual = faixa salarial do cliente
- tipo_cartao = tipo de cartão do cliente
- qtd_produtos = quantidade de produtos comprados nos últimos 12 meses
- iteracoes_12m = quantidade de iterações/transações nos últimos 12 meses
- meses_inativo_12m = quantidade de meses que o cliente ficou inativo
- limite_credito = limite de credito do cliente
- valor_transacoes_12m = valor das transações dos últimos 12 meses
- qtd_transacoes_12m = quantidade de transações dos últimos 12 meses

Para essa exploração de dados, foi utilizada uma amostra dos dados disponibilizados em: [https://github.com/andre-marcos-perez/ebac-course-utils/tree/main/dataset](https://github.com/andre-marcos-perez/ebac-course-utils/tree/main/dataset)

O dataset mencionado no link acima possui aproximadamente 10.000 linhas. Sabe-se que quanto maior a quantidade de dados utilizada, maior é a probabilidade de que a análise seja confiável. No entanto, o processamento de um volume maior de dados pode implicar em maiores custos financeiros. Por esse motivo, em contextos reais de análise de dados, a utilização de uma amostra pode ser uma alternativa interessante. 

Partindo dessa ideia, foi extraída uma amostra aleatória do dataset acima. A utilização de uma amostra aleatória é importante para minimizar o viés de seleção e se certificar de que o conjunto de dados escolhido para análise é similar aos dados completos, partindo-se do pressuposto de que cada indivíduo que compõe os dados terá chance igual de ser selecionado para fazer parte da amostra. Para isso, foi feito o upload de um arquivo .csv contendo todos os dados para o [SQLite](https://sqliteonline.com/) e foi executada a seguinte query:
"""

SELECT * FROM credito_full
ORDER BY RANDOM()
LIMIT 2500

"""A partir dos dados resultantes dessa query, foi criada uma tabela no **AWS Athena** junto com o **S3 Bucket**.

# Conhecendo os dados

**Qual é o tamanho da amostra utilizada, em termos de quantidade de linhas?**
"""

SELECT COUNT(*) from credito

"""> R: 2500

Nesse caso, como o tamanho da amostra já havia sido definido previamente, o número de linhas já era conhecido. Mas em outros contextos de análise, pode ser interessante entender primeiro o tamanho da amostra.

**Quais são as informações contidas em cada coluna?**
"""

SELECT * FROM credito limit 10;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(2).png?raw=true">

**Quais são os tipos de dado em cada coluna?**
"""

DESCRIBE credito;

"""<img src="http://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(1).png?raw=true">

**Quais são as categorias presentes na coluna escolaridade?**
"""

SELECT DISTINCT escolaridade from credito;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(3).png?raw=true">

> é possível identificar que na coluna escolaridade existem valores nulos (”na”) que precisarão ser tratados no momento da análise.

**Quais são as categorias presentes na coluna estado_civil?**
"""

SELECT DISTINCT estado_civil from credito;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(4).png?raw=true">

> Na coluna estado_civil também existem valores nulos (”na”) que precisarão ser tratados.

**Quais são as categorias presentes na coluna salario_anual?**
"""

SELECT DISTINCT salario_anual from credito;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(5).png?raw=true">

> Os dados contém apenas informações sobre a faixa salarial, mas não o valor exato do salário do cliente. Também contém dados nulos (”na”) que precisarão ser tratados.

**Na coluna tipo_cartao, quais são as categorias disponíveis?**
"""

SELECT DISTINCT tipo_cartao from credito;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(24).png?raw=true">

# Análise de dados

Após entender melhor quais são as categorias de dados existentes em cada coluna, é possível iniciar a análise.

**Na amostra em análise, quantos clientes existem em cada faixa salarial?**
"""

SELECT COUNT (*), salario_anual FROM credito GROUP BY salario_anual;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(6).png?raw=true">

> Os dados retornados podem ser representados a partir do gráfico abaixo. É possível identificar que a faixa salarial que possui a maior quantidade de pessoas é a "menos que $40K".

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(7).png?raw=true">

**Quantos clientes são homens e quantos são mulheres?**
"""

SELECT COUNT(*), sexo FROM credito GROUP BY sexo;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(8).png?raw=true">

> Na amostra analisada, a quantidade de homens e mulheres é aproximadamente igual.

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(9).png?raw=true">

**Em cada faixa salarial, qual é a quantidade de homens e mulheres?**
"""

SELECT COUNT (*), salario_anual, sexo  FROM credito_part_semvirgula_ccabecalho
WHERE salario_anual != 'na'
GROUP BY salario_anual, sexo;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(25).png?raw=true">

> Não se encontram pessoas do sexo feminino em faixas salariais acima de $60K. Na faixa salarial mais baixa ("menos que $40K"), **92,4%** das pessoas são do sexo feminino:

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(11).png?raw=true">

**Qual a idade mínima, máxima e média por sexo?**
"""

SELECT ROUND(AVG(idade),0) AS media_idade, MIN(idade) AS min_idade, MAX(idade) AS max_idade, sexo FROM credito GROUP BY sexo;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(12).png?raw=true">

> Em relação a idade, é possível identificar que a idade mínima, média e máxima para o sexo feminino e masculino são aproximadamente iguais.

**Qual o menor e o maior valor de transação?**
"""

SELECT MIN(valor_transacoes_12m) AS transacao_minima, MAX(valor_transacoes_12m) AS transacao_maxima FROM credito;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(13).png?raw=true">

**Quais as características dos clientes que possuem os valores de crédito mais elevados?**
"""

SELECT MAX(limite_credito) AS limite_credito, escolaridade, tipo_cartao, sexo FROM credito 
WHERE escolaridade != 'na' AND tipo_cartao != 'na' 
GROUP BY escolaridade, tipo_cartao, sexo ORDER BY limite_credito DESC LIMIT 10;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(14).png?raw=true">

> Para a amostra analisada, entre as 10 pessoas com o maior valor de limite de crédito, existe apenas 1 mulher para 9 homens. No que diz respeito à escolaridade, não é possível estabelecer relação entre escolaridade e valor de crédito, visto que entre os clientes com o maior valor de crédito, é possível encontrar pessoas com diferentes níveis de escolarização.

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(15).png?raw=true">

**Quais as características dos clientes que possuem os menores valores de crédito?**
"""

SELECT MIN(limite_credito) AS limite_credito, escolaridade, tipo_cartao, sexo FROM credito 
WHERE escolaridade != 'na' AND tipo_cartao != 'na' 
GROUP BY escolaridade, tipo_cartao, sexo 
ORDER BY limite_credito ASC LIMIT 10;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(16).png?raw=true">

> Entre as 10 pessoas com o menor valor de limite de crédito, 50% são mulheres e 50% são homens. Assim como no exemplo anterior, a escolaridade não parece ter relação com o valor de crédito.

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(17).png?raw=true">

**Existe diferença na média de gastos em relação ao sexo?**
"""

SELECT MAX(valor_transacoes_12m) AS maior_valor_gasto, AVG(valor_transacoes_12m) AS media_valor_gasto, MIN(valor_transacoes_12m) AS min_valor_gasto, sexo 
FROM credito 
GROUP BY sexo;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(18).png?raw=true">

> Não é possível identificar diferenças significativas na média de gastos em relação ao sexo.

**Existe diferença na média de gastos em relação ao estado civil?**
"""

SELECT AVG(valor_transacoes_12m) AS media_gastos, estado_civil FROM credito
WHERE estado_civil != 'na'
GROUP BY estado_civil;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(19).png?raw=true">

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(20).png?raw=true">

> Não é possível identificar diferenças significativas na média de gastos em relação ao estado civil.

**Existe diferença na média de gastos em relação a quantidade de dependentes?**
"""

SELECT AVG(valor_transacoes_12m) AS media_gastos, dependentes FROM credito
GROUP BY dependentes;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(21).png?raw=true">

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(22).png?raw=true">

> Não é possível identificar diferenças significativas na média de gastos em relação a quantidade de dependentes.

**É possível que exista alguma relação entre média de quantidade de produtos, média de gastos, faixa salarial e gênero?**
"""

SELECT AVG(qtd_produtos) AS qts_produtos, AVG(valor_transacoes_12m) AS media_valor_transacoes, AVG(limite_credito) AS media_limite, sexo, salario_anual
FROM credito
WHERE salario_anual != 'na'
GROUP BY sexo, salario_anual
ORDER BY AVG(valor_transacoes_12m) DESC;

"""<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(26).png?raw=true">

<img src="https://github.com/msbecalm/Exploracao-e-Analise-de-dados-de-credito-com-SQL-/blob/main/Untitled%20(23).png?raw=true">

> Não é possível identificar diferenças significativas na média de gastos e na média de produtos consumidos entre as diferentes faixas salariais. A partir do gráfico também é possível identificar que não existem pessoas do sexo feminino em faixas salariais acima de <$60K>, algo que já foi identificado anteriormente.

Os gráficos apresentados podem ser encontrados no Dashboard: https://datastudio.google.com/reporting/722a6d34-c41d-4cc8-9c9e-1e6b81c532a0/page/2wt8C/edit

# Conclusões

Os dados da amostra selecionada indicam que a faixa salarial predominante é a de menos que $40K por ano e que quanto maior a faixa salarial, menor a quantidade de pessoas nesse grupo.

Além disso, a proporção entre pessoas do sexo feminino e masculino é equilibrada, sendo 48,6% do sexo masculino e 51,4% do sexo feminino.

Embora tal proporção seja equilibrada, é possível identificar que 92,4% das pessoas que se encontram na menor faixa salarial (menos que $40K por ano) são mulheres. Na segunda menor faixa salarial (40K a 60K), a proporção entre homens e mulheres é igual. No entanto, para as faixas salariais maiores (a partir de 60K), não se encontram pessoas do sexo feminino.

Em relação às pessoas que possuem o valor de crédito mais elevado, não é possível identificar relação entre valor de crédito e escolaridade, visto que para esse grupo, é possível encontrar uma distribuição relativamente uniforme de pessoas com diferentes níveis de escolarização. Em relação ao gênero, 90% das pessoas com maior valor de crédito são do sexo masculino. O fato de apenas 10% do grupo com maior valor de crédito serem mulheres se mostra coerente com o dado de que não se encontram pessoas do sexo feminino em faixas salariais maiores do que $60K. 

Para as pessoas que possuem o valor de crédito mais baixo, também não é possível estabelecer relação entre valor de crédito e escolaridade, pois é possível identificar uma distribuição uniforme de pessoas entre os diferentes níveis de escolaridade. Aliás, se observa que a quantidade de pessoas é exatamente a mesma, independente do nível de escolaridade. Em relação ao gênero, 50% das pessoas com maior valor de crédito são do sexo masculino e 50% das pessoas são do sexo feminino.

No que diz respeito à media de gastos, é possível identificar que a média de gastos para pessoas com menor faixa salarial é ligeiramente maior, quando comparado às demais faixas salariais. Os dados também não possibilitaram estabelecer uma relação proporcional entre faixa salarial e média de gastos e/ou faixa salarial e média de produtos consumidos. Além disso, o estado civil e a quantidade de dependentes também não parecem ser fatores que influenciam na média de gastos. Por fim, também não é possível identificar diferenças significativas na média de gastos e média de produtos consumidos entre pessoas do sexo feminino e masculino.
"""
