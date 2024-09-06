# Door-Lock-Project

This is the project I worked on for a company called Funktional Automation during my summer internship. This project involves a solenoid lock system. This solenoid turned on or off using a Raspberry Pi 4 microprocessor using various inpur sensors. The solenoid is the hooked up to a door and it acts as a door lock. Following input methods were used to lock and 
unlock the solenoid lock:
1. Voice Command:
   We used DFRobot voice module where it has inbuilt multiple commands and can have couple of customizable commands. The solenoid can be triggered as on or off using the voice. For instance, "Hello Robot" will wake up the module and "Open the Door" command will trigger the solenoid. These commands and wake words can be customized.
2. RFID Tags:
   We also implemented the code where the gpio pin of raspberry pi was programmed to trigger the solenoid only when the RFID reader receives tags with specific id. This was an optional feature for the door to be locked/unlocked in case the client wanted only specific people to have access to the room. These tags can be 3d printed and their tag id can be programmed
   to be received by the reader.
4. Push Botton:
   In case of emergency or some hardware or software malfunction if the voice module dont work, we still should be able to let people get inside the door. So I added a push button with a delay for around 5 seconds (this time allows people to get inside the room) that can be connected off the main circuit or in the same circuit depending on its use.
5. Infrared Sensor:
    People inside the room can exit the room at any time by just waving at the IR sensor attached to the solenoid. If we simply wave our hand near the IR sensor, it will detect the hand and trigger the solenoid lock immediately.

The key feature about this project is to minimize the circuit only one 12v source was used and a 12v relay was used to act as a switch that controls the loads based upon vaious input sensors.

Key Notes:

 Voice Module:
 
- Voice recognition module used is DFRobot Offline Voice Recognition Module.
  link = https://www.dfrobot.com/product-2665.html
  
  Documentation: https://www.electroniclinic.com/voice-recognition-module-with-arduino/#google_vignette
- For voice module, communication protocal used is i2c.
- The above documentation comprises DFRobot i2c and uart .py files to established communication with the module. Inside the DFRobot_DF2310Q-master folder the examples folders contains code the arduino code to use voice module for both i2c and uart. Under python-->raspberrypi-->examples folder have raspberry pi files for i2c and uart. Under python-->raspberry folder
   file called DFRobot_DF2301Q.py is the main library. Make sure to have this library file and the main python code in the same folder.

  RFID:
  
 - For RFID Module make sure to install MFRC522 library and main code should be inside the folder containing SimpleMFRC522.py file.

  Raspberry Pi:
  
  For anyone just starting with raspberry pi,
  - I have used raspberry pi 4 model B 8 gb ram.
  - Upload the OS in a SD card first using PC. You can find OS in raspberry pi website.
  - You can use raspberry pi in two way, first either use a monitor, wifi/ethernet cable, keyboard/mouse to use as a desktop or you can use a software like RealVNC Viewer to use it virtually. You can find tutorials online on how to set it up first time.
  - I used thonny to write python codes in raspberry pi.
  - CAUTION! Please be sure to shut down the raspberry pi if not working to prevent data corruption and back it up everynow and then.
