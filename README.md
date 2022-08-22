# Kanban

Kanban is a project-management tool that helps users to visually depict the progress in various stages of the project.

## Description

Kanban consists of lists and cards. Each card denotes a task and list which consists of a group of cards denotes a stage in the project. New lists and cards can be added and existing lists and cards can be deleted. Cards can be moved from one list to another. Cards have deadlines and can be marked as completed upon completion. Summary page gives the overall list wise progress of the tasks. Kanban API can be used to get unrestricted user information.

## Setup and Run

### Windows:
Extract the zip file and open the command prompt from the project folder. Run the following commands in command prompt

```bash
pip install virtualenv
#Install virtual environment

python -m venv .env
#Create a virtual environment .env

.env\scripts\activate
#Activate virtual environment

pip install -r requirements.txt
#Install all necessary modules

python app.py
#Run the app

```
Open this [link](http://127.0.0.1:8080/) in the browser

### Linux:
Extract the zip file and open the terminal from the project folder. Run the following commands in terminal

```bash
pip install virtualenv
#Install virtual environment

python -m venv .env
#Create a virtual environment .env

source .env/bin/activate
#Activate virtual environment

pip install -r requirements.txt
#Install all necessary modules

python app.py
#Run the app

```
Open this [link](http://127.0.0.1:8080/) in the browser

### Note: 
Pre-install python and pip. Incase of inconvenience with above python commands replace 'python' with 'python<version_number>'.

## License
[MIT](https://choosealicense.com/licenses/mit/)
