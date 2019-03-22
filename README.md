# VecaEase
Python Project
Current version of VacaEase application only support on MacOS. Windows
OS will be supported in the future. The reason is described at the end
of this document.

Installation Procedure (from terminal)
1. Download the zip and Unzip the file
2. Open terminal
3. Type [pip install selenium], so selenium module will be installed
4. Change directory to the folder location
5. Type in: python3 start_application.py
6. Program starts

Installation Procedure (from IDLE3)
1. Download the zip
2. Unzip the file
3. Open terminal
4. Type [pip install selenium], so selenium module will be installed
5. type idle3 (make sure the python version is 3.7)
6. In the idle, click “File” → “Open” → open the “start_application.py”
under the source file
7. In the idle, click on “Run” → Run Module
8. Program starts

Example Output:
<img width="1105" alt="Screen Shot 2019-03-18 at 11 28 41 PM" src="https://user-images.githubusercontent.com/46730869/54578342-d01e0200-49d5-11e9-929e-4f3ce5824ba7.png">

Warning
- Please do not click <submit> button multiple times. Please wait once it turns to
blue.
It usually takes one to two minutes for the application to scrap and analyze travel data.
Duration may depend on the number of days you select.
- Please be aware that current free beta version of VacaEase has a limit of usage of
30 submission per day. Submit more than 30 times may lead to failure of the
program. (due to the limit of Google map api call and Yelp api call)
Issue with Windows OS
Data library we use in the application requires C99 data format, but VS2013
Standard in windows is not C99- conformant. We are looking for ways to
support this in our next release. Sorry for inconvenience.
https://stackoverflow.com/questions/25726331/strftime-f-does-not-workon-
windows
