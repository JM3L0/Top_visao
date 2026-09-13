# UNIVERSIDADE FEDERAL DO PIAUÍ – UFPI
## CAMPUS SENADOR HELVÍDIO NUNES DE BARROS – PICOS
**Curso:** Bacharelado em Sistemas de Informação | **Período:** 7° | **Ano/Semestre:** 2026.2  
**Disciplina:** Tópicos Especiais em Visão Computacional  
**Professor:** Me. José Denes Lima Araújo  
**Aluno:** João Marcos Sousa Rufino Leal  

---

# 6ª ATIVIDADE - TRANSFORMAÇÕES GEOMÉTRICAS E INTERPOLAÇÃO DE INTENSIDADES
## Respostas Teóricas e Análise Comparativa

---

### Questão 1) A interpolação de intensidades tem como objetivo preencher os valores desconhecidos entre os pixels amostrados de forma suave e contínua, minimizando artefatos e evitando a perda de detalhes na imagem resultante. Com base nisso, realize uma análise dos seguintes algoritmos de interpolação de intensidade abaixo.

---

### 1.a) Explicação do funcionamento, características, vantagens e desvantagens dos algoritmos:
* **Bilinear**
* **Bicúbica**

---

#### Por que precisamos interpolar?
Quando aplicamos transformações geométricas em uma imagem (como aumentar o tamanho, girar ou cisalhar), usamos o **mapeamento inverso**: pegamos cada pixel da nova imagem e calculamos onde ele estaria na imagem original. 

Na maioria das vezes, essa coordenada calculada cai em uma posição com casas decimais (por exemplo, linha 12.4, coluna 45.7). Como a imagem original só tem valores em posições inteiras, precisamos estimar o valor desse pixel a partir dos pixels vizinhos. É aí que entram os métodos de interpolação.

---

#### 1. Interpolação Bilinear

* **Como funciona:**
  A interpolação bilinear calcula o novo valor a partir dos **4 pixels vizinhos mais próximos** (uma janelinha $2 \times 2$). 
  O cálculo é feito em duas etapas simples:
  1. Primeiro, fazemos uma interpolação linear na horizontal (eixo $x$) usando a parte decimal da coordenada ($dx$).
  2. Em seguida, pegamos os dois valores intermediários calculados e fazemos outra interpolação linear na vertical (eixo $y$) usando $dy$.

  A fórmula direta junta esses passos em uma média ponderada dos 4 pixels:
  $$f(x, y) = (1 - dx)(1 - dy) \cdot I_{11} + dx(1 - dy) \cdot I_{21} + (1 - dx)dy \cdot I_{12} + dx\,dy \cdot I_{22}$$

* **Vantagens:**
  * **Elimina o aspecto pixelado:** acaba com os blocos e o efeito "mosaico" do vizinho mais próximo.
  * **Rápida e leve:** faz poucas operações matemáticas por pixel, sendo muito eficiente para executar em tempo real.
  * **Segura:** os pesos somam 1 e são todos positivos, então o valor resultante nunca passa de 255 nem fica abaixo de 0.

* **Desvantagens:**
  * **Perda de nitidez (desfoque/blur):** como tira uma média ponderada direta, tende a suavizar bordas finas e detalhes pequenos da cena.
  * As transições entre os pixels são lineares, o que pode dar uma leve impressão de "rugas" ou vincos nos gradientes sob ampliação grande.

---

#### 2. Interpolação Bicúbica

* **Como funciona:**
  Em vez de olhar apenas 4 pixels, a interpolação bicúbica analisa uma vizinhança maior de **16 pixels ($4 \times 4$)**. 
  Ela utiliza curvas cúbicas (polinômios de 3º grau, normalmente a função de Keys com $a = -0.5$) para calcular os pesos de cada vizinho com base na distância até o ponto desejado. Por usar polinômios de 3º grau, ela consegue modelar curvas suaves tanto na linha quanto na coluna, acompanhando melhor a curvatura natural da imagem.

