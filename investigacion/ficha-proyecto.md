# Ficha del Proyecto de Investigación

## Información General

| Campo | Valor |
|-------|-------|
| **Título** | Estructuración Formal y Evaluación Estadístico-Experimental de Modelos Ocultos de Markov ante Perturbaciones No Estacionarias: Análisis de Regímenes de Mercado Financiero |
| **Curso** | Simulación |
| **Programa** | Ingeniería de Software y Datos |
| **Institución** | Institución Universitaria Digital de Antioquia (IU Digital) |
| **Fecha** | Noviembre de 2026 |

## Equipo de Trabajo

| Rol | Nombre | Correo |
|-----|--------|--------|
| Estudiante | Sebastian Garces Cadavid | sebastian.garcesc@est.iudigital.edu.co |
| Estudiante | Sofia Miranda Cubides | sofia.miranda@est.iudigital.edu.co |
| Estudiante | Oscar Rene Peñaloza Ardila | oscar.penaloza@est.iudigital.edu.co |
| Estudiante | Andres Mauricio Quintero Rios | andres.quinteror@est.iudigital.edu.co |
| Docente Asesor | Dr. Julián Andrés Loaiza López | julian.loaiza@prof.iudigital.edu.co |

## Descripción del Proyecto

### Problema
Los mercados financieros operan bajo regímenes latentes (alcista, lateral, bajista) que no son directamente observables. Las perturbaciones exógenas como crisis financieras pueden alterar las dinámicas de transición entre estados, degradando la capacidad de los modelos estocásticos para identificar correctamente estos regímenes.

### Objetivo General
Evaluar formalmente el impacto de la no estacionariedad en el rendimiento del algoritmo de Viterbi para la identificación de regímenes de mercado financiero mediante un Modelo Oculto de Markov (HMM).

### Objetivos Específicos
1. Implementar un HMM discreto con topología N=3, M=3 para simulación de regímenes financieros.
2. Diseñar un experimento Monte Carlo con 500 corridas pareadas bajo tres escenarios controlados.
3. Cuantificar la degradación de precisión del algoritmo de Viterbi ante perturbaciones no estacionarias.
4. Comparar la decodificación ciega vs. adaptativa mediante pruebas t pareadas.
5. Generar recomendaciones de trading basadas en los regímenes identificados.

### Metodología
- **Tipo de estudio**: Estadístico-experimental
- **Método**: Simulación Monte Carlo con corridas pareadas
- **Modelo**: HMM discreto (λ = {A, B, π})
- **Algoritmos**: Viterbi (decodificación), Forward (verosimilitud)
- **Escenarios**: Nominal, Crisis no modelada, Crisis modelada
- **Herramientas**: Python 3.x, NumPy, Matplotlib, SciPy, Pandas

### Variables del Experimento
| Variable | Tipo | Valores |
|----------|------|---------|
| Escenario | Independiente | Nominal, Crisis ciego, Crisis adaptativo |
| Precisión global | Dependiente | [0, 1] |
| Precisión en ventana | Dependiente | [0, 1] |
| Períodos (T) | Controlada | 50 |
| Corridas (N) | Controlada | 500 |
| Semilla base | Controlada | 42 |

## Cronograma

| Fase | Actividad | Estado |
|------|-----------|--------|
| 1 | Diagnóstico y planificación | ✅ Completado |
| 2 | Implementación del código | ✅ Completado |
| 3 | Ejecución experimental | ✅ Completado |
| 4 | Análisis de resultados | ✅ Completado |
| 5 | Redacción del artículo | ✅ Completado |
| 6 | Revisión y entrega | 🔄 En curso |

