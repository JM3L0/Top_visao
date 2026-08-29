import json
import base64
import io
import sys
import os
import contextlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2
from skimage import data

print("Gerando notebook conciso da 3ª Atividade...")

cells = []

def add_markdown(source):
    if isinstance(source, list):
        src = [s if s.endswith('\n') else s + '\n' for s in source]
    else:
        src = [s + '\n' for s in source.split('\n')]
    if src and src[-1] == '\n':
        src[-1] = ''
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": src
    })

def add_code(source, global_env):
    if isinstance(source, list):
        code_str = "".join(source)
        src = [s if s.endswith('\n') else s + '\n' for s in source]
    else:
        code_str = source
        src = [s + '\n' for s in source.split('\n')]
    if src and src[-1] == '\n':
        src[-1] = ''

    stdout_buf = io.StringIO()
    figures_data = []

    original_show = plt.show
    def custom_show(*args, **kwargs):
        for fig_num in plt.get_fignums():
            fig = plt.figure(fig_num)
            img_buf = io.BytesIO()
            fig.savefig(img_buf, format='png', bbox_inches='tight', dpi=100)
            img_buf.seek(0)
            b64_data = base64.b64encode(img_buf.read()).decode('utf-8')
            figures_data.append(b64_data)
        plt.close('all')

    plt.show = custom_show

    try:
        with contextlib.redirect_stdout(stdout_buf):
            exec(code_str, global_env)
        custom_show()
    finally:
        plt.show = original_show

    outputs = []
    stdout_val = stdout_buf.getvalue()
    if stdout_val:
        outputs.append({
            "output_type": "stream",
            "name": "stdout",
            "text": [line + '\n' for line in stdout_val.splitlines()]
        })

    for fig_b64 in figures_data:
        outputs.append({
            "output_type": "display_data",
            "data": {
                "image/png": fig_b64,
                "text/plain": ["<Figure size ... with ... Axes>"]
            },
            "metadata": {}
        })

    cells.append({
        "cell_type": "code",
        "execution_count": len([c for c in cells if c['cell_type'] == 'code']) + 1,
        "metadata": {},
        "outputs": outputs,
        "source": src
    })

env = {}

# 1. CABEÇALHO
add_markdown(r"""# UNIVERSIDADE FEDERAL DO PIAUÍ – UFPI
## CAMPUS SENADOR HELVÍDIO NUNES DE BARROS – PICOS
**Curso:** Sistemas de Informação | **Período:** 6° | **Ano/Semestre:** 2026.2  
**Disciplina:** Tópicos Especiais em Visão Computacional  
**Professor:** Me. José Denes Lima Araújo  

---
# 3ª ATIVIDADE - TÉCNICAS DE REALCE

**1) Aplique as seguintes técnicas de realce de imagem usando suas respectivas fórmulas. Ao aplicar cada uma das técnicas mostre o resultado com pelo menos duas variações de parâmetros para ver seus efeitos sobre as imagens:**
* a) Negativo da imagem.
* b) Alongamento de contraste (contrast stretching).
* c) Realce linear.
* d) Realce logarítmico.
* e) Realce quadrático.
* f) Realce por raiz quadrada.
* g) Correção gama.

**OBS:** aplique cada técnica de realce tanto em imagens em escala de cinza quanto em imagens coloridas (RGB). Em seguida, apresente a imagem original colorida, a imagem original em escala de cinza, a imagem em escala de cinza realçada e a imagem colorida realçada.""")

