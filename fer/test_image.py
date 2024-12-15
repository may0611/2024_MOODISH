from fer import FER
import cv2

<<<<<<< HEAD
img_path = r"C:\Users\user\Documents\GitHub\2024_MOODISH\fer\test_image.jpg"
=======
img_path = r"FER/test_image.jpg"
>>>>>>> main
img = cv2.imread(img_path)



def Emotion(img):
    if img is None:
        print("이미지를 불러오지 못했습니다. 경로를 확인하세요.")
    else:
        detector = FER()
        results = detector.detect_emotions(img)

        if not results:
             print("얼굴을 탐지하지 못했거나 감정을 분석하지 못했습니다.")
        else:
            for face in results:
                print(f"탐지된 얼굴 위치: {face['box']}")
                print(f"감정 분석 결과: {face['emotions']}")

    return results
