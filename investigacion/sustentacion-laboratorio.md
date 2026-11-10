# Sustentación del Laboratorio y Tickets de Salida
## Laboratorio de Investigación: "Investiga con IA, Decide con criterio"
### Curso: Simulación — Semestre 2026-II — IU Digital de Antioquia
### Docente Asesor: Dr. Julián Andrés Loaiza López

---

## 🎤 Sustentación Breve del Equipo (5 Preguntas Clave)

### 1. ¿Qué problema y pregunta seleccionaron?
* **Problema:** La inferencia estocástica de regímenes de mercado financiero (*Mercado Alcista, Lateral, Bajista*) a partir de observaciones ruidosas de retorno (*Positivo, Neutral, Negativo*) cuando ocurren perturbaciones exógenas no estacionarias (crisis financieras) que vulneran la homogeneidad temporal de las transiciones.
* **Pregunta Central ($P_1, P_2, P_3$):** ¿En qué medida un HMM con decodificación de Viterbi en log-probabilidades es más robusto y estadísticamente superior frente a un baseline heurístico determinista de ventana deslizante ($k=2$) ante choques no estacionarios temporales?

### 2. ¿Por qué considerar HMM y qué alternativa comparar?
* **Por qué HMM:** Porque desacopla formalmente la trayectoria oculta latente del sistema bursátil de las emisiones discretas ruidosas observadas en el mercado, modelando la persistencia y alternancia probabilística de regímenes económicos.
* **Alternativa de Comparación (Baseline):** Un clasificador determinista por ventana deslizante ($k=2$) basado en la tendencia predominante de las observaciones recientes, que emula la regla reactiva estándar de latencia corta utilizada por operadores tradicionales de trading.

### 3. ¿Qué instrucción modificaron y qué efecto observaron?
* **Modificación 1 (Estabilidad Numérica):** Se modificó la formulación de Viterbi para que operara en el espacio de log-probabilidades ($\ln a_{ij} + \ln b_j$).  
  *Efecto:* Se eliminó completamente el error de subdesbordamiento aritmético (*underflow*) que anulaba las probabilidades en horizontes $T \ge 50$.
* **Modificación 2 (Inclusión de Contraste Justo):** Se rechazó evaluar el HMM de manera aislada o contra un clasificador aleatorio y se incorporó obligatoriamente el baseline determinista ($k=2$).  
  *Efecto:* Permitió cuantificar una ganancia diagnóstica neta y estadísticamente rigurosa de $+13.44$ pp en condiciones nominales y $+18.12$ pp en crisis ($p < 10^{-15}, d = 1.05$).

### 4. ¿Qué hace su skill propia y cómo comprobaron su comportamiento?
* **Skill Creada:** `.agents/skills/evaluar-experimento-hmm/SKILL.md`.
* **Qué hace:** Estandariza la evaluación estadística comparativa, forzando la ejecución de Monte Carlo pareado ($N=500$), pruebas $t$ de Student pareadas, cálculo de $d$ de Cohen e intervalos de confianza al 95%.
* **Comprobación:** Se sometió a prueba ante la ausencia de matrices reales de mercado; la skill respondió reportando con transparencia que los parámetros eran de simulación didáctica controlada, absteniéndose de inventar datos empíricos falsos.

### 5. ¿Qué propuesta de la IA cuestionaron y qué evidencia sigue faltando?
* **Propuesta Cuestionada y Modificada:** La IA propuso inicialmente simular crisis como ruido gaussiano aditivo a los precios y evaluar con solo 10 corridas. El equipo la rechazó porque el ruido blanco aditivo no modela la violación de la homogeneidad markoviana en las transiciones de estado, y 10 réplicas carecen de potencia estadística. Se impuso una matriz $A_{\text{crisis}}$ en ventana crítica $t \in [15, 25]$ y $N=500$ corridas pareadas.
* **Evidencia que sigue faltando:** Datos empíricos de alta frecuencia tick-by-tick de bolsas reales (ej. S&P 500 o BVC) con calibración de parámetros continuos mediante el algoritmo de Baum-Welch (EM) y emisiones gaussianas.

