Echoes After Midnight

Project Description
Echoes After Midnight is a local AI-powered horror story generator developed using Python, Flask, and Ollama. The application allows users to create horror stories by providing a story idea, selecting a setting, and choosing a horror level.
It uses the TinyLlama 1.1B language model to generate stories based on the user's input. The application runs locally, using Ollama to communicate with the AI model.

Features
•	Generate AI-powered horror stories based on user-provided ideas.
•	Select different story settings, including:
        Haunted Mansion
    	Abandoned University
    	Dark Forest
    	Forgotten Cemetery
    	Deserted Hospital
    	Empty Village
    	Old Railway Station
•	Choose a horror level: Mysterious, Medium, Terrifying, or Nightmare.
•	Display generated stories directly on the web application.
•	Provide a responsive, horror-themed user interface.
•	Run AI story generation locally through Ollama.

Technologies Used
Technology	Purpose
Python - Backend programming language
Flask - Web application framework
HTML - Web page structure
CSS	- User interface styling and animations
JavaScript - Frontend interaction
Requests - Communication with the Ollama API
Ollama - Local AI model execution
TinyLlama 1.1B - Horror story generation

System Requirements
•	Python 3
•	Ollama
•	TinyLlama 1.1B model
•	A web browser
•	Visual Studio Code (recommended)

Installation and Setup
1.	Clone the Repository
	git clone https://github.com/ShimraNazar/EchoesAfterMidnight.git
2.	Navigate to the Project Directory
	cd echoes-after-midnight
3.	Create a Virtual Environment
	python -m venv venv
4.	Activate the Virtual Environment
    For Windows:
	       venv\Scripts\activate
5.	Install Required Dependencies
	python -m pip install flask requests
6.	Install the TinyLlama Model
    Install Ollama on your computer and download the TinyLlama model:
    ollama pull tinyllama:1.1b
7.	Run the Application
    Make sure the Ollama service is running. Then start the Flask application:
	python app.py
8.	Access the Application
    Open a web browser and visit:
	    http://127.0.0.1:5000

How to Use
1.	Open the Echoes After Midnight web application.
2.	Enter a horror story idea in the input field.
3.	Select a preferred story setting.
4.	Choose a horror level.
5.	Click the Generate My Ghost Story button.
6.	Wait for the AI model to generate the story.
7.	View the generated story in the output section.

AI Model
This project uses TinyLlama 1.1B, a lightweight language model executed locally through Ollama.
The model receives the user's story idea, selected setting, and horror level as a prompt. It then generates a horror story that is displayed on the web application.
The quality and generation time of the stories may vary depending on the model and the computer's hardware.

Open-Source Innovation
This project demonstrates how open-source AI technologies can be used to develop practical applications without depending on paid AI APIs or cloud-based AI services.
By combining Python, Flask, Ollama, and TinyLlama, the application provides an opportunity to explore local AI integration and experiment with language models in application development.

Project Information
Project Name: Echoes After Midnight
Challenge: Hacktoberfest - Open-Source AI Challenge, Week 4
Project Type: Local AI-Powered Web Application
AI Model: TinyLlama 1.1B
Repository: https://github.com/ShimraNazar/EchoesAfterMidnight.git