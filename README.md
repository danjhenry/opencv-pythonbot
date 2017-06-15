# opencv-pythonbot

Automation of a web-browser based game (galaxy online 2) using opencv template matching functions and windows api as a control method.

## Getting Started

* Save the firefox-bot folder for the wheel script and save the collection script for automated collection. 

### Prerequisites

To begin with make sure you have python 3 or higher (this perticular program was built on python 3.5.3).

* PIP installs.
1. pip install pillow
2. pip install numpy
3. pip install pypiwin32
4. pip install python-opencv

* Software installs
1. [firefox 32bit](https://www.mozilla.org/en-US/firefox/new/?scene=2)
2. [flash player](https://get.adobe.com/flashplayer/)

After installing all the require imports and software the script should be able to run on any windows 8 - windows 10 system.

### Installing
* First run the setup.py script to set login info and the window name.

* Then start the main script and do not minimize the browser window as it prevents windows from captureing the image of the game.
  for the best experiance use virutal windows for the scripted windows.

## Deployment

* Deploy up to 8 instances of the script per machine or VM due to adobe flash player limits.
* Deploy collection script on another VM or machine to prevent collusion.

## Built With

* [IDLE](https://en.wikipedia.org/wiki/IDLE)

## Authors

* **Daniel Henry**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* sentdex tutorials inspired me to make this project (https://www.youtube.com/user/sentdex)
