import cv2
import face_recognition
import os
import time
import tkinter as tk
from tkinter import simpledialog
import serial

def load_known_faces(folder_path):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            face_locations = face_recognition.face_locations(image)

            if face_locations:
                face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)[0]
                known_face_encodings.append(face_encodings)
                known_face_names.append(os.path.splitext(filename)[0])
    
    return known_face_encodings, known_face_names

def save_face(frame, face_location, known_face_encodings, known_face_names):
    # Recortar la región de la cara del frame
    top, right, bottom, left = face_location
    face_image = frame[top:bottom, left:right]

    # Pedir al usuario que ingrese un nombre para la nueva imagen
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    name = simpledialog.askstring("Input", "Ingresa el nombre para la imagen:")

    if name:
        # Guardar la imagen en la carpeta 'images'
        filename = f"images/{name}.jpg"
        cv2.imwrite(filename, face_image)
        print(f"Imagen guardada como {filename}")

        # Cargar la nueva imagen y actualizar las codificaciones conocidas
        image_path = filename
        image = cv2.imread(image_path)
        face_locations = face_recognition.face_locations(image)

        if face_locations:
            face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)[0]
            known_face_encodings.append(face_encodings)
            known_face_names.append(name)
            print(f"Rostro de {name} añadido a la base de datos.")

def main():
    # Configurar el puerto serial
    serial_port = serial.Serial('COM9', 9600)  # Ajusta 'COM3' según sea necesario para tu sistema

    # Cargar las codificaciones de rostros conocidos desde una carpeta
    folder_path = "images"
    known_face_encodings, known_face_names = load_known_faces(folder_path)

    # Inicializar la captura de video
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se pudo leer el frame de la cámara.")
                break

            frame = cv2.flip(frame, 1)  # Voltear la imagen horizontalmente

            # Usar el modelo "hog" para una detección más rápida (menos precisa que "cnn")
            face_locations = face_recognition.face_locations(frame, model="hog")
            if face_locations:
                for face_location in face_locations:
                    # Obtener las codificaciones del rostro en el frame
                    face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]

                    # Comparar las codificaciones del rostro en el frame con las imágenes de comparación
                    matches = face_recognition.compare_faces(known_face_encodings, face_frame_encodings)
                    name = "Desconocido"
                    color = (50, 50, 255)

                    if True in matches:
                        match_index = matches.index(True)
                        name = known_face_names[match_index]
                        color = (125, 220, 0)
                        serial_port.write(b'T')  # Enviar 'T' al puerto serial
                    else:
                        serial_port.write(b'F')  # Enviar 'F' al puerto serial

                    # Dibujar el cuadro y el texto en el frame
                    cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
                    cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
                    cv2.putText(frame, name, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)

                    # Guardar la imagen del rostro si se presiona el botón "s"
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        save_face(frame, face_location, known_face_encodings, known_face_names)

            # Mostrar el frame con los cuadros y textos
            cv2.imshow("Frame", frame)

            # Capturar tecla presionada
            key = cv2.waitKey(1) & 0xFF

            # Salir del bucle si se presiona la tecla ESC
            if key == 27:  # 27 es el código ASCII para ESC
                break
            
            # Simular una interrupción en el sistema si se presiona la tecla de espacio
            elif key == ord(' '):
                print("Simulación de interrupción del sistema. Presione cualquier tecla para continuar...")
                cv2.putText(frame, "Interrupcion del sistema", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.imshow("Frame", frame)
                cv2.waitKey(0)  # Pausar hasta que se presione cualquier tecla para continuar

            # Añadir un pequeño retraso para mejorar la capacidad de respuesta
            time.sleep(0.02)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Liberar los recursos de la cámara y cerrar las ventanas
        cap.release()
        cv2.destroyAllWindows()
        # Cerrar el puerto serial
        serial_port.close()

if __name__ == "__main__":
    main()