# 5ª Atividade - Histograma
**Universidade Federal do Piauí – UFPI**  
**Campus Senador Helvídio Nunes de Barros – Picos**  
**Curso:** Sistemas de Informação | **Período:** 6° | **Ano/Semestre:** 2026.2  
**Disciplina:** Tópicos Especiais em Visão Computacional  
**Professor:** Me. José Denes Lima Araújo  
**Aluno:** João Marcos Sousa Rufino Leal  

---

## 1. Fundamentação Teórica e Respostas das Questões

### Questão 1) Selecione uma imagem (ou mais) e aplique as seguintes transformações:
* **a) Calcule o histograma utilizando a fórmula correspondente e apresente o gráfico resultante.**
* **b) Normalize o histograma utilizando a fórmula correspondente e apresente o gráfico resultante.**
* **c) Aplique a equalização do histograma utilizando a fórmula. Mostre a imagem original juntamente com o gráfico do seu histograma normalizado. Adicionalmente, mostre a imagem após a equalização e seu histograma correspondente.**

---

#### 1.a) Histograma de uma Imagem Digital
O histograma de uma imagem digital com níveis de cinza no intervalo $[0, L-1]$ (onde tipicamente $L = 256$ para imagens de 8 bits) é uma função discreta que representa a frequência de ocorrência de cada intensidade luminosa na imagem.

**Fórmula matemática:**
$$h(r_k) = n_k$$

Onde:
- $r_k$: é o $k$-ésimo nível de intensidade de cinza ($r_0 = 0, r_1 = 1, \dots, r_{L-1} = L-1$).
- $n_k$: é a quantidade exata de pixels na imagem que possuem nível de intensidade igual a $r_k$.
- $k \in \{0, 1, \dots, L-1\}$.

**Interpretação:**
O gráfico do histograma absoluto plota no eixo das abscissas (horizontal) os valores possíveis de intensidade de cinza (0 a 255) e no eixo das ordenadas (vertical) o total absoluto de pixels ($n_k$) que assumem cada nível. Picos no gráfico revelam tonalidades predominantes na cena (e.g., picos próximos a zero indicam imagens escuras / subexpostas, enquanto picos próximos a 255 indicam imagens claras / superexpostas).

---

#### 1.b) Histograma Normalizado
O histograma normalizado expressa a distribuição de intensidades na forma de uma estimativa da probabilidade de ocorrência de cada nível de cinza, tornando a representação invariante à resolução da imagem.

**Fórmula matemática:**
$$p(r_k) = \frac{n_k}{M \times N}$$

Onde:
- $M \times N$: é a resolução espacial da imagem (número total de linhas vezes colunas, isto é, total de pixels).
- $p(r_k)$: é a probabilidade associada ao nível de intensidade $r_k$.

**Propriedades fundamentais:**
1. $0 \le p(r_k) \le 1$ para todo $k = 0, 1, \dots, L-1$.
2. $\sum_{k=0}^{L-1} p(r_k) = 1$ (a soma de todas as probabilidades é rigorosamente igual a $1,0$ ou $100\%$).

**Vantagem:**
O histograma normalizado permite comparar diretamente imagens com diferentes dimensões espaciais (resoluções) sob a mesma escala probabilística.

---

#### 1.c) Equalização de Histograma (*Histogram Equalization*)
A equalização de histograma é uma técnica de transformação pontual de contraste cujo objetivo é redistribuir as intensidades de cinza para aproximá-las de uma distribuição de probabilidade uniforme ao longo de toda a escala disponível $[0, L-1]$.

**Formulação matemática discreta:**
A transformação baseia-se na Função de Distribuição Acumulada (FDA / CDF - *Cumulative Distribution Function*):

$$s_k = T(r_k) = \text{round}\left( (L - 1) \sum_{j=0}^{k} p_r(r_j) \right) = \text{round}\left( \frac{L - 1}{M \times N} \sum_{j=0}^{k} n_j \right)$$

