## Rectangular Skylines (RectSky)

### WHAT IT IS:
This is an application that rotates the skyline formed by vertical rectangles into the same skyline formed by the 
minimum number of horizontal rectangles.

### REQUIREMENTS:
RectSky requires:
* Mac-OSx
* Python2.7
* PIP (Python's tools)
* Tkinter (Python's de-facto standard GUI)

#### WHY?
Some packages need to be installed manually as they need user consent and admin priviledges, 
like PIP.
And PIP is dependecy installer that we would use to install the missing dependecies, like Tkinter.

### HOW TO RUN IT (easy way):
1. Clone the sources using ```git clone https://github.com/jmcruz1983/RectSky.git```
2. Run the app generated for Mac-OSx using the terminal and typing ```open ./RectSky.app```
3. The application is generated using ```py2App``` utility. See [instructions](https://www.metachris.com/2015/11/create-standalone-mac-os-x-applications-with-python-and-py2app/). 

### HOW TO RUN IT (more elaborated):
Usually Tkinter comes as default in most of Python distros. In case it is missing you would need to do the following:
1. Clone the sources using ```git clone https://github.com/jmcruz1983/RectSky.git```
2. Install Python2.7 using Mac-OSx installer [python-2.7.14-macosx10.6.pkg](https://www.python.org/ftp/python/2.7.14/python-2.7.14-macosx10.6.pkg).See[instructions](https://www.python.org/downloads/release/python-2714/).
3. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) for PIP installation. See [instructions](https://pip.pypa.io/en/stable/installing/).
4. Install PIP using command ```python get-pip.py```
5. Install Tkinter using ```pip install python-tk```
6. Run the application using ```python RectSky/RectSky.py```

### NOTES:
* The application is a GUI-based consisting of a plot area, a text input and action buttons.
* Please have a look to the video MP4 video that comes with the code where usage is explained visually.
* The application plots vertica skyline in BLUE doted lines and the horizontal skyline in RED doted lines.
* Hovering over the plot the coordinates are displayed helping to verify the skyline.

### HOW TO USE IT:
Having the application up running:
* Initial plot and text input show the example given in the challenge.
* You can find FOUR buttons:
    * CLEAR : It cleans-up the plot and text inserted.
    * RANDOM : It generates a random vertical skyline providing valid JSON input.
    * SOLVE : Having a valid JSON input, it computes a solution and plots it. 
    * COPY : It copies the JSON input to the clipboard.
* You can generate a RANDOM skyline and compute the solution using SOLVE button.
* Another option is to paste-in a valid JSON and compute a solution pression SOLVE button.

### EXAMPLE OF USAGE:
1. Run the application.
2. Example JSON input is shown in the startup.
3. Press SOLVE and find a solution.
4. Press CLEAR for clean-up.
5. Press RANDOM to generate a random vertical skyline.
6. Press SOLVE to find a solution providing a horizontal skyline.
7. Press COPY to copy into clipboard the expected OUTPUT.