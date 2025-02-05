# Talking-keyboard-controlled-by-eye-movement-2019-2020
This project uses Python with opencv and DLIP to detect eye movements, which helps control a virtual keyboard for composing words or sentences. Once the word or sentence is formed, the user can click on the "Speak" button to have it spoken out loud. 

## Acknowledgements
- This is the first release of the project, and currently, it only supports the English language.
- The design of this keyboard is different from a traditional one. This is because the camera detects eye movements more clearly when moving left and right, rather than up and down. This design takes into account the camera's quality, ensuring that it works well even with medium or lower-quality cameras  
- This code is inspired by the tutorials and resources available on PySource: https://pysource.com/

## Requirements
1. pyhton > 3.0
2. python libraries
- cv2
- Numpy
- dlib
- math
- pyttsx3
3. shape_predictor_68_face_landmarks.dat file from (https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat)
4. a webcam to start capturing

## How to use it
1. The keyboard consists of 10 large boxes, and each large box contains 4 smaller boxes, each having a button for a specific action or letter.
2. Start moving your eyes left and right. The highlighted large box on the keyboard will change based on your eye movement.
3. Select the large box you want, then blink your eyes for about 2 seconds. This will confirm your selection and allow you to enter the selected box.
4. Once inside a large box, you can move between the 4 smaller boxes. Choose a small box by blinking your eyes for 2 seconds. After selection, the letter or action from the small box will appear on the screen.
5. If you accidentally enter a wrong large box and want to exit, look left or right for 2 seconds to return 
6. Once you've formed a statement, you can choose the "Speak" button, and the system will pronounce it for you.