# 2. SETUP E CARREGAMENTO
add_markdown(r"""### Setup e Carregamento das Imagens""")
code_setup = """import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import data

# Carregando imagem de teste RGB e convertendo para escala de cinza
img_rgb = data.astronaut()
img_cinza = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# Função compacta para exibição padronizada dos resultados
def exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, t1="Var 1", t2="Var 2"):
    fig, axes = plt.subplots(2, 4, figsize=(15, 6))
    
    # Linha 1: Escala de Cinza
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title("1. Original RGB")
    axes[0, 1].imshow(img_cinza, cmap='gray')
    axes[0, 1].set_title("2. Original Cinza")
    axes[0, 2].imshow(cinza_v1, cmap='gray')
    axes[0, 2].set_title(f"3. Cinza ({t1})")
    axes[0, 3].imshow(cinza_v2, cmap='gray')
    axes[0, 3].set_title(f"4. Cinza ({t2})")
    
    # Linha 2: Imagem Colorida (RGB)
    axes[1, 0].imshow(img_rgb)
    axes[1, 0].set_title("1. Original RGB")
    axes[1, 1].imshow(img_cinza, cmap='gray')
    axes[1, 1].set_title("2. Original Cinza")
    axes[1, 2].imshow(rgb_v1)
    axes[1, 2].set_title(f"3. Colorida ({t1})")
    axes[1, 3].imshow(rgb_v2)
    axes[1, 3].set_title(f"4. Colorida ({t2})")
    
    for ax in axes.flat:
        ax.axis('off')
    plt.tight_layout()
    plt.show()
"""
add_code(code_setup, env)

# 3. ITEM A: NEGATIVO
add_markdown(r"""### a) Negativo da Imagem
**Fórmula:** $s = (L - 1) - r = 255 - r$""")
code_neg = """# Variação 1: Inversão total (s = 255 - r)
cinza_v1 = 255 - img_cinza
rgb_v1 = 255 - img_rgb

# Variação 2: Inversão com ganho suave (s = 255 - 0.7*r)
cinza_v2 = np.clip(255 - 0.7 * img_cinza, 0, 255).astype(np.uint8)
rgb_v2 = np.clip(255 - 0.7 * img_rgb, 0, 255).astype(np.uint8)

exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, "Total: 255 - r", "Suave: 255 - 0.7r")
"""
add_code(code_neg, env)

# 4. ITEM B: ALONGAMENTO DE CONTRASTE
add_markdown(r"""### b) Alongamento de Contraste (Contrast Stretching)
**Fórmula:** $s = \frac{r - r_{min}}{r_{max} - r_{min}} \times 255$""")
code_cs = """def stretch(img, p_min=0, p_max=100):
    rmin, rmax = np.percentile(img, p_min), np.percentile(img, p_max)
    return np.clip(((img - rmin) / (rmax - rmin)) * 255, 0, 255).astype(np.uint8)

# Variação 1: Min-Max (0% a 100%) | Variação 2: Percentis robustos (5% a 95%)
cinza_v1, rgb_v1 = stretch(img_cinza, 0, 100), stretch(img_rgb, 0, 100)
cinza_v2, rgb_v2 = stretch(img_cinza, 5, 95), stretch(img_rgb, 5, 95)

exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, "Min-Max (0-100%)", "Percentis (5-95%)")
"""
add_code(code_cs, env)

# 5. ITEM C: REALCE LINEAR
add_markdown(r"""### c) Realce Linear
**Fórmula:** $s = \text{clip}(\alpha \cdot r + \beta, 0, 255)$""")
code_lin = """def linear(img, a, b):
    return np.clip(a * img.astype(np.float32) + b, 0, 255).astype(np.uint8)

# Variação 1: Alto contraste (a=1.6, b=10) | Variação 2: Baixo contraste e mais brilho (a=0.7, b=50)
cinza_v1, rgb_v1 = linear(img_cinza, 1.6, 10), linear(img_rgb, 1.6, 10)
cinza_v2, rgb_v2 = linear(img_cinza, 0.7, 50), linear(img_rgb, 0.7, 50)

exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, "a=1.6, b=10", "a=0.7, b=50")
"""
add_code(code_lin, env)