Onde:
- $r_k$: nível de cinza original do pixel de entrada.
- $s_k$: novo nível de intensidade mapeado após a equalização.
- $\sum_{j=0}^{k} p_r(r_j)$: soma acumulada das probabilidades até o nível $k$.
- $(L - 1)$: escala máxima de cinza ($255$ para imagens de 8 bits).
- $\text{round}(\cdot)$: operador de arredondamento para o número inteiro mais próximo no intervalo $[0, L-1]$.

**Efeitos visuais e analíticos:**
- Imagens que apresentavam baixo contraste (pixels concentrados em uma faixa estreita de cinza) passam a utilizar todo o espectro dinâmico $[0, 255]$.
- Detalhes ocultos em sombras profundas ou altas luzes tornam-se visíveis.
- O histograma resultante torna-se mais espalhado e espaçado, aumentando o contraste global automaticamente.

---

### Questão 2) Aplique a especificação do histograma utilizando a fórmula e mostre os seguintes itens:
* **a) Mostre a imagem de entrada, juntamente com o gráfico do seu histograma normalizado antes da especificação.**
* **b) Mostre a imagem de referência, juntamente com o gráfico do seu histograma normalizado.**
* **c) Mostre a imagem de entrada, juntamente com o gráfico do seu histograma normalizado após a especificação.**

---

#### 2. Fundamentação Teórica da Especificação de Histograma (*Histogram Matching*)
Enquanto a equalização gera um histograma aproximadamente uniforme de forma automática, existem cenários em que se deseja que uma imagem de entrada adquira o perfil específico de tonalidade e iluminação de uma imagem de referência. Essa técnica é chamada de **Especificação de Histograma** (*Histogram Specification* ou *Histogram Matching*).

#### Algoritmo Passo a Passo (Conforme ensinado em aula):

1. **Equalização da Imagem de Entrada ($r$):**
   Calcula-se o histograma normalizado $p_r(r_k)$ da imagem de entrada e obtém-se seus níveis equalizados discretos:
   $$s_k = T(r_k) = \text{round}\left( (L - 1) \sum_{j=0}^{k} p_r(r_j) \right), \quad k = 0, 1, \dots, L-1$$

2. **Equalização da Imagem de Referência ($z$):**
   Calcula-se o histograma normalizado $p_z(z_q)$ da imagem de referência e obtém-se seus níveis equalizados discretos:
   $$v_q = G(z_q) = \text{round}\left( (L - 1) \sum_{i=0}^{q} p_z(z_i) \right), \quad q = 0, 1, \dots, L-1$$

3. **Construção da Tabela de Mapeamento ($HE(r_k) \to z_q$):**
   Para cada intensidade equalizada da imagem de entrada ($s_k$), procura-se no vetor de intensidades equalizadas da referência ($v_q$) aquele valor mais próximo, e associa-se o valor original $z_q$ correspondente:
   $$\hat{z}_k = \arg\min_{z_q} |s_k - G(z_q)|$$
   *(Em caso de valores com mesma distância mínima, adota-se o menor índice $z_q$, preservando a monotonicidade).*

4. **Transformação da Imagem:**
   Cada pixel com intensidade original $r_k$ na imagem de entrada é substituído diretamente pelo valor $\hat{z}_k$ mapeado da imagem de referência:
   $$I_{\text{especificada}}(x, y) = \text{Mapeamento}[I_{\text{entrada}}(x, y)]$$

#### Vantagens e Aplicações Práticas:
1. **Correção e Padronização de Iluminação:** Normalizar lotes de imagens adquiridas sob diferentes condições de luz solar ou iluminação artificial antes de alimentar modelos de Aprendizado de Máquina (Machine Learning) ou Reconhecimento de Padrões.
2. **Harmonização em Sensoriamento Remoto:** Equalizar imagens de satélite tiradas em dias ou horários distintos para permitir mosaicos perfeitos sem emendas visíveis.
3. **Visão Médica:** Padronizar tomografias ou radiografias obtidas em diferentes equipamentos para calibrar o contraste em diagnósticos auxiliados por computador.
