# Estructuración Formal y Evaluación Estadístico-Experimental de Modelos Ocultos de Markov ante Perturbaciones No Estacionarias: Análisis de Regímenes de Mercado Financiero

**Sebastian Garces Cadavid¹, Sofia Miranda Cubides¹, Oscar Rene Peñaloza Ardila¹, Andres Mauricio Quintero Rios¹, Dr. Julián Andrés Loaiza López²·***

¹ Estudiantes de Ingeniería de Software y Datos, Curso de Simulación  
² Docente Asesor, Departamento de Ingeniería de Software y Datos, Institución Universitaria Digital de Antioquia (IU Digital)  
\* Docente asesor / Autor de correspondencia — Noviembre de 2026

sebastian.garcesc@est.iudigital.edu.co | sofia.miranda@est.iudigital.edu.co | oscar.penaloza@est.iudigital.edu.co | andres.quinteror@est.iudigital.edu.co | julian.loaiza@prof.iudigital.edu.co

---

## Resumen

El modelado estocástico mediante Modelos Ocultos de Markov (HMM) constituye un pilar fundamental en el análisis de sistemas con dinámica latente y observaciones ruidosas. En mercados financieros, perturbaciones exógenas como crisis económicas o cambios de política monetaria vulneran el supuesto estándar de homogeneidad temporal en las transiciones de estado. Este trabajo presenta un estudio estadístico-experimental estructurado bajo el estándar editorial Q1 que evalúa formalmente el impacto de la no estacionariedad en el rendimiento del algoritmo de Viterbi. Mediante una topología de N=3 estados latentes (Mercado Alcista, Mercado Lateral, Mercado Bajista) y M=3 emisiones discretas de retorno (Positivo, Neutral, Negativo), se diseñó un experimento Monte Carlo de 500 corridas pareadas (T=50 períodos de trading) comparando tres escenarios: Nominal (A_nominal estacionaria), Crisis no modelada (A_crisis en ventana crítica t=15 a t=25 con decodificador ciego) y Crisis modelada (A(t) adaptativa). Los resultados confirman que omitir la perturbación degrada la precisión diagnóstica en la ventana crítica, donde la formulación adaptativa alcanza un 70.42% frente al 67.64% del decodificador ciego (p < 10⁻⁸), superando significativamente al clasificador heurístico determinista de ventana deslizante (52.30%, p < 10⁻¹⁵).

**Palabras clave:** Modelos Ocultos de Markov, algoritmo de Viterbi, regímenes financieros, no estacionariedad, simulación Monte Carlo, cambio de régimen.

---

## 1. Introducción

Los mercados financieros son sistemas dinámicos complejos que exhiben comportamientos heterogéneos a lo largo del tiempo. La identificación de diferentes regímenes de mercado —alcista, lateral y bajista— constituye un problema central en finanzas cuantitativas, con implicaciones directas para la gestión de riesgo, la asignación de activos y la construcción de estrategias de trading [1, 9].

Los Modelos Ocultos de Markov (HMM), formalizados por Baum y Petrie [3] y ampliamente difundidos por el tutorial de Rabiner [1], proveen un marco probabilístico natural para modelar sistemas donde los estados subyacentes no son directamente observables. En el contexto financiero, los regímenes de mercado actúan como estados ocultos que se manifiestan a través de observaciones ruidosas: los retornos de los activos [8].

El trabajo seminal de Hamilton [2] introdujo los modelos de cambio de régimen (Markov-switching models) para el análisis de ciclos económicos, estableciendo que las series financieras pueden modelarse como procesos gobernados por una cadena de Markov latente. Investigaciones posteriores han confirmado que los retornos financieros presentan propiedades estadísticas bien documentadas —volatilidad en clusters, colas pesadas, asimetría— que son consistentes con una estructura de regímenes latentes [11, 8].

Sin embargo, un supuesto fundamental de los HMM estándar es la **homogeneidad temporal** de la matriz de transición: las probabilidades de cambio entre estados permanecen constantes en el tiempo. Esta condición se viola frecuentemente en la práctica cuando ocurren perturbaciones exógenas como crisis financieras, cambios de política monetaria o eventos geopolíticos, que alteran abruptamente las dinámicas de transición entre regímenes [7, 9].

---

## 2. Preguntas de investigación, objetivos y aportes

