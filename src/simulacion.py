"""
Modelo Oculto de Markov (HMM) para Identificación de Regímenes de Mercado Financiero.

Autores:
    - Sebastian Garces Cadavid (sebastian.garces@est.iudigital.edu.co)
    - Sofia Miranda Cubides (sofia.miranda@est.iudigital.edu.co)
    - Oscar Rene Peñaloza Ardila (oscar.penaloza@est.iudigital.edu.co)
    - Andres Mauricio Quintero Rios (andres.quintero@est.iudigital.edu.co)

Docente Asesor:
    - Dr. Julián Andrés Loaiza López (julian.loaiza@prof.iudigital.edu.co)

Institución:
    Institución Universitaria Digital de Antioquia (IU Digital)
    Facultad de Ingeniería — Simulación — Noviembre 2026

Descripción:
    Implementa un HMM discreto con N=3 estados latentes (Alcista, Lateral, Bajista)
    y M=3 emisiones (Retorno Positivo, Neutral, Negativo).
    Incluye:
    - Algoritmo de Viterbi numéricamente estable en log-probabilidades (evita underflow).
    - Baseline heurístico determinista de ventana deslizante (k=2) como contraste operacional.
    - Simulación Monte Carlo pareada (500 corridas, T=50 períodos) bajo tres escenarios:
        1. Nominal (estacionario).
        2. Crisis no modelada (perturbación exógena con decodificador ciego).
        3. Crisis modelada (decodificador adaptativo dependiente de régimen).
    - Pruebas t pareadas, d de Cohen e intervalos de confianza al 95%.
    - Generación de figuras individuales a 300 DPI y archivos CSV.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import warnings
import argparse
import os
from typing import Tuple, List, Dict, Optional

warnings.filterwarnings('ignore')


# =============================================================================
# CLASE PRINCIPAL: HMM PARA MERCADOS FINANCIEROS
# =============================================================================

class HMMFinanciero:
    """
    Modelo Oculto de Markov discreto formalizado como λ = (S, V, A, B, π).

    Topología:
        - S = {Alcista, Lateral, Bajista} (N = 3)
        - V = {Positivo, Neutral, Negativo} (M = 3)
    """

    def __init__(self,
                 A: Optional[np.ndarray] = None,
                 B: Optional[np.ndarray] = None,
                 pi: Optional[np.ndarray] = None,
                 T: int = 50):
        self.estados = ['Mercado Alcista', 'Mercado Lateral', 'Mercado Bajista']
        self.observaciones = ['Retorno Positivo', 'Retorno Neutral', 'Retorno Negativo']
        self.N = len(self.estados)
        self.M = len(self.observaciones)
        self.T = T

        # Paleta editorial formal
        self.colores_estado = {
            0: '#2ecc71',  # Verde - Alcista
            1: '#f39c12',  # Ámbar - Lateral
            2: '#e74c3c',  # Rojo - Bajista
        }

        # Matriz de Transición Nominal A (3x3)
        if A is not None:
            self.A = np.array(A, dtype=np.float64)
        else:
            self.A = np.array([
                [0.60, 0.30, 0.10],  # Alcista
                [0.30, 0.40, 0.30],  # Lateral
                [0.10, 0.30, 0.60],  # Bajista
            ], dtype=np.float64)

        # Matriz de Emisión B (3x3)
        if B is not None:
            self.B = np.array(B, dtype=np.float64)
        else:
            self.B = np.array([
                [0.70, 0.20, 0.10],  # Alcista -> Pos, Neu, Neg
                [0.30, 0.40, 0.30],  # Lateral -> Pos, Neu, Neg
                [0.10, 0.20, 0.70],  # Bajista -> Pos, Neu, Neg
            ], dtype=np.float64)

        # Distribución Inicial π (1x3)
        if pi is not None:
            self.pi = np.array(pi, dtype=np.float64)
        else:
            self.pi = np.array([0.40, 0.30, 0.30], dtype=np.float64)

        self._validar_modelo()

    def _validar_modelo(self):
        """Valida que las filas sean estocásticas."""
        for i in range(self.N):
            assert np.isclose(self.A[i].sum(), 1.0), f"Fila {i} de A no suma 1"
            assert np.isclose(self.B[i].sum(), 1.0), f"Fila {i} de B no suma 1"
        assert np.isclose(self.pi.sum(), 1.0), "pi no suma 1"

    def simular(self, T: Optional[int] = None, seed: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Generación estocástica forward de secuencias de estados y observaciones."""
        if T is None:
            T = self.T
        if seed is not None:
            np.random.seed(seed)

        estados_seq = np.zeros(T, dtype=int)
        obs_seq = np.zeros(T, dtype=int)

        estados_seq[0] = np.random.choice(self.N, p=self.pi)
        obs_seq[0] = np.random.choice(self.M, p=self.B[estados_seq[0]])

        for t in range(1, T):
            estados_seq[t] = np.random.choice(self.N, p=self.A[estados_seq[t - 1]])
            obs_seq[t] = np.random.choice(self.M, p=self.B[estados_seq[t]])

        return estados_seq, obs_seq

    def generar_precios(self, estados_seq: np.ndarray, obs_seq: np.ndarray,
                        precio_inicial: float = 100.0) -> Tuple[np.ndarray, np.ndarray]:
        """Genera precios geométricos brownianos condicionados al régimen latente."""
        T = len(estados_seq)
        params = {
            0: (0.020, 0.010),   # Alcista: μ=2.0%, σ=1.0%
            1: (0.000, 0.008),   # Lateral: μ=0.0%, σ=0.8%
            2: (-0.020, 0.015),  # Bajista: μ=-2.0%, σ=1.5%
        }
        mod_obs = {0: 0.004, 1: 0.0, 2: -0.004}

        precios = np.zeros(T + 1)
        precios[0] = precio_inicial
        retornos = np.zeros(T)

        for t in range(T):
            mu, sigma = params[estados_seq[t]]
            mod = mod_obs[obs_seq[t]]
            retorno = np.random.normal(mu + mod, sigma)
            retornos[t] = retorno
            precios[t + 1] = precios[t] * (1.0 + retorno)

        return precios, retornos

    def viterbi(self, obs_seq: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Algoritmo de Viterbi exacto en log-probabilidades para prevenir underflow numérico.
        """
        T = len(obs_seq)
        delta = np.zeros((T, self.N))
        psi = np.zeros((T, self.N), dtype=int)

        eps = 1e-300
        delta[0] = np.log(self.pi + eps) + np.log(self.B[:, obs_seq[0]] + eps)

        for t in range(1, T):
            for j in range(self.N):
                trans_probs = delta[t - 1] + np.log(self.A[:, j] + eps)
                psi[t, j] = np.argmax(trans_probs)
                delta[t, j] = trans_probs[psi[t, j]] + np.log(self.B[j, obs_seq[t]] + eps)

        path = np.zeros(T, dtype=int)
        path[T - 1] = np.argmax(delta[T - 1])
        log_prob = delta[T - 1, path[T - 1]]

        for t in range(T - 2, -1, -1):
            path[t] = psi[t + 1, path[t + 1]]

        return path, log_prob

    def baseline_heuristico_ventana(self, obs_seq: np.ndarray, k: int = 2) -> np.ndarray:
        """
        Línea base operacional: Clasificador heurístico determinista por ventana deslizante (k=2).
        Regla:
            - Si las últimas k observaciones son mayoritariamente Retorno Positivo (0) -> Alcista (0)
            - Si las últimas k observaciones son mayoritariamente Retorno Negativo (2) -> Bajista (2)
            - En cualquier otro caso (o mezcla con neutral) -> Lateral (1)
        """
        T = len(obs_seq)
        pred_heuristica = np.zeros(T, dtype=int)

        for t in range(T):
            if t == 0:
                # Regla univariada instantánea
                if obs_seq[t] == 0:
                    pred_heuristica[t] = 0
                elif obs_seq[t] == 2:
                    pred_heuristica[t] = 2
                else:
                    pred_heuristica[t] = 1
            else:
                inicio = max(0, t - k + 1)
                ventana = obs_seq[inicio:t + 1]
                cuenta_pos = np.sum(ventana == 0)
                cuenta_neg = np.sum(ventana == 2)

                if cuenta_pos > len(ventana) / 2:
                    pred_heuristica[t] = 0
                elif cuenta_neg > len(ventana) / 2:
                    pred_heuristica[t] = 2
                else:
                    pred_heuristica[t] = 1

        return pred_heuristica

    def calcular_metricas(self, estados_reales: np.ndarray, estados_estimados: np.ndarray) -> Dict:
        """Calcula precisión global y por clase."""
        T = len(estados_reales)
        aciertos = np.sum(estados_reales == estados_estimados)
        precision_global = aciertos / T

        prec_por_estado = {}
        for i in range(self.N):
            mask = estados_reales == i
            prec_por_estado[self.estados[i]] = (
                np.sum(estados_estimados[mask] == i) / mask.sum() if mask.sum() > 0 else np.nan
            )

        return {
            'precision_global': precision_global,
            'precision_por_estado': prec_por_estado,
            'aciertos': int(aciertos),
            'total': T
        }

    def analisis_riesgo(self, estados_seq: np.ndarray, retornos: np.ndarray, precios: np.ndarray) -> Dict:
        """Calcula VaR, CVaR, Sharpe y Drawdown condicionado por régimen."""
        ret_total = (precios[-1] / precios[0]) - 1.0
        vol_global = np.std(retornos)
        sharpe = (np.mean(retornos) / vol_global) if vol_global > 0 else 0.0

        picos = np.maximum.accumulate(precios)
        drawdowns = (precios - picos) / picos
        max_dd = np.min(drawdowns)

        por_regimen = {}
        for i in range(self.N):
            mask = (estados_seq == i)
            if mask.sum() > 0:
                ret_k = retornos[mask]
                por_regimen[self.estados[i]] = {
                    'periodos': int(mask.sum()),
                    'proporcion': float(mask.sum() / len(estados_seq)),
                    'retorno_medio': float(np.mean(ret_k)),
                    'volatilidad': float(np.std(ret_k)),
                    'var_95': float(np.percentile(ret_k, 5)) if len(ret_k) > 1 else np.nan
                }

        return {
            'retorno_total': float(ret_total),
            'volatilidad_global': float(vol_global),
            'var_95': float(np.percentile(retornos, 5)),
            'var_99': float(np.percentile(retornos, 1)),
            'max_drawdown': float(max_dd),
            'sharpe_ratio': float(sharpe),
            'por_regimen': por_regimen
        }

    def generar_recomendaciones(self, estado_actual: int, riesgo: Dict) -> Dict:
        """Genera directrices operativas según el régimen latente inferido."""
        recs = {
            0: {
                'estado': 'Mercado Alcista',
                'color': '🟢',
                'posicion': 'COMPRA (Long)',
                'exposicion': 'Alta (80% - 100%)',
                'stop_loss': '-3.0%',
                'take_profit': '+6.0%',
                'estrategia': 'Seguimiento de tendencia. Optimización de beta y mantenimiento de posiciones largas.',
                'nivel_riesgo': 'BAJO'
            },
            1: {
                'estado': 'Mercado Lateral',
                'color': '🟡',
                'posicion': 'NEUTRAL / RANGO',
                'exposicion': 'Moderada (40% - 50%)',
                'stop_loss': '-2.0%',
                'take_profit': '+2.5%',
                'estrategia': 'Estrategias de reversión a la media, spreads y captura de primas en canales.',
                'nivel_riesgo': 'MEDIO'
            },
            2: {
                'estado': 'Mercado Bajista',
                'color': '🔴',
                'posicion': 'VENTA / COBERTURA (Short/Cash)',
                'exposicion': 'Mínima (0% - 15%) o Activos Refugio',
                'stop_loss': '-4.0%',
                'take_profit': '+7.0%',
                'estrategia': 'Preservación de capital. Coberturas dinámicas con derivados y rotación a liquidez.',
                'nivel_riesgo': 'ALTO'
            }
        }
        r = recs[estado_actual]
        r['max_drawdown'] = f"{riesgo['max_drawdown']:.2%}"
        r['sharpe'] = f"{riesgo['sharpe_ratio']:.3f}"
        return r


# =============================================================================
# EXPERIMENTO MONTE CARLO Y EVALUACIÓN COMPARATIVA
# =============================================================================

class ExperimentoMonteCarloFinanciero:
    """
    Marco experimental pareado de 500 corridas Monte Carlo para contrastar
    HMM Viterbi frente a perturbación no estacionaria y clasificador heurístico baseline.
    """

    def __init__(self, hmm: HMMFinanciero, n_corridas: int = 500, seed_base: int = 42):
        self.hmm = hmm
        self.n_corridas = n_corridas
        self.seed_base = seed_base
        self.t_inicio_crisis = 15
        self.t_fin_crisis = 25

        # Matriz de perturbación en crisis: fuga masiva al estado bajista
        self.A_crisis = np.array([
            [0.20, 0.30, 0.50],  # Alcista colapsa a Bajista con prob 0.50
            [0.10, 0.30, 0.60],  # Lateral cae a Bajista con prob 0.60
            [0.05, 0.15, 0.80],  # Bajista queda atrapado con prob 0.80
        ], dtype=np.float64)

    def simular_crisis(self, seed: int) -> Tuple[np.ndarray, np.ndarray]:
        """Simula proceso estocástico no homogéneo en el tiempo."""
        np.random.seed(seed)
        T = self.hmm.T
        estados = np.zeros(T, dtype=int)
        obs = np.zeros(T, dtype=int)

        estados[0] = np.random.choice(self.hmm.N, p=self.hmm.pi)
        obs[0] = np.random.choice(self.hmm.M, p=self.hmm.B[estados[0]])

        for t in range(1, T):
            A_t = self.A_crisis if (self.t_inicio_crisis <= t <= self.t_fin_crisis) else self.hmm.A
            estados[t] = np.random.choice(self.hmm.N, p=A_t[estados[t - 1]])
            obs[t] = np.random.choice(self.hmm.M, p=self.hmm.B[estados[t]])

        return estados, obs

    def ejecutar(self) -> pd.DataFrame:
        """Ejecuta las corridas pareadas para los 3 escenarios + baseline heurístico."""
        registros = []
        T = self.hmm.T
        mask_crisis = np.zeros(T, dtype=bool)
        mask_crisis[self.t_inicio_crisis:self.t_fin_crisis + 1] = True

        # HMM adaptativo ponderado
        t_crisis = self.t_fin_crisis - self.t_inicio_crisis + 1
        A_adaptativa = ((T - t_crisis) * self.hmm.A + t_crisis * self.A_crisis) / T
        A_adaptativa /= A_adaptativa.sum(axis=1, keepdims=True)
        hmm_adaptativo = HMMFinanciero(A=A_adaptativa, B=self.hmm.B, pi=self.hmm.pi, T=T)

        for i in range(self.n_corridas):
            seed = self.seed_base + i

            # 1. Nominal
            est_nom, obs_nom = self.hmm.simular(seed=seed)
            vit_nom, _ = self.hmm.viterbi(obs_nom)
            heur_nom = self.hmm.baseline_heuristico_ventana(obs_nom, k=2)

            prec_nom = np.mean(est_nom == vit_nom)
            prec_heur_nom = np.mean(est_nom == heur_nom)

            # 2. Crisis (simulación idéntica para Ciego y Adaptativo)
            est_cr, obs_cr = self.simular_crisis(seed)
            vit_ciego, _ = self.hmm.viterbi(obs_cr)
            vit_adapt, _ = hmm_adaptativo.viterbi(obs_cr)
            heur_cr = self.hmm.baseline_heuristico_ventana(obs_cr, k=2)

            prec_cr_ciego = np.mean(est_cr == vit_ciego)
            prec_cr_adapt = np.mean(est_cr == vit_adapt)
            prec_cr_heur = np.mean(est_cr == heur_cr)

            # Métricas en ventana crítica de crisis [t=15 a t=25]
            prec_vent_ciego = np.mean(est_cr[mask_crisis] == vit_ciego[mask_crisis])
            prec_vent_adapt = np.mean(est_cr[mask_crisis] == vit_adapt[mask_crisis])
            prec_vent_heur = np.mean(est_cr[mask_crisis] == heur_cr[mask_crisis])

            registros.append({
                'corrida': i + 1,
                'seed': seed,
                'precision_nominal': prec_nom,
                'precision_nominal_heuristica': prec_heur_nom,
                'precision_crisis_ciego': prec_cr_ciego,
                'precision_crisis_adaptativo': prec_cr_adapt,
                'precision_crisis_heuristica': prec_cr_heur,
                'precision_ventana_ciego': prec_vent_ciego,
                'precision_ventana_adaptativo': prec_vent_adapt,
                'precision_ventana_heuristica': prec_vent_heur,
            })

        return pd.DataFrame(registros)

    def tabla_resumen(self, df: pd.DataFrame) -> pd.DataFrame:
        """Tabla descriptiva con IC del 95%."""
        columnas = [
            'precision_nominal', 'precision_nominal_heuristica',
            'precision_crisis_ciego', 'precision_crisis_adaptativo', 'precision_crisis_heuristica',
            'precision_ventana_ciego', 'precision_ventana_adaptativo', 'precision_ventana_heuristica'
        ]
        filas = []
        for col in columnas:
            data = df[col]
            ic = stats.t.interval(0.95, len(data) - 1, loc=data.mean(), scale=stats.sem(data))
            filas.append({
                'metrica': col,
                'media': float(data.mean()),
                'std': float(data.std()),
                'mediana': float(data.median()),
                'min': float(data.min()),
                'max': float(data.max()),
                'ic_95_inf': float(ic[0]),
                'ic_95_sup': float(ic[1]),
            })
        return pd.DataFrame(filas)

    def pruebas_hipotesis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Pruebas t pareadas formales."""
        pares = [
            ('precision_nominal', 'precision_nominal_heuristica', 'Nominal: Viterbi vs Heurística Baseline'),
            ('precision_nominal', 'precision_crisis_ciego', 'Nominal vs Crisis Ciego'),
            ('precision_nominal', 'precision_crisis_adaptativo', 'Nominal vs Crisis Adaptativo'),
            ('precision_crisis_ciego', 'precision_crisis_adaptativo', 'Crisis Ciego vs Crisis Adaptativo'),
            ('precision_ventana_ciego', 'precision_ventana_adaptativo', 'Ventana Crisis: Ciego vs Adaptativo'),
            ('precision_ventana_adaptativo', 'precision_ventana_heuristica', 'Ventana Crisis: Adaptativo vs Heurística')
        ]
        res = []
        for c1, c2, nombre in pares:
            diff = df[c1] - df[c2]
            t_val, p_val = stats.ttest_rel(df[c1], df[c2])
            cohen = diff.mean() / diff.std() if diff.std() > 0 else 0.0
            res.append({
                'comparacion': nombre,
                'diferencia_medias': float(diff.mean()),
                't_statistic': float(t_val),
                'p_value': float(p_val),
                'cohens_d': float(cohen),
                'significativo_005': bool(p_val < 0.05)
            })
        return pd.DataFrame(res)


# =============================================================================
# GENERACIÓN DE GRÁFICOS FORMALES INDIVIDUALES (300 DPI)
# =============================================================================

def generar_figuras_articulo(hmm: HMMFinanciero, df_res: pd.DataFrame,
                             precios: np.ndarray, estados: np.ndarray,
                             obs: np.ndarray, viterbi_seq: np.ndarray,
                             salida: str = '.'):
    """
    Genera las 3 figuras requeridas con resolución 300 DPI:
        - Figura 1: precision_global_ventana.png
        - Figura 2: precision_paso_a_paso.png
        - Figura 3: corrida_individual.png
    """
    os.makedirs(salida, exist_ok=True)
    T = len(estados)

    # -------------------------------------------------------------------------
    # FIGURA 3: corrida_individual.png (Trayectoria, estados latentes y retornos)
    # -------------------------------------------------------------------------
    fig3, axes3 = plt.subplots(3, 1, figsize=(12, 8), sharex=True,
                               gridspec_kw={'height_ratios': [3, 0.8, 0.8]})

    # Panel A: Serie de precios
    ax_p = axes3[0]
    ax_p.plot(range(T + 1), precios, color='#1a252f', linewidth=2.0, label='Precio Simulado S(t)')
    for t in range(T):
        ax_p.axvspan(t, t + 1, color=hmm.colores_estado[estados[t]], alpha=0.22)
    ax_p.set_ylabel('Nivel de Precio ($)', fontsize=11, fontweight='bold')
    ax_p.set_title('Figura 3. Corrida Representativa del Proceso HMM y Régimen de Mercado Latente (T=50)',
                   fontsize=12, fontweight='bold', pad=12)
    ax_p.grid(True, linestyle='--', alpha=0.4)

    p1 = mpatches.Patch(color='#2ecc71', alpha=0.6, label='Mercado Alcista (S₁)')
    p2 = mpatches.Patch(color='#f39c12', alpha=0.6, label='Mercado Lateral (S₂)')
    p3 = mpatches.Patch(color='#e74c3c', alpha=0.6, label='Mercado Bajista (S₃)')
    ax_p.legend(handles=[p1, p2, p3], loc='upper left', framealpha=0.9, fontsize=9)

    # Panel B: Estados reales vs decodificados
    ax_s = axes3[1]
    colores_reales = [hmm.colores_estado[s] for s in estados]
    ax_s.bar(range(T), np.ones(T), color=colores_reales, width=1.0, align='edge')
    errores = np.where(estados != viterbi_seq)[0]
    if len(errores) > 0:
        ax_s.scatter(errores + 0.5, [0.5] * len(errores), color='black', marker='x',
                     s=45, label=f'Error Viterbi ({len(errores)} desaciertos)')
        ax_s.legend(loc='upper right', fontsize=8)
    ax_s.set_ylabel('Estado S(t)', fontsize=10, fontweight='bold')
    ax_s.set_yticks([])

    # Panel C: Emisiones discretas observadas
    ax_o = axes3[2]
    col_obs_map = {0: '#27ae60', 1: '#7f8c8d', 2: '#c0392b'}
    colores_obs = [col_obs_map[o] for o in obs]
    ax_o.bar(range(T), np.ones(T), color=colores_obs, width=1.0, align='edge')
    ax_o.set_ylabel('Retorno O(t)', fontsize=10, fontweight='bold')
    ax_o.set_xlabel('Período Discreto de Simulación (t)', fontsize=11, fontweight='bold')
    ax_o.set_yticks([])
    ax_o.set_xlim(0, T)

    po1 = mpatches.Patch(color='#27ae60', label='Retorno Positivo (v₁)')
    po2 = mpatches.Patch(color='#7f8c8d', label='Retorno Neutral (v₂)')
    po3 = mpatches.Patch(color='#c0392b', label='Retorno Negativo (v₃)')
    ax_o.legend(handles=[po1, po2, po3], loc='upper right', fontsize=8, ncol=3)

    plt.tight_layout()
    ruta_fig3 = os.path.join(salida, 'corrida_individual.png')
    fig3.savefig(ruta_fig3, dpi=300, bbox_inches='tight')
    plt.close(fig3)
    print(f" [OK] Figura 3 generada: {ruta_fig3} (300 DPI)")

    # -------------------------------------------------------------------------
    # FIGURA 1: precision_global_ventana.png (Distribución global y ventana crítica)
    # -------------------------------------------------------------------------
    fig1, (ax1_a, ax1_b) = plt.subplots(1, 2, figsize=(13, 5))

    # Panel Izquierdo: Histogramas KDE globales
    ax1_a.hist(df_res['precision_nominal'], bins=25, alpha=0.55, color='#2ecc71',
               label='Nominal (Estacionario)', edgecolor='black', density=True)
    ax1_a.hist(df_res['precision_crisis_ciego'], bins=25, alpha=0.55, color='#e74c3c',
               label='Crisis (Decodificador Ciego)', edgecolor='black', density=True)
    ax1_a.hist(df_res['precision_crisis_adaptativo'], bins=25, alpha=0.55, color='#2980b9',
               label='Crisis (Adaptativo A(t))', edgecolor='black', density=True)
    ax1_a.set_title('A) Densidad de Precisión Global (N=500)', fontsize=11, fontweight='bold')
    ax1_a.set_xlabel('Precisión Global de Inferencia', fontsize=10)
    ax1_a.set_ylabel('Densidad empírica', fontsize=10)
    ax1_a.grid(True, linestyle=':', alpha=0.5)
    ax1_a.legend(fontsize=9, loc='upper left')

    # Panel Derecho: Boxplot comparativo en ventana crítica t ∈ [15, 25]
    bp_data = [
        df_res['precision_ventana_heuristica'],
        df_res['precision_ventana_ciego'],
        df_res['precision_ventana_adaptativo']
    ]
    bp = ax1_b.boxplot(bp_data, labels=['Heurística (k=2)', 'Viterbi Ciego', 'Viterbi Adaptativo'],
                       patch_artist=True, medianprops=dict(color='black', linewidth=1.5))
    colores_box = ['#95a5a6', '#e74c3c', '#2980b9']
    for patch, c in zip(bp['boxes'], colores_box):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
    ax1_b.set_title('B) Rendimiento en Ventana Crítica de Crisis [t=15 a t=25]',
                    fontsize=11, fontweight='bold')
    ax1_b.set_ylabel('Precisión Local', fontsize=10)
    ax1_b.grid(True, linestyle=':', alpha=0.5)

    plt.suptitle('Figura 1. Evaluación Comparativa de Precisión Global y en Ventana Crítica',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    ruta_fig1 = os.path.join(salida, 'precision_global_ventana.png')
    fig1.savefig(ruta_fig1, dpi=300, bbox_inches='tight')
    plt.close(fig1)
    print(f" [OK] Figura 1 generada: {ruta_fig1} (300 DPI)")

    # -------------------------------------------------------------------------
    # FIGURA 2: precision_paso_a_paso.png (Trayectoria temporal paso a paso)
    # -------------------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(12, 5))

    # Computar precisión promedio período a período sobre 100 corridas
    n_sub = 100
    acc_paso_nom = np.zeros((n_sub, T))
    acc_paso_cr_ciego = np.zeros((n_sub, T))
    acc_paso_cr_adapt = np.zeros((n_sub, T))
    acc_paso_heur = np.zeros((n_sub, T))

    exp_temp = ExperimentoMonteCarloFinanciero(hmm, n_corridas=n_sub, seed_base=42)
    t_crisis = exp_temp.t_fin_crisis - exp_temp.t_inicio_crisis + 1
    A_ad = ((T - t_crisis) * hmm.A + t_crisis * exp_temp.A_crisis) / T
    A_ad /= A_ad.sum(axis=1, keepdims=True)
    hmm_ad = HMMFinanciero(A=A_ad, B=hmm.B, pi=hmm.pi, T=T)

    for k in range(n_sub):
        s = 42 + k
        # Nominal
        en, on = hmm.simular(seed=s)
        vn, _ = hmm.viterbi(on)
        acc_paso_nom[k] = (en == vn).astype(float)

        # Crisis
        ec, oc = exp_temp.simular_crisis(seed=s)
        vc, _ = hmm.viterbi(oc)
        va, _ = hmm_ad.viterbi(oc)
        vh = hmm.baseline_heuristico_ventana(oc, k=2)

        acc_paso_cr_ciego[k] = (ec == vc).astype(float)
        acc_paso_cr_adapt[k] = (ec == va).astype(float)
        acc_paso_heur[k] = (ec == vh).astype(float)

    media_nom = acc_paso_nom.mean(axis=0)
    media_cr_ciego = acc_paso_cr_ciego.mean(axis=0)
    media_cr_adapt = acc_paso_cr_adapt.mean(axis=0)
    media_heur = acc_paso_heur.mean(axis=0)

    t_axis = range(1, T + 1)
    ax2.plot(t_axis, media_nom, label='Nominal (A estacionaria)', color='#2ecc71', linewidth=2.0)
    ax2.plot(t_axis, media_cr_ciego, label='Crisis (Viterbi Ciego)', color='#e74c3c', linewidth=2.0, linestyle='--')
    ax2.plot(t_axis, media_cr_adapt, label='Crisis (Viterbi Adaptativo)', color='#2980b9', linewidth=2.2)
    ax2.plot(t_axis, media_heur, label='Baseline Heurístico (k=2)', color='#7f8c8d', linewidth=1.5, linestyle=':')

    # Sombrear la ventana de perturbación no estacionaria [15, 25]
    ax2.axvspan(15, 25, color='#e74c3c', alpha=0.15, label='Ventana de Perturbación [t=15 a 25]')
    ax2.set_xlabel('Período de Trading (t)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Precisión Media Paso a Paso', fontsize=11, fontweight='bold')
    ax2.set_title('Figura 2. Dinámica Temporal de Precisión Paso a Paso ante Perturbación Exógena',
                  fontsize=12, fontweight='bold', pad=12)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.set_ylim(0.2, 0.95)
    ax2.legend(loc='lower left', framealpha=0.9, fontsize=9, ncol=2)

    plt.tight_layout()
    ruta_fig2 = os.path.join(salida, 'precision_paso_a_paso.png')
    fig2.savefig(ruta_fig2, dpi=300, bbox_inches='tight')
    plt.close(fig2)
    print(f" [OK] Figura 2 generada: {ruta_fig2} (300 DPI)")


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

def main(T: int = 50, seed: int = 42, n_corridas: int = 500, salida: str = '.'):
    print("=" * 75)
    print("  HMM FINANCIERO: EVALUACIÓN ESTADÍSTICO-EXPERIMENTAL Y MONTE CARLO")
    print("  IU Digital de Antioquia — Curso de Simulación — Noviembre 2026")
    print("=" * 75)

    os.makedirs(salida, exist_ok=True)

    # 1. Instanciación y simulación representativa
    hmm = HMMFinanciero(T=T)
    estados_rep, obs_rep = hmm.simular(seed=seed)
    precios_rep, retornos_rep = hmm.generar_precios(estados_rep, obs_rep)
    viterbi_rep, log_prob = hmm.viterbi(obs_rep)

    metr = hmm.calcular_metricas(estados_rep, viterbi_rep)
    riesgo = hmm.analisis_riesgo(estados_rep, retornos_rep, precios_rep)
    rec = hmm.generar_recomendaciones(estados_rep[-1], riesgo)

    print(f"\n[Corrida Representativa (seed={seed})]")
    print(f" - Precisión Viterbi Global: {metr['precision_global']:.2%}")
    print(f" - Log-Verosimilitud:        {log_prob:.4f}")
    print(f" - Régimen Final:            {rec['color']} {rec['estado']} -> {rec['posicion']}")
    print(f" - Sharpe Ratio:             {riesgo['sharpe_ratio']:.3f} | Max Drawdown: {riesgo['max_drawdown']:.2%}")

    # 2. Experimento Monte Carlo de 500 corridas pareadas
    print(f"\n[Ejecutando Monte Carlo Pareado ({n_corridas} corridas)...]")
    exp = ExperimentoMonteCarloFinanciero(hmm, n_corridas=n_corridas, seed_base=seed)
    df_crudos = exp.ejecutar()
    df_resumen = exp.tabla_resumen(df_crudos)
    df_hip = exp.pruebas_hipotesis(df_crudos)

    # Exportación de CSVs
    p_crudos = os.path.join(salida, 'resultados_crudos.csv')
    p_resumen = os.path.join(salida, 'tabla_resumen.csv')
    p_hip = os.path.join(salida, 'pruebas_hipotesis.csv')

    df_crudos.to_csv(p_crudos, index=False)
    df_resumen.to_csv(p_resumen, index=False)
    df_hip.to_csv(p_hip, index=False)

    print(" [OK] CSVs exportados:")
    print(f"   -> {p_crudos}")
    print(f"   -> {p_resumen}")
    print(f"   -> {p_hip}")

    # 3. Generación de las 3 figuras requeridas a 300 DPI
    print("\n[Generando Figuras Formales a 300 DPI...]")
    generar_figuras_articulo(hmm, df_crudos, precios_rep, estados_rep, obs_rep, viterbi_rep, salida=salida)

    print("\n" + "=" * 75)
    print("  SIMULACIÓN Y GENERACIÓN COMPLETADA CON ÉXITO")
    print("=" * 75)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HMM de Regímenes Financieros')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--periodos', type=int, default=50)
    parser.add_argument('--corridas', type=int, default=500)
    parser.add_argument('--salida', type=str, default='.')
    args = parser.parse_args()

    main(T=args.periodos, seed=args.seed, n_corridas=args.corridas, salida=args.salida)
