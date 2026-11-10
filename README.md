# Identificación de Regímenes de Mercado Financiero mediante Modelos Ocultos de Markov

## Estructuración Formal y Evaluación Estadístico-Experimental de Modelos Ocultos de Markov ante Perturbaciones No Estacionarias

### Autores
- **Sebastian Garces Cadavid** — sebastian.garcesc@est.iudigital.edu.co
- **Sofia Miranda Cubides** — sofia.miranda@est.iudigital.edu.co
- **Oscar Rene Peñaloza Ardila** — oscar.penaloza@est.iudigital.edu.co
- **Andres Mauricio Quintero Rios** — andres.quinteror@est.iudigital.edu.co

### Docente Asesor
- **Dr. Julián Andrés Loaiza López** — julian.loaiza@prof.iudigital.edu.co

### Institución
Institución Universitaria Digital de Antioquia (IU Digital)  
Departamento de Ingeniería de Software y Datos  
Curso de Simulación — Noviembre 2026

---

## Descripción

Este repositorio contiene el código fuente, datos experimentales y manuscrito del proyecto de investigación que evalúa formalmente el impacto de la **no estacionariedad** en el rendimiento del algoritmo de **Viterbi** para la identificación de regímenes de mercado financiero mediante un **Modelo Oculto de Markov (HMM)**.

### Topología del modelo
- **N = 3 estados latentes**: Mercado Alcista, Mercado Lateral, Mercado Bajista
- **M = 3 emisiones discretas**: Retorno Positivo, Retorno Neutral, Retorno Negativo

### Diseño experimental
- Simulación Monte Carlo con **500 corridas pareadas**
- **T = 50** períodos de trading por corrida
- **3 escenarios**: Nominal (estacionario), Crisis no modelada (decodificador ciego), Crisis modelada (decodificador adaptativo)
- Evaluación mediante pruebas t pareadas con intervalos de confianza al 95%

---

## Estructura del Repositorio

```
├── 📄 Documentos del Artículo y Cuaderno
│   ├── articulo_final_q1.pdf          # Artículo formal en PDF con nombres y 11 referencias
│   ├── anteproyecto_hmm_financiero.tex # Código fuente LaTeX del artículo
│   ├── anteproyecto_hmm_financiero.md  # Manuscrito en Markdown
│   └── simulacion_hmm_financiero.ipynb # Cuaderno interactivo ejecutable para Google Colab
│
├── 📊 Datos Experimentales y Gráficos (300 dpi)
│   ├── tabla_resumen.csv              # Estadísticos descriptivos e intervalos de confianza al 95%
│   ├── pruebas_hipotesis.csv          # Resultados de las pruebas t pareadas
│   ├── resultados_crudos.csv          # Datos individuales de las 500 corridas
│   ├── precision_global_ventana.png   # Figura 1
│   ├── precision_paso_a_paso.png      # Figura 2
│   └── corrida_individual.png         # Figura 3
│
├── ⚙️ Configuración y Código
│   ├── README.md                      # Documentación principal del repositorio
│   ├── requirements.txt               # Lista de librerías para instalación con pip
│   └── generar_pdf.py                 # Script que genera el PDF
│
├── 📁 Carpetas
│   ├── src/
│   │   └── simulacion.py             # Código fuente principal de la simulación
│   ├── materiales/
│   │   └── caso-servidor.md          # Descripción del caso de estudio
│   ├── investigacion/
│   │   └── ficha-proyecto.md         # Ficha técnica del proyecto
│   └── bitacora-decisiones.md        # Registro de decisiones del equipo
```

---

## Instalación y Ejecución

### Requisitos
```bash
pip install -r requirements.txt
```

### Ejecución local
```bash
python src/simulacion.py --seed 42 --periodos 50 --corridas 500 --salida .
```

### Google Colab
Abrir `simulacion_hmm_financiero.ipynb` directamente en [Google Colab](https://colab.research.google.com/).

---

## Resultados Principales

| Escenario | Precisión Media | IC 95% |
|-----------|:-:|:-:|
| Nominal | 59.56% | [58.83%, 60.30%] |
| Crisis (ciego) | 61.20% | [60.44%, 61.96%] |
| Crisis (adaptativo) | 61.44% | [60.68%, 62.19%] |

Las pruebas t pareadas confirman que:
- La crisis **sí** impacta significativamente la precisión (p < 0.001)
- La adaptación en ventana de crisis mejora la precisión de 67.64% a 70.42% (p < 0.001)

---

## Licencia
Proyecto académico — Uso educativo únicamente.

