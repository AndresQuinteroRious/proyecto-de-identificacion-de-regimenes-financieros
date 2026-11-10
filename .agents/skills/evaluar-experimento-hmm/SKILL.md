---
name: evaluar-experimento-hmm
description: Evaluación estadística comparativa y validación de robustez de HMM frente a perturbaciones no estacionarias y clasificadores baseline.
---

# Skill: Evaluar Experimento HMM (Fase 03 - CREA)

## Propósito
Esta skill especializada ejecuta el protocolo de contrastación empírica y validación de hipótesis estadísticas para modelos estocásticos HMM bajo perturbaciones no estacionarias.

## Entradas Necesarias
- Secuencias de observaciones discretas $\{O_t\}$ de longitud $T \ge 50$.
- Parámetros del modelo nominal $\lambda = (A, B, \pi)$.
- Parámetros de perturbación temporal $A_{\text{crisis}}$ en ventana delimitada $[t_1, t_2]$.
- Clasificador determinista de referencia (*Baseline* de ventana deslizante $k=2$).

## Criterios Específicos de Revisión
1. **Estabilidad Numérica**: El algoritmo de Viterbi debe ejecutarse en log-probabilidades para impedir el subdesbordamiento (*underflow*).
2. **Evaluación Comparativa Justa**: Contrastar obligatoriamente frente al baseline heurístico ($k=2$). Ningún HMM se evaluará de forma aislada.
3. **Poder Estadístico**: Ejecutar un mínimo de $N=500$ corridas Monte Carlo pareadas con semilla global fija (`seed = 42`).
4. **Pruebas de Hipótesis**: Reportar estadísticos $t$ pareados, valores $p$, intervalos de confianza al 95% ($IC_{95\%}$) y tamaño del efecto mediante $d$ de Cohen.

## Decisiones Reservadas al Investigador
- Definición de la ventana de perturbación y magnitud del shock exógeno.
- Interpretación prudencial de las recomendaciones operativas y límites del modelo.
- Selección de fuentes académicas indexadas (mínimo 11 referencias reales verificadas).

## Comportamiento ante Evidencia Faltante
Si un conjunto de datos real no está disponible o faltan etiquetas de estado verdadero, la skill **no inventará mediciones ni asumirá certezas analíticas**. Reportará explícitamente que se trata de un escenario simulado con parámetros didácticos/hipotéticos.

