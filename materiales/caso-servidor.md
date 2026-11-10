# Caso de Estudio: Identificación de Regímenes de Mercado Financiero mediante HMM

## Contexto

Los mercados financieros exhiben comportamientos dinámicos que pueden clasificarse en diferentes **regímenes** o estados latentes: períodos alcistas (bull markets), laterales (sideways/range-bound) y bajistas (bear markets). Estos regímenes no son directamente observables, pero se manifiestan a través de señales como los retornos de los activos.

## Problemática

Un gestor de portafolios necesita identificar en tiempo real el régimen de mercado actual para ajustar su estrategia de inversión. Sin embargo:

1. Los regímenes de mercado son **estados ocultos** que no pueden observarse directamente.
2. Solo se dispone de **observaciones ruidosas**: los retornos periódicos del activo.
3. Las transiciones entre regímenes son **estocásticas** y pueden verse afectadas por perturbaciones exógenas (crisis financieras, cambios de política monetaria, eventos geopolíticos).

## Modelo Propuesto

Se propone un **Modelo Oculto de Markov (HMM)** discreto con la siguiente topología:

### Estados ocultos (N = 3)
| Estado | Descripción | Comportamiento típico |
|--------|-------------|----------------------|
| Mercado Alcista | Tendencia ascendente sostenida | Retornos positivos frecuentes, baja volatilidad |
| Mercado Lateral | Sin tendencia definida | Retornos mixtos, volatilidad moderada |
| Mercado Bajista | Tendencia descendente | Retornos negativos frecuentes, alta volatilidad |

### Observaciones discretas (M = 3)
| Observación | Criterio |
|-------------|----------|
| Retorno Positivo | Retorno del período > umbral superior |
| Retorno Neutral | Retorno dentro del rango neutral |
| Retorno Negativo | Retorno del período < umbral inferior |

### Parámetros del modelo

**Matriz de Transición A (3×3):**
```
         Alcista  Lateral  Bajista
Alcista  [ 0.60    0.30     0.10 ]
Lateral  [ 0.30    0.40     0.30 ]
Bajista  [ 0.10    0.30     0.60 ]
```

**Matriz de Emisión B (3×3):**
```
         Positivo  Neutral  Negativo
Alcista  [ 0.70     0.20     0.10 ]
Lateral  [ 0.30     0.40     0.30 ]
Bajista  [ 0.10     0.20     0.70 ]
```

**Distribución inicial π:**
```
π = [Alcista: 0.40, Lateral: 0.30, Bajista: 0.30]
```

## Diseño experimental

### Escenarios de simulación

1. **Escenario Nominal**: Matrices estacionarias durante todo el horizonte (T = 50 períodos).
2. **Escenario de Crisis No Modelada**: Perturbación en la matriz de transición entre los períodos t = 15 y t = 25 (simulando una crisis financiera repentina), con decodificador Viterbi ciego que usa A nominal.
3. **Escenario de Crisis Modelada**: Misma perturbación, pero el decodificador usa una matriz A adaptativa que pondera la crisis.

### Método
- **500 corridas pareadas** de Monte Carlo
- Decodificación con **algoritmo de Viterbi** (log-espacio)
- Evaluación de **precisión global** y **precisión en ventana de crisis**
- **Pruebas t pareadas** para significancia estadística
- **Intervalos de confianza al 95%**

## Pregunta de investigación

¿En qué medida la no estacionariedad de las transiciones de estado (provocada por una perturbación tipo crisis financiera) degrada la precisión del algoritmo de Viterbi en la identificación de regímenes de mercado, y cómo se compara la decodificación ciega frente a una adaptativa?

## Aplicación práctica

Los resultados informan:
- **Gestión de riesgo**: Ajustar la exposición según el régimen identificado.
- **Asignación de activos**: Rotar entre renta variable, renta fija y activos refugio.
- **Sistemas de alerta temprana**: Detectar transiciones hacia regímenes bajistas.

