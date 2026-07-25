# Face Detector Intelligent Home

Sistema de reconocimiento facial en tiempo real que detecta personas registradas
a través de la cámara y dispara acciones personalizadas al reconocerlas
(por ejemplo, reproducir música al detectar a "Messi").

## Requisitos

- Python 3.10 (recomendado; `dlib` puede dar problemas de compilación en
  versiones muy nuevas de Python en Windows)
- Una cámara web (integrada o USB)
- Windows / macOS / Linux

## Instalación

1. **Clonar o descargar el proyecto** y ubicarte en su carpeta:

   ```bash
   cd Face_Detector_Intelligent_Home
   ```

2. **Crear y activar un entorno virtual**

   En Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   En macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

   > **Nota sobre `dlib`/`face_recognition` en Windows**: si `pip install dlib`
   > falla, necesitas tener instalado **CMake** y **Visual Studio Build Tools**
   > (con soporte de C++) antes de instalar, o usar una rueda (`.whl`)
   > precompilada para tu versión de Python.

## Estructura de carpetas esperada

```
Face_Detector_Intelligent_Home/
├── main.py
├── requirements.txt
├── README.md
├── images/
│   └── messi.jpg          # foto de referencia de cada persona a registrar
└── music/
    └── De_Musica_Ligera.mp3   # audio que se reproduce al reconocer a Messi
```

- **`images/`**: coloca aquí una foto clara y de frente de cada persona que
  quieras registrar. El nombre del archivo no importa, pero debe verse
  claramente el rostro.
- **`music/`**: coloca aquí los archivos de audio que se reproducirán al
  reconocer a cada persona.

## Configuración antes de ejecutar

Abre `main.py` y revisa estos puntos:

1. **Registrar rostros** — agrega una línea por cada persona:
   ```python
   registrar_rostro("images/messi.jpg", "Messi")
   registrar_rostro("images/elon.jpg", "Elon Musk")
   ```

2. **Cámara a usar** — `VideoStream(0)` usa la cámara por defecto del equipo;
   `VideoStream(1)` usa una segunda cámara (por ejemplo, una webcam USB externa
   cuando también existe una integrada). Ajusta el número según tu equipo.

3. **Acciones personalizadas** — la clase `PersonAction` define qué pasa al
   reconocer a cada persona. Agrega un método nuevo por persona y engánchalo
   en el bloque `if name == "...":` dentro del bucle principal.

## Ejecución

Con el entorno virtual activado:

```bash
python main.py
```

- Se abrirá una ventana con el video de la cámara.
- Los rostros reconocidos se marcan con un cuadro **verde** y su nombre;
  los no reconocidos, con un cuadro **rojo** y la etiqueta "Desconocido".
- Al reconocer por primera vez a una persona registrada, se ejecuta su
  acción asociada (por ejemplo, reproducir música). La acción no se repite
  mientras la persona siga en cuadro; vuelve a dispararse si sale y regresa.
- Presiona **`q`** con la ventana de video enfocada para cerrar el programa.

## Solución de problemas

- **`pygame.error: music_drmp3: corrupt mp3 file`**: el archivo MP3 está dañado
  o mal codificado. Reconviértelo con `ffmpeg` o usa un archivo `.wav` en su
  lugar.
- **`RuntimeError: No se pudo acceder a la cámara`**: prueba cambiar el índice
  en `VideoStream(0)` / `VideoStream(1)`, o cierra otras apps que puedan estar
  usando la cámara (Zoom, Teams, etc.).
- **No detecta ningún rostro en la imagen de referencia**: usa una foto donde
  el rostro se vea de frente, bien iluminado y sin obstrucciones.
- **Rendimiento lento / pocos FPS**: ajusta `ESCALA` (más bajo = más rápido,
  menos preciso) y `PROCESAR_CADA_N_FRAMES` (más alto = más rápido, menos
  responsivo) en `mainV2.py`.
