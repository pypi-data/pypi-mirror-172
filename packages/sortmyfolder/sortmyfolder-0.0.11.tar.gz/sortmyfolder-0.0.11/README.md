# Documentation for automating file/folder sorting

#### order of executing script

The scipt is excuted by changing directory into auto_group and executing **python determine_location.py**.
This will ask a number of questions regarding the directory you want file executed into. 


This execution will call on the a function within the module **gather_files.py** called  then call on the module **type_of_file.py**.
The code in type_of_file will return a dictionary of the file ending and list of how to to perhaps sort it in a defualt way. 


# installation


This script will...
