# 📋 Bitácora de Decisiones del Equipo (Trazabilidad Humana)
## Proyecto: Identificación de Regímenes Financieros mediante HMM ante Perturbaciones No Estacionarias
### Curso: Simulación — Semestre 2026-II — IU Digital de Antioquia
### Docente Asesor: Dr. Julián Andrés Loaiza López

---

> **Norma de Registro Metodológico**: Este documento certifica cronológicamente las decisiones formalmente concertadas, expresadas y justificadas por el equipo de investigación en consenso con el docente asesor. Registra únicamente hechos reales, parámetros fijados y verificaciones empíricas del laboratorio de 120 minutos ("Investiga con IA, Decide con criterio").

---

### Registro Cronológico de Decisiones Formales [DEC-01 a DEC-15]

| Código | Decisión Formal del Equipo | Justificación Técnica / Metodológica | Responsables / Quórum | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **DEC-01** | **Topología Discreta HMM ($N=3, M=3$):** Adopción de estados latentes $S = \{\text{Alcista}, \text{Lateral}, \text{Bajista}\}$ y emisiones de retorno $V = \{\text{Positivo}, \text{Neutral}, \text{Negativo}\}$. | Captura las fases macroeconómicas estándar de los mercados bursátiles sin sobreparametrizar el espacio de estados estocásticos. | Equipo completo | **Aprobado** |
| **DEC-02** | **Estabilidad Numérica en Viterbi:** Implementación obligatoria de la recursión en el espacio de log-probabilidades: $\delta_t(j) = \max_i [\delta_{t-1}(i) + \ln a_{ij}] + \ln b_j(O_t)$. | Evita el subdesbordamiento aritmético (*underflow*) causado por la multiplicación encadenada de probabilidades infinitesimales en horizontes $T \ge 50$. | Andres Quintero / Equipo | **Aprobado** |
| **DEC-03** | **Línea Base de Contraste (*Baseline*):** Inclusión de un clasificador determinista reactivo por ventana deslizante ($k=2$) basado en la tendencia de retornos recientes. | Permite una evaluación comparativa justa de Viterbi frente a una regla tradicional univariada de latencia corta utilizada en trading. | Sofia Miranda / Equipo | **Aprobado** |
| **DEC-04** | **Horizonte Temporal ($T=50$ períodos):** Fijación de 50 intervalos de trading por simulación. | Emula un trimestre operativo de mercado con suficiente longitud para observar transiciones de régimen y reversión a la media. | Equipo completo | **Aprobado** |
| **DEC-05** | **Choque No Estacionario (Crisis Temporal):** Inyección de la matriz perturbada $A_{\text{crisis}}$ en la ventana crítica delimitada $t \in [15, 25]$ con fuerte absorción al estado bajista ($a_{33}=0.80$). | Modela rigurosamente la violación de la homogeneidad markoviana temporal inducida por eventos exógenos extremos (crisis de liquidez). | Oscar Peñaloza / Equipo | **Aprobado** |
| **DEC-06** | **Diseño de Escenarios Pareados:** Contraste simultáneo de: (1) Nominal estacionario, (2) Crisis con decodificador ciego, (3) Crisis con decodificador adaptativo $A(t)$. | Aísla cuantitativamente el costo de omitir la no estacionariedad frente a la ganancia de incorporar reestimación adaptativa. | Equipo completo | **Aprobado** |
| **DEC-07** | **Potencia Estadística Monte Carlo ($N=500$):** Protocolo experimental de 500 corridas pareadas con semilla global base fija `seed = 42`. | Garantiza significancia estadística, control estricto de variabilidad exógena y reproducibilidad total de los experimentos. | Sebastian Garces / Equipo | **Aprobado** |
| **DEC-08** | **Inferencia Estadística Rigurosa:** Aplicación de pruebas $t$ de Student pareadas, cálculo del tamaño del efecto ($d$ de Cohen) e intervalos de confianza al 95% ($IC_{95\%}$). | Permite rechazar formalmente la hipótesis nula de equivalencia entre decodificadores controlando la correlación de corridas pareadas. | Equipo completo | **Aprobado** |
| **DEC-09** | **Análisis de Riesgo Financiero Condicionado:** Incorporación de métricas de VaR 95%, VaR 99%, Maximum Drawdown y Sharpe Ratio según el régimen identificado. | Conecta la inferencia estadística del HMM con la toma de decisiones prudenciales de gestión de capital y asignación de portafolios. | Equipo completo | **Aprobado** |
| **DEC-10** | **Resolución Gráfica Editorial (300 DPI):** Exportación de figuras 1, 2 y 3 en alta definición a 300 DPI exactos mediante renderizado estricto. | Satisface las normas internacionales de publicación científica indexada Q1 (claridad vectorial y legibilidad de ejes). | Equipo completo | **Aprobado** |
| **DEC-11** | **Integridad Epistemológica de Fuentes:** Empleo exclusivo de 11 fuentes primarias reales indexadas con DOI (Hamilton 1989, Rabiner 1989, Viterbi 1967, Cont 2001, etc.). | Prohíbe de manera terminante la invención de literatura, citas fantasma o referencias no verificadas en repositorios académicos. | Equipo completo | **Aprobado** |
| **DEC-12** | **Asignación Formal de Autorías del Manuscrito:** <br>1. Sebastian Garces Cadavid (`sebastian.garcesc@est.iudigital.edu.co`) <br>2. Sofia Miranda Cubides (`sofia.miranda@est.iudigital.edu.co`) <br>3. Oscar Rene Peñaloza Ardila (`oscar.penaloza@est.iudigital.edu.co`) <br>4. Andres Mauricio Quintero Rios (`andres.quinteror@est.iudigital.edu.co`). | Estudiantes investigadores del programa de Ingeniería de Software y Datos en el curso de Simulación. | Equipo completo | **Aprobado** |
| **DEC-13** | **Designación del Docente Asesor y Autor de Correspondencia:** Dr. Julián Andrés Loaiza López (`julian.loaiza@prof.iudigital.edu.co`). | Docente titular del curso de Simulación y asesor metodológico institucional de la IU Digital de Antioquia. | Equipo completo | **Aprobado** |
| **DEC-14** | **Construcción de Skill Especializada (Fase 03 / CREA):** Creación e integración de `.agents/skills/evaluar-experimento-hmm/SKILL.md`. | Estandariza la evaluación estadística y la respuesta ética del agente ante datos faltantes en el entorno Antigravity. | Equipo completo | **Aprobado** |
| **DEC-15** | **Sustentación y Tickets de Salida:** Formalización del documento `investigacion/sustentacion-laboratorio.md` con las 5 preguntas del cierre y tickets individuales de salida. | Certifica la apropiación conceptual individual de cada integrante del equipo al cierre de la sesión de 120 minutos. | Equipo completo | **Aprobado** |

