import cv2
import face_recognition
import time

def main():
    # Leer la imagen de comparación y calcular sus codificaciones de rostro
    image = cv2.imread("images/josue.jpg")
    face_loc = face_recognition.face_locations(image)[0]
    face_image_encodings = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0]

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
                    
                    # Comparar las codificaciones del rostro en el frame con la imagen de comparación
                    result = face_recognition.compare_faces([face_image_encodings], face_frame_encodings)
                    
                    # Determinar el texto y color del cuadro en función del resultado de la comparación
                    if result[0]:
                        text = "Josue"
                        color = (125, 220, 0)
                    else:
                        text = "Desconocido"
                        color = (50, 50, 255)

                    # Dibujar el cuadro y el texto en el frame
                    cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
                    cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
                    cv2.putText(frame, text, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)

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

if __name__ == "__main__":
    main()