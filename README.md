# password-manager

## Before running the file you have to run command:
    $ pip install pyperclip

## After that run the following commands to get the appropriate output
*-> Example with 'Instagram' and user 'user123456':*

**Generating new password:** 

    $ python passman.py add -title instagram -username user123456 -generatepassword

**Copying password:** 

    $ python passman.py copy -title instagram
    
**Deleting password:**

    $ python passman.py delete -title instagram

**Exporting passwords to CSV:**

    $ python passman.py export -filename export.csv
    
**Changing password:**

    $ python passman.py change -title instagram
 
**Changing Master-Password:**

    $ python passman.py master -update