### Preguntas de investigación
- **P1:** ¿Cómo puede formalizarse matemáticamente el problema de inferencia de regímenes financieros mediante la tupla matricial $\lambda = (S, V, A, B, \pi)$ y resolverse de forma numéricamente estable?
- **P2:** ¿Cómo impacta la degradación estocástica de los parámetros del modelo (matrices de transición $A$ y emisión $B$) en la precisión diagnóstica y en los intervalos de confianza del modelo?
- **P3:** ¿En qué medida un HMM con decodificación de Viterbi es más robusto y reproducible frente a un baseline heurístico de ventana deslizante en diferentes escenarios de perturbación?

### Objetivos y aportes principales
1. **Formalización completa:** Deducción e implementación del modelo markoviano $\lambda$ con decodificación de Viterbi en log-probabilidades para evitar desbordamiento numérico (*underflow*).
2. **Evaluación comparativa justa:** Implementación de un clasificador determinista por ventana de latencia ($k=2$) como línea base de contraste operacional.
3. **Validación estadística rigurosa:** Evaluación sobre $N=500$ simulaciones Monte Carlo independientes con semilla fija global (`seed = 42`), reportando medias, desviaciones estándar e intervalos de confianza al 95% ($IC_{95\%}$) para tres escenarios contrastantes.

---

## 3. Marco Teórico y Metodología

### 3.1 Topología del modelo
Se formaliza el HMM mediante la quíntupla $\lambda = (S, V, A, B, \pi)$:
- **$S$ (Estados Ocultos, $N=3$):** Mercado Alcista ($S_1$), Mercado Lateral ($S_2$), Mercado Bajista ($S_3$).
- **$V$ (Observaciones Discretas, $M=3$):** Retorno Positivo ($v_1$), Retorno Neutral ($v_2$), Retorno Negativo ($v_3$).
- **$T = 50$ períodos** de trading discretos por simulación.

### 3.2 Matrices del Modelo

**Matriz de Transición Nominal ($A_{\text{nominal}}$):**
```
            Alcista   Lateral   Bajista
Alcista    [ 0.60      0.30      0.10 ]
Lateral    [ 0.30      0.40      0.30 ]
Bajista    [ 0.10      0.30      0.60 ]
```

**Matriz de Emisión ($B$):**
```
            Positivo  Neutral   Negativo
Alcista    [ 0.70      0.20      0.10 ]
Lateral    [ 0.30      0.40      0.30 ]
Bajista    [ 0.10      0.20      0.70 ]
```

**Distribución Inicial ($\pi$):**
```
π = [0.40, 0.30, 0.30]
```

### 3.3 Perturbación No Estacionaria (Crisis Financiera)
Durante la ventana crítica $t \in [15, 25]$, se aplica la matriz de transición perturbada $A_{\text{crisis}}$:
```
            Alcista   Lateral   Bajista
Alcista    [ 0.20      0.30      0.50 ]
Lateral    [ 0.10      0.30      0.60 ]
Bajista    [ 0.05      0.15      0.80 ]
```

---

## 4. Resultados Experimentales y Tablas

### Tabla 1. Estadísticos Descriptivos e Intervalos de Confianza al 95% ($N=500$ Corridas Pareadas)

| Métrica / Escenario | Media | Desv. Est. | Mediana | $IC_{95\%}$ Inf. | $IC_{95\%}$ Sup. |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Viterbi Nominal** | **59.56%** | 8.37% | 60.00% | 58.83% | 60.30% |
| **Heurística Baseline ($k=2$)** | 46.12% | 7.91% | 46.00% | 45.43% | 46.81% |
| **Viterbi Crisis Ciego** | 61.20% | 8.60% | 62.00% | 60.44% | 61.96% |
| **Viterbi Crisis Adaptativo** | **61.44%** | 8.58% | 62.00% | 60.68% | 62.19% |
| **Ventana Crítica Ciego** | 67.64% | 18.80% | 72.73% | 65.98% | 69.29% |
| **Ventana Crítica Adaptativo** | **70.42%** | 17.66% | 72.73% | 68.87% | 71.97% |
| **Ventana Crítica Heurística** | 52.30% | 15.42% | 54.55% | 50.95% | 53.65% |

### Tabla 2. Pruebas de Hipótesis Pareadas ($t$ de Student y $d$ de Cohen)

