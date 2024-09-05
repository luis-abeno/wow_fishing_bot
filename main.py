from PIL import Image, ImageGrab
import numpy as np
import cv2 as cv
import time
from threading import Thread
from fishing.fishing_agent import FishingAgent

class MainAgent:
    def __init__(self) -> None:
        self.agents = []
        self.fishing_thread = None
        self.cur_img = None         # BGR image
        self.cur_img_HSV = None     # HSV image
        
        self.zone = "Feralas"
        self.time = "night"

        # print("Main agent setup completed")                

def update_screen(agent):
    t0 = time.time()
    fps_report_delay = 5
    fps_report_time = time.time()
    
    while True:
        agent.cur_img = ImageGrab.grab()
        agent.cur_img = np.array(agent.cur_img)
        
        agent.cur_img = cv.cvtColor(agent.cur_img, cv.COLOR_RGB2BGR)
        agent.cur_img_HSV = cv.cvtColor(agent.cur_img, cv.COLOR_BGR2HSV)
        
        # cv.imshow("Computer Vision", agent.cur_img)
        key = cv.waitKey(1)
        
        if key == ord('q'):
            break
        
        ex_time = time.time() - t0

        if time.time() - fps_report_time >= fps_report_delay:
            print("FPS: " + str(1/(ex_time)))  
            fps_report_time = time.time()
        
        t0 = time.time()    
        time.sleep(0.005)

def print_menu():
    print("Enter a command:")
    print("\tS\tStart the main agent.")
    print("\tZ\tSet zone.")
    print("\tF\tStart the fishing agent.")
    print("\tQ\tQuit the program.") 
        
if __name__ == "__main__":
    main_agent = MainAgent()
    
    print_menu()    
    while True:
        user_input = input()
        user_input = str.lower(user_input).strip()
        
        if user_input == "s":
            update_screen_thread = Thread(
                target=update_screen, 
                args=(main_agent,),
                name="update_screen_thread",
                daemon=True
            )
            
            update_screen_thread.start()
            
            print("Thread started.")
            
        elif user_input == "z":
            pass
        
        elif user_input == "f":
            fishing_agent = FishingAgent(main_agent=main_agent)
            fishing_agent.run()
        
        elif user_input == "q":
            cv.destroyAllWindows() # TODO(fix): it's causing the program to not respond
            break
        
        else:
            print("Invalid command. Please try again.")
            print_menu()
            
    print("Done.")    