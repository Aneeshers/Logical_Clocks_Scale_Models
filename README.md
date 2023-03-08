# Logical_Clocks_Scale_Models

First clone this repository. Then CD into the cloned repository.


To run this code all you need to do is type into your command line:
`python3 deploy.py`

This will start the three processes on ports 2056, 3056, and 4056.

These values are hardcoded into our code so if those ports are busy you can
change the ports in line 319-321 in the deploy.py file.

Our logs are kept in the logs folder and are cleared everytime the program runs
so you don't have to worry about manually clearing old logs. Each port has its own log named {PORT}.txt . There are also additional logs which are used for plotting.


The experimental figures are located in the figure folder -- the figure folder has subfolders labeled by the tick size (this is the m value in our trials -- refer to design choices google doc)

You can view our design decisions, documentation, experiments, results, and unit testing decisions here:
https://docs.google.com/document/d/1vbAVpAJy-5Iyd06PHyGI3Aj-SBigErB9bznpL6dn5Jc/edit#
