python -m venv waterdistribution
pip install Flask
pip install Flask mysql-connector-python

to activate environment
waterdistribution\Scripts\activate.bat

for restricted access run this
open powershell as admin from start button
run this command: Set-ExecutionPolicy RemoteSigned

INSERT INTO `suppliers`(`ID`, `Name`, `Phone Number`, `Region`, `Date/Time`, `Username`, `Email`, `password`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]','[value-8]')

