# 4ª Atividade - Técnicas de Filtragem Espacial
**Disciplina:** Tópicos Especiais em Visão Computacional  
**Professor:** Me. José Denes Lima Araújo  
**Aluno:** João Marcos Sousa Rufino Leal  

---

### 1) O que são filtros espaciais de suavização? Quais são suas principais aplicações?

**Resposta:**

Filtros espaciais de suavização (ou filtros passa-baixa) são técnicas aplicadas diretamente sobre os pixels de uma imagem para reduzir variações bruscas de intensidade e ruídos, gerando um efeito de desfoque (suavização). O valor de cada pixel é recalculado com base nos pixels da sua vizinhança.

Os principais tipos são:
- **Filtros Lineares (Média e Gaussiano):** substituem o pixel central pela média (simples ou ponderada) dos vizinhos.
- **Filtros Não-Lineares (Mediana):** ordenam os pixels da vizinhança e pegam o valor central (mediana).

**Principais aplicações:**
1. **Redução de ruído:** eliminação de ruído gaussiano (usando média ou gaussiano) e ruído tipo sal e pimenta (usando mediana).
2. **Pré-processamento:** suavizar a imagem antes de aplicar algoritmos de detecção de bordas (como Sobel ou Canny) ou segmentação, evitando falsas detecções causadas por ruídos.
3. **Junção de descontinuidades:** fechar pequenos cortes ou falhas em linhas, contornos e caracteres (útil em OCR).
4. **Remoção de detalhes pequenos:** eliminar texturas irrelevantes de fundo para destacar objetos maiores.

---

### 2) Dada a seguinte imagem representada por uma matriz de pixels, informe as saídas após a aplicação dos filtros de suavização:

**Matriz de entrada (8x8):**
```
[[  0, 230,   0,   0,   0,   0,   0,   0],
 [  0, 230,   0,   0, 210, 210, 210,   0],
 [  0,   0,   0,   0, 190, 190, 210,   0],
 [  0,   0,   0,   0, 190,   0, 210,   0],
 [  0,   0,   0,   0, 190, 190, 210,   0],
 [  0,   0,   0,   0,   0,   0,   0,   0],
 [  0,   0, 190,   0,   0,   0,   0,   0],
 [  0,   0,   0,   0,   0,   0,   0,   0]]
```

---

#### **a) Filtro da média, máscara 3x3**

* **Borda não processada (mantém as bordas originais):**
```
[[  0.0, 230.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0],
 [  0.0,  51.1,  51.1,  44.4,  88.9, 135.6,  91.1,   0.0],
 [  0.0,  25.6,  25.6,  65.6, 110.0, 180.0, 114.4,   0.0],
 [  0.0,   0.0,   0.0,  63.3, 105.6, 175.6, 112.2,   0.0],
 [  0.0,   0.0,   0.0,  42.2,  63.3, 110.0,  67.8,   0.0],
 [  0.0,  21.1,  21.1,  42.2,  42.2,  65.6,  44.4,   0.0],
 [  0.0,  21.1,  21.1,  21.1,   0.0,   0.0,   0.0,   0.0],
 [  0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0]]
```

* **Padding por replicação (replica a borda mais próxima):**
```
[[ 76.7,  76.7,  76.7,  23.3,  46.7,  70.0,  46.7,  23.3],
 [ 51.1,  51.1,  51.1,  44.4,  88.9, 135.6,  91.1,  46.7],
 [ 25.6,  25.6,  25.6,  65.6, 110.0, 180.0, 114.4,  70.0],
 [  0.0,   0.0,   0.0,  63.3, 105.6, 175.6, 112.2,  70.0],
 [  0.0,   0.0,   0.0,  42.2,  63.3, 110.0,  67.8,  46.7],
 [  0.0,  21.1,  21.1,  42.2,  42.2,  65.6,  44.4,  23.3],
 [  0.0,  21.1,  21.1,  21.1,   0.0,   0.0,   0.0,   0.0],
 [  0.0,  21.1,  21.1,  21.1,   0.0,   0.0,   0.0,   0.0]]
```

---

#### **b) Filtro da mediana, máscara 3x3**

* **Borda não processada:**
```
[[  0, 230,   0,   0,   0,   0,   0,   0],
 [  0,   0,   0,   0,   0, 190,   0,   0],
 [  0,   0,   0,   0, 190, 210, 190,   0],
 [  0,   0,   0,   0, 190, 190, 190,   0],
 [  0,   0,   0,   0,   0, 190,   0,   0],
 [  0,   0,   0,   0,   0,   0,   0,   0],
 [  0,   0, 190,   0,   0,   0,   0,   0],
 [  0,   0,   0,   0,   0,   0,   0,   0]]
```

* **Padding por replicação:**
```
[[  0,   0,   0,   0,   0,   0,   0,   0],
 [  0,   0,   0,   0,   0, 190,   0,   0],
 [  0,   0,   0,   0, 190, 210, 190,   0],
 [  0,   0,   0,   0, 190, 190, 190,   0],
 [  0,   0,   0,   0,   0, 190,   0,   0],
 [  0,   0,   0,   0,   0,   0,   0,   0],
 [  0,   0,   0,   0,   0,   0,   0,   0],
 [  0,   0,   0,   0,   0,   0,   0,   0]]
```
