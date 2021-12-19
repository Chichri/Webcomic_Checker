import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('beautifulsoup4')
install('requests')
#This file installs the libraries used in this application
#There's a better way to do this, but I'm doing it like this for now 
