## VIT Wifi Autologger

This program only works on Windows.

VIT provides free wifi to students, but one needs to log in to the wifi network to get access to the internet, and it's a pain to do that every time. This program automates the process of logging in and out of the wifi network.

Clone this repository, create a `.env` file as shown in [`.env.sample`](./.env.sample), and then run the program with the following command:

    $ python3 autologger.py

The program creates a System Tray application.

 - The tray icon is a green logo of a router
 - Left-click to log into wifi network
 - Right-click to show options
    - Log into wifi
    - Log out of wifi
    - Exit application


To permanently have this system tray application, [click here](https://stackoverflow.com/questions/4438020/how-to-start-a-python-file-while-windows-starts) to find out how a python program can be run on windows startup.