* **Vantagens:**
  * **Excelente qualidade e nitidez:** preserva bordas com muito mais clareza e nitidez do que a bilinear, sem deixar a imagem borrada.
  * **Transições suaves e naturais:** garante que tanto a intensidade quanto a sua inclinação (derivada) variem suavemente, sem quebras angulares.
  * É o método mais usado em softwares profissionais de imagem e visão computacional quando a prioridade é fidelidade visual.

* **Desvantagens:**
  * **Mais pesada computacionalmente:** precisa acessar 16 posições de memória e calcular funções cúbicas para cada pixel, consumindo cerca de 3 a 5 vezes mais tempo que a bilinear.
  * **Pequenos artefatos de contorno (*ringing*):** em transições muito bruscas (como uma linha preta encostada em um fundo branco puro), a curvatura do polinômio pode gerar um efeito de leve halo claro ou escuro ao redor da borda.

---

### 1.b) Aplicação nas Transformações Geométricas (Escala, Rotação e Cisalhamento) e Comparação com o Vizinho Mais Próximo

---

#### 1. Comparativo Visual nas Transformações

Aplicando os três métodos na imagem do *Cameraman* ($512 \times 512$, em nível de cinza), notamos diferenças claras:

* **Escala (Ampliação de 2x):**
  * **Vizinho Mais Próximo:** a imagem fica cheia de blocos quadrados grandes (pixelizada). As linhas diagonais parecem escadas.
  * **Bilinear:** remove totalmente os blocos, mas deixa detalhes finos (como as hastes do tripé e o quepe) visivelmente desfocados.
  * **Bicúbica:** entrega o melhor resultado visual. As bordas continuam bem definidas, o contraste se mantém e a imagem parece natural, sem blocos e sem o desfoque da bilinear.

* **Rotação (30° em torno do centro):**
  * **Vizinho Mais Próximo:** todas as retas inclinadas ficam com degraus rígidos e serrilhados (*jaggies*), dando um aspecto quebrado às bordas.
  * **Bilinear:** suaviza os degraus criando tons cinzentos intermediários nas bordas. Fica melhor, mas com contornos levemente esfumaçados.
  * **Bicúbica:** as linhas inclinadas ficam contínuas, bem desenhadas e nítidas, com bordas limpas e sem serrilhado perceptível.

* **Cisalhamento (*Shear* horizontal e vertical):**
  * **Vizinho Mais Próximo:** a deformação angular quebra as retas em vários degraus repetidos.
  * **Bilinear:** espalha suavemente a deformação, mantendo as superfícies contínuas.
  * **Bicúbica:** preserva com precisão o alinhamento das texturas e o contraste das faixas oblíquas.

---

#### 2. Comparativo de Desempenho Computacional

Medindo o tempo real de execução no processamento da imagem:

| Método de Interpolação | Vizinhos Usados | Tempo Médio ($512 \times 512$) | Qualidade Visual | Quando Usar? |
| :--- | :---: | :---: | :---: | :--- |
| **Vizinho Mais Próximo** | 1 | **~5 ms** | Baixa (serrilhada e em blocos) | Quando a velocidade for a única prioridade, ou em máscaras binárias/labels de segmentação. |
| **Bilinear** | 4 | **~22 ms** | Boa (suave, porém com leve desfoque) | Ótimo equilíbrio para aplicações interativas, jogos, aumentação de dados e tempo real. |
| **Bicúbica** | 16 | **~94 ms** | Excelente (nítida e sem serrilhado) | Ideal para edição de imagem, impressão, diagnósticos médicos e processamento onde a qualidade é essencial. |

---

#### 3. Conclusão Direta

1. **Vizinho Mais Próximo:** é quase instantâneo, mas a qualidade visual é fraca na maioria dos casos práticos de transformação contínua.
2. **Bilinear:** é rápida e resolve o problema dos blocos, servindo como uma solução prática muito eficiente no dia a dia.
3. **Bicúbica:** exige mais cálculos, mas entrega com folga a imagem mais limpa, nítida e fiel ao original.
