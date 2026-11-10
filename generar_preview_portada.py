"""
Genera una imagen de alta resolución de la primera página del artículo para previsualización inmediata.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

fig = plt.figure(figsize=(8.5, 11), dpi=300)
fig.patch.set_facecolor('white')

# Título principal
plt.text(0.5, 0.93, "Estructuración Formal y Evaluación Estadístico-Experimental de Modelos\nOcultos de Markov ante Perturbaciones No Estacionarias:\nAnálisis de Regímenes de Mercado Financiero",
         ha='center', va='center', fontsize=12.5, fontweight='bold', linespacing=1.35, color='#0f172a')

# Bloque formal de autores solicitados
autores_linea = "Sebastian Garces Cadavid¹, Sofia Miranda Cubides¹, Oscar Rene Peñaloza Ardila¹,\nAndres Mauricio Quintero Rios¹, Dr. Julián Andrés Loaiza López²*"
plt.text(0.5, 0.84, autores_linea, ha='center', va='center', fontsize=9.5, fontweight='bold', linespacing=1.3, color='#1e293b')

filiaciones = ("¹Estudiantes de Ingeniería de Software y Datos, Curso de Simulación\n"
               "²Docente Asesor, Departamento de Ingeniería de Software y Datos, Institución Universitaria Digital de Antioquia (IU Digital)\n"
               "{sebastian.garces, sofia.miranda, oscar.penaloza, andres.quintero}@est.iudigital.edu.co | julian.loaiza@prof.iudigital.edu.co\n"
               "*Docente asesor / Autor de correspondencia — Noviembre de 2026")
plt.text(0.5, 0.77, filiaciones, ha='center', va='center', fontsize=7.5, style='italic', linespacing=1.25, color='#475569')

# Línea divisoria
plt.plot([0.08, 0.92], [0.725, 0.725], color='#94a3b8', lw=1.0)

# Resumen formal
resumen_txt = (
    "Resumen — El modelado estocástico mediante Modelos Ocultos de Markov (HMM) constituye un pilar fundamental en el análisis "
    "de sistemas con dinámica latente y observaciones ruidosas. En mercados financieros, perturbaciones exógenas como crisis económicas "
    "vulneran el supuesto estándar de homogeneidad temporal en las transiciones de estado. Este trabajo presenta un estudio "
    "estadístico-experimental estructurado bajo estándar editorial Q1 que evalúa formalmente el impacto de la no estacionariedad "
    "en el rendimiento del algoritmo de Viterbi. Mediante una topología de N=3 estados latentes (Mercado Alcista, Lateral, Bajista) "
    "y M=3 emisiones discretas de retorno (Positivo, Neutral, Negativo), se diseñó un experimento Monte Carlo de 500 corridas pareadas "
    "(T=50 períodos de trading) comparando tres escenarios: Nominal (A_nominal estacionaria), Crisis no modelada (A_crisis en ventana "
    "crítica t=15 a 25 con decodificador ciego) y Crisis modelada (A(t) adaptativa). Los resultados confirman que omitir la perturbación "
    "degrada la precisión diagnóstica en la ventana crítica, donde la formulación adaptativa alcanza 70.42% frente al 67.64% del decodificador "
    "ciego (p < 10^-8), superando significativamente al clasificador heurístico determinista de ventana deslizante (52.30%, p < 10^-15).\n\n"
    "Palabras clave — Modelos Ocultos de Markov, algoritmo de Viterbi, regímenes financieros, no estacionariedad, simulación Monte Carlo."
)
plt.text(0.5, 0.61, resumen_txt, ha='center', va='center', fontsize=7.5,
         bbox=dict(boxstyle='square,pad=0.8', facecolor='#f8fafc', edgecolor='#cbd5e1'), linespacing=1.25, color='#1e293b')

# Sección 2
sec2 = (
    "2. Preguntas de investigación, objetivos y aportes\n\n"
    "Preguntas de investigación:\n"
    "• P1: ¿Cómo puede formalizarse matemáticamente el problema de inferencia de regímenes financieros mediante la tupla matricial\n"
    "  λ = (S, V, A, B, π) y resolverse de forma numéricamente estable?\n"
    "• P2: ¿Cómo impacta la degradación estocástica de los parámetros del modelo (matrices de transición A y emisión B) en la precisión\n"
    "  diagnóstica y en los intervalos de confianza del modelo?\n"
    "• P3: ¿En qué medida un HMM con decodificación de Viterbi es más robusto y reproducible frente a un baseline heurístico de\n"
    "  ventana deslizante en diferentes escenarios de perturbación?\n\n"
    "Objetivos y aportes principales:\n"
    "1. Formalización completa: Deducción e implementación del modelo markoviano λ con decodificación de Viterbi en log-probabilidades\n"
    "   para evitar desbordamiento numérico (underflow).\n"
    "2. Evaluación comparativa justa: Implementación de un clasificador determinista por ventana de latencia (k = 2) como línea base de contraste.\n"
    "3. Validación estadística rigurosa: Evaluación sobre N = 500 simulaciones Monte Carlo independientes con semilla fija global (seed = 42),\n"
    "   reportando medias, desviaciones estándar e intervalos de confianza al 95% (IC 95%) para tres escenarios contrastantes."
)
plt.text(0.08, 0.45, sec2, ha='left', va='top', fontsize=7.4, linespacing=1.25, color='#0f172a')

# Tablas
tablas = (
    "3. Resultados Experimentales (Monte Carlo N=500 corridas pareadas, T=50)\n"
    "---------------------------------------------------------------------------------------------------------\n"
    "Métrica / Escenario                      Media        Desv. Est.       IC 95% Inferior       IC 95% Superior\n"
    "---------------------------------------------------------------------------------------------------------\n"
    "Viterbi Nominal                          59.56%         8.37%              58.83%                60.30%\n"
    "Heurística Baseline (k=2)                46.12%         7.91%              45.43%                46.81%\n"
    "Viterbi Crisis Ciego                     61.20%         8.60%              60.44%                61.96%\n"
    "Viterbi Crisis Adaptativo                61.44%         8.58%              60.68%                62.19%\n"
    "Ventana Crítica Ciego                    67.64%        18.80%              65.98%                69.29%\n"
    "Ventana Crítica Adaptativo               70.42%        17.66%              68.87%                71.97%\n"
    "Ventana Crítica Heurística               52.30%        15.42%              50.95%                53.65%\n"
    "---------------------------------------------------------------------------------------------------------\n"
    "Pruebas t pareadas de hipótesis (α = 0.05):\n"
    "• Nominal (Viterbi vs Heurística Baseline):  Δ = +13.44%,  t = +32.18,  p < 10^-15,  d = +1.44 (Muy Grande)\n"
    "• Ventana Crítica (Ciego vs Adaptativo):     Δ = -2.78%,   t = -5.75,   p < 10^-8,   d = -0.26 (Significativo)"
)
plt.text(0.08, 0.22, tablas, ha='left', va='top', fontsize=6.8, family='monospace', linespacing=1.2, color='#0f172a')

plt.axis('off')
plt.savefig('portada_articulo_nombres.png', bbox_inches='tight', dpi=300)
plt.close(fig)
print("Portada en PNG generada: portada_articulo_nombres.png")

