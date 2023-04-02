import cv2
import mediapipe as mp
import gtts  
from playsound import playsound  
import pyttsx3

engine = pyttsx3.init()  

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4
text=""
text1=""
# like_img = cv2.imread("images/like.png")
# like_img = cv2.resize(like_img, (200, 180))

# dislike_img = cv2.imread("images/dislike.png")
# dislike_img = cv2.resize(dislike_img, (200, 180))

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    results = hands.process(img)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

            finger_fold_status = []
            finger_fold_status_downwards = []
            finger_fold_for_yes=[]
            fingers_for_no=[]
            fingers_Up_status=[]
            finger_Complete_fold_status_downwards=[]

            for tip in finger_tips:
                x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                # print(id, ":", x, y)
                # cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)

                if lm_list[tip].x > lm_list[tip - 2].x:
                    # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)
                
                if lm_list[tip].y > lm_list[tip - 2].y:
                    # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold_status_downwards.append(True)
                else:
                    finger_fold_status_downwards.append(False)

                if lm_list[tip].y > lm_list[tip - 3].y:
                    # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    finger_Complete_fold_status_downwards.append(True)
                else:
                    finger_Complete_fold_status_downwards.append(False)


                if lm_list[tip].y < lm_list[tip - 1].y < lm_list[tip - 2].y < lm_list[tip - 3].y:
                    # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    fingers_Up_status.append(True)
                else:
                    fingers_Up_status.append(False)


                if lm_list[tip-2].y > lm_list[tip - 3].y:
                    # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold_for_yes.append(True)
                else:
                    finger_fold_for_yes.append(False)
                
                if tip!= 16 and tip!= 20:
                    if lm_list[tip].x < lm_list[tip - 1].x < lm_list[tip - 2].x < lm_list[tip - 3].x :
                    
                        # if lm_list[thumb_tip].y > lm_list[tip]:
                        fingers_for_no.append(True)
                    else:
                        fingers_for_no.append(False)
                
                
                

            print(finger_fold_status)

            if all(fingers_for_no) and finger_fold_status_downwards[2] and finger_fold_status_downwards[3]:
                if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x:
                    
                    cv2.putText(img, "No", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    text="No"

            if finger_fold_status_downwards[2]== True and finger_fold_status_downwards[3]== True :
                    if finger_fold_status_downwards[0]== False and finger_fold_status_downwards[1]== False :
                        if lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x > lm_list[thumb_tip - 2].x :
                            if lm_list[8].x > lm_list[12].x and lm_list[8].y > lm_list[12].y:
                                if lm_list[12].y < lm_list[8].y < lm_list[7].y <lm_list[10].y :
                                    cv2.putText(img, "Right Direction", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                                    text="Right Direction"
                                

            if finger_fold_status_downwards[2]== True and finger_fold_status_downwards[3]== True :
                    if finger_fold_status_downwards[0]== False and finger_fold_status_downwards[1]== False :
                        if lm_list[thumb_tip].x > lm_list[thumb_tip - 1].x > lm_list[thumb_tip - 2].x :
                            if lm_list[8].x < lm_list[12].x and lm_list[7].x < lm_list[11].x and lm_list[6].x < lm_list[10].x and  lm_list[6].y <= lm_list[10].y:
                                cv2.putText(img, "Peace", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                                text="Peace"  
                                print( lm_list[12].x - lm_list[8].x )             

               
            if all(finger_fold_status):
                # like
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y < lm_list[thumb_tip - 3].y and lm_list[8].y > lm_list[thumb_tip - 2].y:
                    text="I Agree"
                    cv2.putText(img, "I Agree", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    # h, w, c = like_img.shape
                    # img[35:h + 35, 30:w + 30] = like_img
                # Dislike
                if lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y > lm_list[thumb_tip - 3].y:
                    cv2.putText(img, "I Disagree", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    text="I Disagree"
                    # h, w, c = dislike_img.shape
                    # img[35:h + 35, 30:w + 30] = dislike_img
            elif all(finger_Complete_fold_status_downwards) and all(finger_fold_for_yes)==False:               # img[35:h + 35, 30:w + 30] = dislike_img
                if lm_list[6].x < lm_list[10].x < lm_list[14].x < lm_list[18].x:
                    if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y < lm_list[thumb_tip - 3].y:
                       if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x :
                           cv2.putText(img, "I am not sure", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                           text="I am not sure"
            
            elif finger_Complete_fold_status_downwards[0]==False and finger_Complete_fold_status_downwards[1]  and finger_Complete_fold_status_downwards[2] and finger_Complete_fold_status_downwards[3]:
                if lm_list[6].x < lm_list[10].x < lm_list[14].x < lm_list[18].x:
                    if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x :
                        if lm_list[thumb_tip-2].x < lm_list[5].x and lm_list[thumb_tip-2].x < lm_list[12].x:
                            cv2.putText(img, "Left Direction", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                            text="Left Direction"
                            
            elif finger_Complete_fold_status_downwards[0]==False and finger_Complete_fold_status_downwards[1]  and finger_Complete_fold_status_downwards[2] and finger_Complete_fold_status_downwards[3]==False:
                if lm_list[6].x < lm_list[10].x < lm_list[14].x < lm_list[18].x:
                    if lm_list[thumb_tip].x < lm_list[thumb_tip - 1].x < lm_list[thumb_tip - 2].x :
                        if lm_list[thumb_tip-2].x < lm_list[5].x and lm_list[thumb_tip-2].x < lm_list[12].x:
                            cv2.putText(img, "I Love You", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                            text="I Love You"


                 # h, w, c = dislike_img.shape



            # if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x > lm_list[8].x:
            #     if finger_fold_status_downwards[2]==False and finger_fold_status_downwards[2]==False:
            #         if lm_list[5].x < lm_list[thumb_tip].x < lm_list[17].x:
            #             cv2.putText(img, "Hello", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            #             text="Hello"              
            # else:
            #     cv2.putText(img, " ", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            if all(fingers_Up_status):
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[thumb_tip].x > lm_list[8].x:
                # if finger_fold_status_downwards[2]==False and finger_fold_status_downwards[2]==False:
                    if lm_list[5].x < lm_list[thumb_tip].x < lm_list[17].x:
                        cv2.putText(img, "Hello", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        text="Hello"              


            if lm_list[thumb_tip].x < lm_list[8].x < lm_list[12].x < lm_list[16].x < lm_list[20].x :
                if all(fingers_Up_status):
                    cv2.putText(img, "Goodbye ", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    text="Goodbye"

            if all(finger_fold_for_yes) and lm_list[thumb_tip].y > lm_list[6].y:
                if  lm_list[5].x < lm_list[thumb_tip].x < lm_list[17].x:
                    cv2.putText(img, "Yes", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    text="Yes"
            
               


            mp_draw.draw_landmarks(img, hand_landmark,
                                   mp_hands.HAND_CONNECTIONS,
                                   mp_draw.DrawingSpec((0, 0, 255), 6, 3),
                                   mp_draw.DrawingSpec((0, 255, 0), 4, 2)
                                   )
    
    # ------------for text to speech----------------------
    # if text1=="":
    #     engine.say(text) 
    #     engine.runAndWait()    
    # if text1 != text:
    #     engine.say(text) 
    #     engine.runAndWait()    
    # text1=text 
    cv2.imshow("Hand Sign Detection", img)
    cv2.waitKey(1)