| Comparación Pareada | $\Delta$ Medias | Estadístico $t$ | $p$-valor | $d$ de Cohen | Significativo ($\alpha=0.05$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Nominal: Viterbi vs Heurística** | **+13.44%** | **+32.18** | **$< 10^{-15}$** | **+1.440** | **Sí** |
| **Nominal vs Crisis Ciego** | -1.64% | -7.38 | $< 10^{-12}$ | -0.330 | **Sí** |
| **Crisis Ciego vs Adaptativo** | -0.24% | -1.12 | 0.261 | -0.050 | No |
| **Ventana: Ciego vs Adaptativo** | **-2.78%** | **-5.75** | **$< 10^{-8}$** | **-0.257** | **Sí** |
| **Ventana: Adaptativo vs Heurística** | **+18.12%** | **+23.44** | **$< 10^{-15}$** | **+1.048** | **Sí** |

---

## 5. Discusión y Análisis de Riesgo

1. **Superioridad del HMM frente al Baseline:** El algoritmo de Viterbi superó en más de **13.44 puntos porcentuales** a la heurística de ventana deslizante en condiciones normales y en más de **18.12 puntos porcentuales** durante la ventana de crisis, validando que el modelado formal de transiciones latentes supera a las reglas reactivas univariadas.
2. **Efecto de Choques No Estacionarios:** La crisis no modelada altera significativamente la distribución de inferencia ($p < 10^{-12}$). Sin embargo, la formulación adaptativa $A(t)$ compensa la pérdida en la ventana de shock con una ganancia de **+2.78 puntos porcentuales** ($p < 10^{-8}$).
3. **Métricas Financieras:** En la corrida representativa, el régimen alcista aportó un retorno medio de $\mu = +2.14\%$ ($\sigma = 1.10\%$), frente al régimen bajista con $\mu = -2.41\%$ ($\sigma = 1.17\%$). El portafolio modelado reportó un Sharpe Ratio de $0.304$ y un Máximo Drawdown controlado de $-12.58\%$.

---

## 6. Conclusiones

Se estructuró, implementó y evaluó formalmente un Modelo Oculto de Markov para regímenes financieros con decodificación de Viterbi en log-probabilidades. El experimento Monte Carlo demostró la superioridad indiscutible del enfoque estocástico frente a líneas base deterministas y evidenció que las formulaciones adaptativas mitigan la degradación de inferencia en presencia de choques exógenos no estacionarios.

---

## Referencias Académicas Verificadas

[1] L. R. Rabiner, "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition," *Proceedings of the IEEE*, vol. 77, no. 2, pp. 257–286, 1989. DOI: 10.1109/5.18626

[2] J. D. Hamilton, "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle," *Econometrica*, vol. 57, no. 2, pp. 357–384, 1989. DOI: 10.2307/1912559

[3] L. E. Baum and T. Petrie, "Statistical Inference for Probabilistic Functions of Finite State Markov Chains," *The Annals of Mathematical Statistics*, vol. 37, no. 6, pp. 1554–1563, 1966.

[4] A. J. Viterbi, "Error Bounds for Convolutional Codes and an Asymptotically Optimum Decoding Algorithm," *IEEE Transactions on Information Theory*, vol. 13, no. 2, pp. 260–269, 1967. DOI: 10.1109/TIT.1967.1054010

[5] A. P. Dempster, N. M. Laird, and D. B. Rubin, "Maximum Likelihood from Incomplete Data via the EM Algorithm," *Journal of the Royal Statistical Society: Series B*, vol. 39, no. 1, pp. 1–38, 1977.

[6] J. D. Hamilton, *Time Series Analysis*. Princeton: Princeton University Press, 1994.

[7] A. Ang and G. Bekaert, "Regime Switches in Interest Rates," *Journal of Business & Economic Statistics*, vol. 20, no. 2, pp. 163–182, 2002. DOI: 10.1198/073500102317351930

[8] T. Rydén, T. Teräsvirta, and S. Åsbrink, "Stylized Facts of Daily Return Series and the Hidden Markov Model," *Journal of Applied Econometrics*, vol. 13, no. 3, pp. 217–244, 1998.

[9] M. Guidolin and A. Timmermann, "Asset Allocation under Multivariate Regime Switching," *Journal of Economic Dynamics and Control*, vol. 31, no. 11, pp. 3503–3544, 2007. DOI: 10.1016/j.jedc.2006.12.004

[10] P. Glasserman, *Monte Carlo Methods in Financial Engineering*. New York: Springer, 2003. DOI: 10.1007/978-0-387-21617-1

[11] R. Cont, "Empirical Properties of Asset Returns: Stylized Facts and Statistical Issues," *Quantitative Finance*, vol. 1, no. 2, pp. 223–236, 2001. DOI: 10.1080/713665670
