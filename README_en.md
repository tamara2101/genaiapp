# Setup Instructions 🚀

This folder contains the necessary environment to run a Chatbot powered by OpenAI within a Streamlit Dashboard application. 

Please note that you will also be provided with secret API keys for an OpenAI Account. Use this app exclusively for educational purposes in our course and do not share these keys with others.


## How to Start the Chatbot

*If you encounter "👋 REPLACE-ME" in the code, simply substitute it with the required content.*


To operate the app, perform the following steps within a Visual Studio Code environment:

1. **Create Your Assistant**:
   - Navigate to the **assistant-gpt** folder.
   - Open the `assistant_create.ipynb` notebook and execute the instructions to generate your Assistant. Ensure to copy the Assistant ID once created.
   - You only need to perform this step once. If you want to change your Assitant, take a look at the last step (how to update your assistant) 

2. **Configure Environment Variables**:
   - Open the `assistant.py` file.
   - Replace `👋 REPLACE-ME` with the Assistant ID you copied earlier:

     ```bash
     OPENAI_ASSISTANT='👋 REPLACE-ME'
     ```

   - Save your changes and keep the remaining content unchanged.

3. **Launch the Application**:
   - For Windows users: Open the Anaconda Command Prompt and navigate to the **assistant-gpt** directory.
   - For Mac users: In Visual Studio Code, open the integrated Terminal via the VS Code menu (Terminal > New Terminal).
   - In the command line, enter:

     ```bash
     streamlit run app.py
     ```

   - This command should open your browser and direct you to a login page.

4. **Log In**:
   - On the login page, enter the following credentials:
     - AI Tutor: `CustomGPT`
     - Password: `123`

You are now ready to interact with your Chatbot!

## How to Update Your Chatbot's Instructions

To update the instructions for your Chatbot:

- Open the `assistant_update.ipynb` notebook in the **assistant-gpt** folder.
- Follow the provided steps to modify and update your Chatbot's configuration.