---

### Resumen de Archivos Vinculados a la Bitácora
* **Decisiones Humanas del Equipo:** [`investigacion/decisiones/bitacora-decisiones-equipo.md`](file:///d:/IU%20Digital/simulacion/tarea%202/proyecto%20de%20identificacion%20de%20regimenes%20financieros/investigacion/decisiones/bitacora-decisiones-equipo.md) y [`bitacora-decisiones.md`](file:///d:/IU%20Digital/simulacion/tarea%202/proyecto%20de%20identificacion%20de%20regimenes%20financieros/bitacora-decisiones.md)
* **Trazabilidad de Propuestas de la IA:** [`investigacion/decisiones/bitacora-ia.md`](file:///d:/IU%20Digital/simulacion/tarea%202/proyecto%20de%20identificacion%20de%20regimenes%20financieros/investigacion/decisiones/bitacora-ia.md)
* **Evidencia Comparativa Experimental:** [`investigacion/decisiones/comparacion-skills.md`](file:///d:/IU%20Digital/simulacion/tarea%202/proyecto%20de%20identificacion%20de%20regimenes%20financieros/investigacion/decisiones/comparacion-skills.md)
* **Sustentación y Tickets de Salida:** [`investigacion/sustentacion-laboratorio.md`](file:///d:/IU%20Digital/simulacion/tarea%202/proyecto%20de%20identificacion%20de%20regimenes%20financieros/investigacion/sustentacion-laboratorio.md)

---
*Ratificado formalmente por el equipo el 10 de noviembre de 2026.*
