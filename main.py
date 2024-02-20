"""
python main.py
python -m unittest discover -s assessment -t .
coverage run -m unittest discover -s assessment -t . && coverage report

NRG Python Assessment

Create a python-based solution to respond to the manual inputs 
of an automobile gear shift with automatic transmission, 
as well as dealing with automated gear shifts.  
This should include Unit Testing for the basic scenarios.

Assessee: Gregory Michael Genovese
Date of Assessment: 2-19-2024
"""
from assessment.engine import Engine


def main():
    Engine.run()
        

if __name__ == "__main__":
    main()
