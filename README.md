# Chatbot

## Chatbot for ZKTeco
This chatbot is designed to provide information and support related to ZKTeco products and services. It utilizes OpenAI's API for generating responses and can be integrated with various platforms.

## Installation or Implementation Guide

### Prerequisites
Before installing, ensure you have the following:
- Python (3.7 or later)
- Git

### Installation Steps
Follow these steps to set up the chatbot:

1. Clone the repository:
   ```sh
   git clone https://github.com/Jerrinthomas007/Chatbot.git
   ```
2. Navigate to the project directory:
   ```sh
   cd chatbot
   ```
3. Create a virtual environment:
   - For Windows:
     ```sh
     python -m venv chatbot
     ```
   - For Linux/Mac:
     ```sh
     python3 -m venv chatbot
     ```
4. Activate the virtual environment:
   - For Windows:
     ```sh
     chatbot\Scripts\activate
     ```
   - For Linux/Mac:
     ```sh
     source chatbot/bin/activate
     ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Copy the environment file:
   - For Linux/Mac:
     ```sh
     cp .env.sample .env
     ```
   - For Windows:
     ```sh
     copy .env.sample .env
     ```
7. Add your OpenAI API key in the `.env` file.
8. Run the chatbot application:
   ```sh
   python app.py
   ```
9. Open your browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

