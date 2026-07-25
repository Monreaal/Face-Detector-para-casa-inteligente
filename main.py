import cv2
import threading
# pyrefly: ignore [missing-import]
import face_recognition
# pyrefly: ignore [missing-import]
from pygame import mixer

# Inicializamos el mixer al principio del módulo
mixer.init()

class Actions:
    def reproducir_musica(nombre_cancion):
        print(f"Reproduciendo {nombre_cancion}...")
        mixer.music.load(nombre_cancion)
        mixer.music.play()  # Reproduce en segundo plano sin pausar el video


class PersonAction:

    def messi_function(self):
        print("Messi is here")
        print("Welcome home, Pulga!")
        print("Here is your favourite music playing")
        Actions.reproducir_musica("music/De_Musica_Ligera.wav")


acciones = PersonAction()


class VideoStream:
    """Captura frames en un hilo aparte para que la lectura de la
    cámara no bloquee al hilo que hace el reconocimiento facial."""

    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise RuntimeError("No se pudo acceder a la cámara.")
        self.ret, self.frame = self.cap.read()
        self.stopped = False
        self.lock = threading.Lock()
        threading.Thread(target=self._update, daemon=True).start()

    def _update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret, self.frame = ret, frame

    def read(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.ret else None

    def stop(self):
        self.stopped = True
        self.cap.release()

# ---------------------------------------------------------
# 1. Cargar y codificar los rostros "registrados"
#    (aquí agregas todas las personas que quieras reconocer)
# ---------------------------------------------------------
known_face_encodings = []
known_face_names = []

def registrar_rostro(ruta_imagen, nombre):
    img = cv2.imread(ruta_imagen)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)
    if len(encodings) == 0:
        print(f"[AVISO] No se detectó rostro en {ruta_imagen}, se omite.")
        return
    known_face_encodings.append(encodings[0])
    known_face_names.append(nombre)

registrar_rostro("images/messi.jpg", "Messi")
# registrar_rostro("images/elon.jpg", "Elon Musk")  # así agregas más personas

# ---------------------------------------------------------
# 2. Abrir la cámara (captura en hilo aparte)
# ---------------------------------------------------------
video_stream = VideoStream(1)

# Para acelerar el procesamiento, se puede reducir la resolución del frame
ESCALA = 0.2  # procesa a 1/5 del tamaño original

# Solo detectar/reconocer cada N frames; en los demás se reutiliza
# el último resultado. Esto reduce mucho la carga de CPU sin que
# se note visualmente en la mayoría de los casos.
PROCESAR_CADA_N_FRAMES = 3
contador_frames = 0
resultados_previos = []  # [(top, right, bottom, left, name), ...]

# Para no relanzar la acción (ej. reiniciar la música) en cada ciclo
# de detección mientras la persona sigue en cuadro, recordamos a
# quién ya se le ejecutó la acción. Se "olvida" cuando esa persona
# deja de detectarse, para poder disparar de nuevo si reaparece.
personas_ya_saludadas = set()

while True:
    ret, frame = video_stream.read()
    if not ret or frame is None:
        break

    contador_frames += 1

    if contador_frames % PROCESAR_CADA_N_FRAMES == 0:
        # Reducir tamaño para procesar más rápido
        small_frame = cv2.resize(frame, (0, 0), fx=ESCALA, fy=ESCALA)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # model="hog" es el detector rápido en CPU (evitar "cnn" sin GPU)
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        resultados_previos = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Desconocido"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            # Reescalar coordenadas al tamaño original del frame
            top = int(top / ESCALA)
            right = int(right / ESCALA)
            bottom = int(bottom / ESCALA)
            left = int(left / ESCALA)

            resultados_previos.append((top, right, bottom, left, name))

            # -----------------------------------------------------
            # 3. Disparar la acción correspondiente solo la primera
            #    vez que se detecta a la persona en esta aparición.
            # -----------------------------------------------------
            if name != "Desconocido" and name not in personas_ya_saludadas:
                personas_ya_saludadas.add(name)

                if name == "Messi":
                    acciones.messi_function()
                # elif name == "Otra Persona":
                #     acciones.otra_funcion()

        # Las personas que ya no aparecen en este ciclo se "olvidan"
        # para que la acción se pueda disparar de nuevo si regresan.
        nombres_detectados_ahora = {n for (_, _, _, _, n) in resultados_previos}
        personas_ya_saludadas &= nombres_detectados_ahora

    # Dibujar usando el último resultado disponible (se actualice o no en este frame)
    for (top, right, bottom, left, name) in resultados_previos:
        color = (0, 255, 0) if name != "Desconocido" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow("Reconocimiento facial en video", frame)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_stream.stop()
cv2.destroyAllWindows()