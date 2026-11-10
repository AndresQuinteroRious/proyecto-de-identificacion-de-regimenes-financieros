# Bitácora de Decisiones sobre IA (Trazabilidad del Asistente)
## Proyecto: Identificación de Regímenes Financieros mediante HMM ante Perturbaciones No Estacionarias
### Semestre 2026-II — IU Digital de Antioquia

---

> **Finalidad del Documento**: Registra cronológicamente cada propuesta técnica, metodológica o de código generada por el asistente de IA a lo largo de las etapas del curso, su método empírico de verificación y la decisión explícita (aceptar, modificar o rechazar) expresada y justificada por el equipo de investigación.

---

### Registro Cronológico de Interacciones y Validación

#### Etapa 1: Definición del Dominio y Topología del HMM
- **Propuesta de la IA**: Modelar los regímenes financieros mediante un espacio continuo de estados con modelos GARCH acoplados.
- **Método de Verificación**: Contraste con el programa del curso y la especificación formal del problema docente.
- **Decisión Humana**: **Modificar**. Se instruyó implementar un HMM estrictamente discreto de $N=3$ estados latentes y $M=3$ emisiones discretas para garantizar control analítico exacto y decodificación reproducible.

#### Etapa 2: Estabilidad Numérica del Algoritmo de Viterbi
- **Propuesta de la IA**: Computar la recursión tradicional en probabilidades directas $\delta_t(j) = \max_i [\delta_{t-1}(i) \cdot a_{ij}] \cdot b_j(O_t)$.
- **Método de Verificación**: Prueba de ejecución en horizonte $T=50$. Se detectó desbordamiento hacia cero (*underflow*) por acumulación de potencias decimales infinitesimales.
- **Decisión Humana**: **Modificar / Corregir**. Se exigió la formulación estricta en el espacio de log-probabilidades $\delta_t(j) = \max_i [\delta_{t-1}(i) + \ln a_{ij}] + \ln b_j(O_t)$, resolviendo el problema $P_1$.

#### Etapa 3: Formulación del Baseline de Contraste Operacional
- **Propuesta de la IA**: Contrastar el HMM únicamente frente a un clasificador aleatorio uniforme ($1/3$).
- **Método de Verificación**: Análisis de rigurosidad editorial para publicación científica (estándar Q1). Un clasificador aleatorio representa un contraste trivial no competitivo.
- **Decisión Humana**: **Rechazar**. Se diseñó y codificó un clasificador heurístico determinista de ventana deslizante ($k=2$) basado en la tendencia de las observaciones recientes, resolviendo el problema $P_3$.

#### Etapa 4: Modelado de No Estacionariedad (Crisis Financiera)
- **Propuesta de la IA**: Simular perturbaciones mediante ruido blanco gaussiano aditivo a la serie temporal de precios.
- **Método de Verificación**: Evaluación teórica de la hipótesis markoviana. El ruido aditivo no viola el supuesto de homogeneidad temporal en las transiciones de régimen.
- **Decisión Humana**: **Modificar**. Se estructuró una matriz estocástica no homogénea $A_{\text{crisis}}$ aplicada en una ventana crítica delimitada $t \in [15, 25]$, donde la probabilidad de absorción/retención del régimen bajista salta al 80%, modelando una crisis exógena real (problema $P_2$).

#### Etapa 5: Protocolo Experimental y Significancia Estadística
- **Propuesta de la IA**: Ejecutar 10 simulaciones aisladas y reportar promedios simples.
- **Método de Verificación**: Cálculo de potencia estadística y tamaño del efecto. Una muestra de $N=10$ carece de poder para detectar diferencias con significancia $p < 0.05$.
- **Decisión Humana**: **Modificar**. Se estableció un diseño Monte Carlo riguroso de $N=500$ corridas pareadas con semilla global base `seed = 42`, reportando intervalos de confianza al 95% ($IC_{95\%}$), estadísticos $t$ pareados y $d$ de Cohen.

#### Etapa 6: Resolución de Visualizaciones
- **Propuesta de la IA**: Generar gráficos estándar en pantalla mediante llamadas interactivas de `plt.show()`.
- **Método de Verificación**: Inspección de requisitos editoriales. La compilación y exportación de figuras para artículos Q1 exige gráficos exportados directamente en archivos a 300 DPI (`precision_global_ventana.png`, `precision_paso_a_paso.png`, `corrida_individual.png`).
- **Decisión Humana**: **Modificar**. Se implementó backend headless (`matplotlib.use('Agg')`) y renderizado directo a 300 DPI con leyendas formales.

#### Etapa 7: Adjudicación de Autorías y Citas
- **Propuesta de la IA**: Mantener nombres de prueba y citas genéricas.
- **Método de Verificación**: Verificación de identidad estudiantil y búsqueda académica en bases de datos indexadas (Scopus / IEEE Xplore / Web of Science).
- **Decisión Humana**: **Aceptar formalización**:
  - Autorías asignadas: Sebastian Garces Cadavid, Sofia Miranda Cubides, Oscar Rene Peñaloza Ardila, Andres Mauricio Quintero Rios y Dr. Julián Andrés Loaiza López (Asesor).
  - Fuentes verificadas: 11 referencias reales fundamentales (Rabiner 1989, Hamilton 1989, Viterbi 1967, Cont 2001, etc.).

---
*Trazabilidad actualizada y verificada.*