# 6. ITEM D: REALCE LOGARÍTMICO
add_markdown(r"""### d) Realce Logarítmico
**Fórmula:** $s = c \cdot \ln(1 + r)$""")
code_log = """c_norm = 255.0 / np.log(256.0)

def log_transf(img, c):
    return np.clip(c * np.log(1.0 + img.astype(np.float32)), 0, 255).astype(np.uint8)

# Variação 1: c normalizado (~45.99) | Variação 2: c acentuado (60.0)
cinza_v1, rgb_v1 = log_transf(img_cinza, c_norm), log_transf(img_rgb, c_norm)
cinza_v2, rgb_v2 = log_transf(img_cinza, 60.0), log_transf(img_rgb, 60.0)

exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, f"c={c_norm:.1f} (Normalizado)", "c=60.0 (Expansão Alta)")
"""
add_code(code_log, env)

# 7. ITEM E: REALCE QUADRÁTICO
add_markdown(r"""### e) Realce Quadrático
**Fórmula:** $s = c \cdot r^2 = \frac{r^2}{255}$""")
code_quad = """def quadratico(img, ganho=1.0, offset=0):
    return np.clip(ganho * ((img.astype(np.float32) ** 2) / 255.0) + offset, 0, 255).astype(np.uint8)

# Variação 1: s = r²/255 | Variação 2: s = 1.3*(r²/255) - 15 (Acentuado)
cinza_v1, rgb_v1 = quadratico(img_cinza, 1.0, 0), quadratico(img_rgb, 1.0, 0)
cinza_v2, rgb_v2 = quadratico(img_cinza, 1.3, -15), quadratico(img_rgb, 1.3, -15)

exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, "s = r²/255 (Puro)", "s = 1.3*(r²/255) - 15")
"""
add_code(code_quad, env)

# 8. ITEM F: REALCE POR RAIZ QUADRADA
add_markdown(r"""### f) Realce por Raiz Quadrada
**Fórmula:** $s = 255 \cdot \sqrt{\frac{r}{255}}$""")
code_sqrt = """def raiz(img, exp):
    return np.clip(255.0 * ((img.astype(np.float32) / 255.0) ** exp), 0, 255).astype(np.uint8)

# Variação 1: Raiz quadrada (exp=0.5) | Variação 2: Raiz cúbica (exp=1/3)
cinza_v1, rgb_v1 = raiz(img_cinza, 0.5), raiz(img_rgb, 0.5)
cinza_v2, rgb_v2 = raiz(img_cinza, 1.0/3.0), raiz(img_rgb, 1.0/3.0)

exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, "Raiz Quadrada (r^0.5)", "Raiz Cúbica (r^0.33)")
"""
add_code(code_sqrt, env)

# 9. ITEM G: CORREÇÃO GAMA
add_markdown(r"""### g) Correção Gama
**Fórmula:** $s = 255 \cdot \left(\frac{r}{255}\right)^\gamma$""")
code_gam = """def gama(img, g):
    return np.clip(255.0 * ((img.astype(np.float32) / 255.0) ** g), 0, 255).astype(np.uint8)

# Variação 1: gamma = 0.5 (Clareamento) | Variação 2: gamma = 2.2 (Escurecimento)
cinza_v1, rgb_v1 = gama(img_cinza, 0.5), gama(img_rgb, 0.5)
cinza_v2, rgb_v2 = gama(img_cinza, 2.2), gama(img_rgb, 2.2)

exibir(cinza_v1, cinza_v2, rgb_v1, rgb_v2, "gamma = 0.5 (Clarear)", "gamma = 2.2 (Escurecer)")
"""
add_code(code_gam, env)

# Salvar o notebook JSON
notebook_dict = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

output_path = r"03_Atividade/03_Atividade_Tecnicas_de_Realce.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook_dict, f, indent=1, ensure_ascii=False)

print(f"Notebook conciso gerado com sucesso em: {output_path}")
print(f"Total de células: {len(cells)}")