---

## 🎟️ Tickets de Salida Individuales

### 1. Sebastian Garces Cadavid (`sebastian.garcesc@est.iudigital.edu.co`)
* **¿Qué decisión tomaste tú y qué evidencia utilizaste?**  
  Decidí fijar el protocolo de evaluación en $N=500$ réplicas Monte Carlo con semilla única `seed=42`. La evidencia fue la dispersión observada en los intervalos de confianza del 95%, que demostraron convergencia asintótica estable.
* **¿Qué propuesta modificaste o rechazaste y por qué?**  
  Rechacé la propuesta de evaluar la exactitud asumiendo que los estados eran conocidos en la realidad; aclaré que se trata de una simulación controlada donde conocemos la verdad fundamental únicamente para fines de validación experimental.
* **Siguiente paso:** Implementar el algoritmo Baum-Welch para entrenar las matrices $A$ y $B$ a partir de retornos históricos del índice COLCAP.

### 2. Sofia Miranda Cubides (`sofia.miranda@est.iudigital.edu.co`)
* **¿Qué decisión tomaste tú y qué evidencia utilizaste?**  
  Decidí incorporar el clasificador heurístico de ventana ($k=2$) como baseline. La evidencia fue la exigencia del estándar Q1 de no reportar exactitud de un modelo sin una línea base de referencia competitiva.
* **¿Qué propuesta modificaste o rechazaste y por qué?**  
  Modifiqué la forma de presentar los resultados gráficos, exigiendo que las figuras 1, 2 y 3 se exportaran a 300 DPI con fondos sombreados por régimen en lugar de gráficos interactivos efímeros.
* **Siguiente paso:** Evaluar la sensibilidad del modelo variando el tamaño de ventana de la heurística ($k=3, k=5$).

### 3. Oscar Rene Peñaloza Ardila (`oscar.penaloza@est.iudigital.edu.co`)
* **¿Qué decisión tomaste tú y qué evidencia utilizaste?**  
  Decidí modelar la crisis no estacionaria mediante una matriz perturbada específica $A_{\text{crisis}}$ con $a_{33}=0.80$ en la ventana $t \in [15, 25]$. La evidencia teórica provino de los trabajos de Hamilton (1989) y Ang & Bekaert (2002) sobre persistencia en regímenes de alta volatilidad.
* **¿Qué propuesta modificaste o rechazaste y por qué?**  
  Rechacé la sugerencia de la IA de usar bibliografía generada automáticamente y exigí verificar 11 fuentes académicas primarias con sus respectivos DOIs y autores reales.
* **Siguiente paso:** Estudiar extensiones semi-markovianas (HSMM) donde el tiempo de permanencia en crisis siga distribuciones de cola pesada.

### 4. Andres Mauricio Quintero Rios (`andres.quinteror@est.iudigital.edu.co`)
* **¿Qué decisión tomaste tú y qué evidencia utilizaste?**  
  Decidí implementar la formulación de Viterbi en log-probabilidades para evitar el desbordamiento numérico (*underflow*). La evidencia fue que la multiplicación de 50 probabilidades consecutivas producía valores menores a $10^{-300}$, colapsando a cero en precisión de punto flotante estándar.
* **¿Qué propuesta modificaste o rechazaste y por qué?**  
  Modifiqué las recomendaciones de trading para condicionarlas al análisis de riesgo formal (VaR 95%, Sharpe Ratio y Drawdown) en lugar de emitir recomendaciones cualitativas sin sustento cuantitativo.
* **Siguiente paso:** Conectar la inferencia de regímenes a un simulador de backtesting financiero con comisiones de corretaje y deslizamiento (*slippage*).

---
*Documento compilado y validado para la sesión del Laboratorio de Investigación.*

