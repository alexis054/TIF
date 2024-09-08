import cv2
from pyVHR.analysis.pipeline import Pipeline
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def capture_video(output_path='output.avi'):
    """
    Captura video desde la cámara web y lo guarda en un archivo.

    Args:
        output_path (str): La ruta del archivo donde se guardará el video capturado.

    Returns:
        bool: True si la captura fue exitosa, False en caso contrario.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return False

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        cv2.imshow('Captura de Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return True

def process_video(output_path='output.avi'):
    """
    Captura y procesa un video para analizar la frecuencia cardíaca.

    Args:
        output_path (str): La ruta del archivo donde se guardará el video capturado.
    """
    if not capture_video(output_path):
        return

    pipe = Pipeline()
    try:
        time, BPM, uncertainty, bvps, bvps_completa, sig_completa = pipe.run_on_video(
            output_path, roi_method='convexhull', roi_approach='patches'
        )
        plot_bpm(time, BPM, uncertainty)
    except Exception as e:
        print(f"Error durante el procesamiento del video: {e}")

def plot_bpm(time, BPM, uncertainty):
    """
    Grafica la frecuencia cardíaca estimada a lo largo del tiempo.

    Args:
        time (list): Lista de tiempos.
        BPM (list): Lista de valores de frecuencia cardíaca.
        uncertainty (list): Lista de incertidumbres asociadas a los valores de frecuencia cardíaca.
    """
    global canvas, ax  
    ax.clear()
    ax.plot(time, BPM, label='Frecuencia Cardíaca (BPM)', color='blue')
    ax.fill_between(time, BPM - uncertainty, BPM + uncertainty, color='lightblue', alpha=0.5)
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Frecuencia Cardíaca (BPM)')
    ax.set_title('Frecuencia Cardíaca Estimada a lo Largo del Tiempo')
    ax.legend()
    ax.grid()
    canvas.draw()

def create_ui():
    """
    Crea la interfaz gráfica de usuario para la captura y análisis de frecuencia cardíaca.
    """
    global canvas, ax  
    root = tk.Tk()
    root.title("Análisis de Frecuencia Cardíaca")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    container = ttk.Frame(root, padding="20")
    container.pack(fill='both', expand=True)

    result_frame = ttk.Frame(container, padding="10")
    result_frame.pack(fill='x')

    graph_frame = ttk.Frame(container, padding="10")
    graph_frame.pack(fill='both', expand=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title('Gráfica vacía')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Frecuencia Cardíaca (BPM)')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 200)
    ax.grid()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    process_button = ttk.Button(result_frame, text="Iniciar Captura y Análisis", command=process_video)
    process_button.pack(pady=10)

    result_label = ttk.Label(result_frame, text="", font=("Helvetica", 14), background="#f0f0f0")
    result_label.pack(pady=10)

    style = ttk.Style()
    style.configure("TButton", background="lightblue", foreground="black", font=("Helvetica", 12))
    style.configure("TLabel", font=("Helvetica", 14), background="#f0f0f0")
    style.configure("TFrame", background="#f0f0f0")
    result_frame.configure(borderwidth=2, relief="groove")
    graph_frame.configure(borderwidth=2, relief="groove")

    root.mainloop()

# Llamar a la función para crear la interfaz
create_ui()