# Logical_Clocks_Scale_Models

To run this code all you need to do is type into your command line:
`python3 deploy.py`

This will start the three processes on ports 2056, 3056, and 4056.

These values are hardcoded into our code so if those ports are busy you can
change the ports in line 319-321 in the deploy.py file.

Our logs are kept in the logs folder and are cleared everytime the program runs
so you don't have to worry about manually clearing old logs.
