import numpy as np
import matplotlib.pyplot as plt

def truncate_lists(ecg_bpm, rppg_bpm):
    """
    Trunca las listas de BPM a la misma longitud.

    Args:
        ecg_bpm (list or np.ndarray): Lista o array de BPM obtenidos por ECG.
        rppg_bpm (list or np.ndarray): Lista o array de BPM obtenidos por rPPG.

    Returns:
        tuple: Listas truncadas de BPM.
    """
    min_length = min(len(ecg_bpm), len(rppg_bpm))
    return ecg_bpm[:min_length], rppg_bpm[:min_length]

def calculate_bland_altman(ecg_bpm, rppg_bpm):
    """
    Calcula las estadísticas de Bland-Altman.

    Args:
        ecg_bpm (list or np.ndarray): Lista o array de BPM obtenidos por ECG.
        rppg_bpm (list or np.ndarray): Lista o array de BPM obtenidos por rPPG.

    Returns:
        tuple: Media de BPM, sesgo, límite superior y límite inferior.
    """
    mean_bpm = (ecg_bpm + rppg_bpm) / 2
    bias = rppg_bpm - ecg_bpm
    mean_bias = np.mean(bias)
    std_bias = np.std(bias)
    upper_limit = mean_bias + 1.96 * std_bias
    lower_limit = mean_bias - 1.96 * std_bias
    return mean_bpm, bias, mean_bias, upper_limit, lower_limit

def plot_bland_altman(mean_bpm, bias, mean_bias, upper_limit, lower_limit):
    """
    Grafica el análisis de Bland-Altman.

    Args:
        mean_bpm (np.ndarray): Media de BPM.
        bias (np.ndarray): Sesgo (diferencia entre rPPG y ECG).
        mean_bias (float): Sesgo promedio.
        upper_limit (float): Límite superior (95%).
        lower_limit (float): Límite inferior (95%).
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(mean_bpm, bias, color='blue')
    plt.axhline(mean_bias, color='red', linestyle='--', label='Bias Promedio')
    plt.axhline(upper_limit, color='green', linestyle='--', label='Límite Superior (95%)')
    plt.axhline(lower_limit, color='green', linestyle='--', label='Límite Inferior (95%)')
    plt.title('Análisis de Bland-Altman entre rPPG y ECG')
    plt.xlabel('BPM Promedio')
    plt.ylabel('Diferencia (rPPG - ECG)')
    plt.legend()
    plt.grid(True)
    plt.show()

def grafica_bland_altman(ecg_bpm, rppg_bpm):
    """
    Realiza un análisis de Bland-Altman entre las frecuencias cardíacas obtenidas por ECG y rPPG.

    Args:
        ecg_bpm (list or np.ndarray): Lista o array de BPM obtenidos por ECG.
        rppg_bpm (list or np.ndarray): Lista o array de BPM obtenidos por rPPG.
    """
    ecg_bpm, rppg_bpm = truncate_lists(ecg_bpm, rppg_bpm)
    mean_bpm, bias, mean_bias, upper_limit, lower_limit = calculate_bland_altman(ecg_bpm, rppg_bpm)
    plot_bland_altman(mean_bpm, bias, mean_bias, upper_limit, lower_limit)

