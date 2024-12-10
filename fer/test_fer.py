import cv2
from fer import FER

detector = FER(mtcnn=True)

emotion_mapping = {
    'happy' : 'happy',
    'sad' : 'sad',
    'angry' : 'anger/stress',
    'fear' : 'anger/stress',
    'neutral' : 'bored',
    'disgust' : 'fatigue', 
} #감정 매핑

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    if not ret:
        break
    
    result = detector.detect_emotions(frame)
    
    for face in result:
        (x, y, w, h) = face["box"]
        emotions = face["emotions"]
        
        mapped_emotions = {}
        for emotion, score in emotions.items():
            if emotion in emotion_mapping:
                mapped_emotion = emotion_mapping[emotion]
                if mapped_emotion in mapped_emotions:
                    mapped_emotions[mapped_emotion] += score
                else:
                    mapped_emotions[mapped_emotion] = score
                    
        if mapped_emotions:
            max_emotion = max(mapped_emotions, key=mapped_emotions.get)
            confidence = mapped_emotions[max_emotion]
            
            
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            
            cv2.putText(frame, f'{max_emotion} : {confidence:.2f}', (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
            
            
    cv2.imshow('Emotion Recognition', frame)
    
    if cv2.waitkey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()



