# Comparación de Skills y Enfoques de Simulación
## Evaluación Experimental de Capacidades de Modelado y Decodificación Estocástica

### 1. Resumen Ejecutivo
Este documento recopila la evidencia comparativa de desempeño entre el clasificador estocástico HMM (con decodificación óptima de Viterbi) y el clasificador heurístico determinista de ventana deslizante ($k=2$) ante diferentes condiciones de estacionariedad temporal.

### 2. Tabla Comparativa de Rendimiento (Monte Carlo N=500, T=50)

| Enfoque / Algoritmo | Escenario Operacional | Precisión Media ($\mu$) | Desviación Estándar ($\sigma$) | $IC_{95\%}$ | Complejidad Temporal |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Viterbi (Log-Probabilidades)** | Nominal Estacionario | **59.56%** | 8.37% | [58.83%, 60.30%] | $\mathcal{O}(T \cdot N^2)$ |
| **Heurística Determinista ($k=2$)** | Nominal Estacionario | 46.12% | 7.91% | [45.43%, 46.81%] | $\mathcal{O}(T \cdot k)$ |
| **Viterbi Ciego** | Crisis Perturbada | 61.20% | 8.60% | [60.44%, 61.96%] | $\mathcal{O}(T \cdot N^2)$ |
| **Viterbi Adaptativo $A(t)$** | Crisis Perturbada | **61.44%** | 8.58% | [60.68%, 62.19%] | $\mathcal{O}(T \cdot N^2)$ |
| **Viterbi Adaptativo** | Ventana Crítica $[15, 25]$ | **70.42%** | 17.66% | [68.87%, 71.97%] | $\mathcal{O}(T_{\text{crisis}} \cdot N^2)$ |
| **Viterbi Ciego** | Ventana Crítica $[15, 25]$ | 67.64% | 18.80% | [65.98%, 69.29%] | $\mathcal{O}(T_{\text{crisis}} \cdot N^2)$ |
| **Heurística Determinista ($k=2$)** | Ventana Crítica $[15, 25]$ | 52.30% | 15.42% | [50.95%, 53.65%] | $\mathcal{O}(T_{\text{crisis}} \cdot k)$ |

### 3. Conclusiones Comparativas Principales
1. **Superioridad de Viterbi**: El HMM con decodificación de Viterbi supera al baseline heurístico en más de **13.4 puntos porcentuales** en el escenario nominal y en más de **18.1 puntos porcentuales** en la ventana crítica de crisis ($p < 10^{-15}$).
2. **Capacidad de Adaptación**: En la ventana crítica de shock exógeno, el decodificador adaptativo $A(t)$ supera al decodificador ciego en $+2.78$ puntos porcentuales ($p < 10^{-8}$), demostrando la necesidad de incorporar mecanismos de reestimación paramétrica en tiempo real.

