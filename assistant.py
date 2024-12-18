"""
Liste mit Custom GPTs
"""

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# AI-Assistant Neo
# OPENAI_ASSISTANT = 'asst_1Jmn1tntQOhqHQIvZQCnJhLB' 

# Insert your assistant id below (replace it with your id) 
# Comment out the code in line 10 (deactivate Neo)

OPENAI_ASSISTANT = 'asst_xBotJ8xPzKYFC9dUs6eibcwA'

gpts = {
    "CustomGPT": OPENAI_ASSISTANT,
}