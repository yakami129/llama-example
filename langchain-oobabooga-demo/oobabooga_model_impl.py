import json
from langchain.llms.base import LLM
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import requests,os
load_dotenv() 

class Oobabooga(LLM):
    max_token: int = 2048
    temperature: float = 0.7
    top_p: float = 0.95

    # .env add OOBABOOGA_API_URL=xxx
    oobabooga_url: str = os.getenv("OOBABOOGA_API_URL")
    chat_api_url: str = oobabooga_url +'/api/v1/chat'
    
    def __init__(self):
       super().__init__()
       print(self.oobabooga_url)
       print(self.chat_api_url)
            
    @property
    def _llm_type(self) -> str:
        return "oobabooga"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:

        print('prompt:',prompt)

        body = {
            'user_input': prompt,
            'max_new_tokens': self.max_token,
            'auto_max_new_tokens': False,
            'history': {'internal': [], 'visible': []},
            'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'Example',
            'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
            # 'context_instruct': '',  # Optional
            'your_name': 'You',
            'regenerate': False,
            '_continue': False,
            'stop_at_newline': False,
            'chat_generation_attempts': 1,
            'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            'preset': 'None',
            'do_sample': True,
            'temperature': self.temperature,
            'top_p': 0.1,
            'typical_p': 1,
            'epsilon_cutoff': 0,  # In units of 1e-4
            'eta_cutoff': 0,  # In units of 1e-4
            'tfs': 1,
            'top_a': 0,
            'repetition_penalty': 1.18,
            'repetition_penalty_range': 0,
            'top_k': 40,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,

            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': []
        }

        response = requests.post(self.chat_api_url, json=body)
        if response.status_code == 200:
            result = response.json()['results'][0]['history']
            result_message = result['visible'][-1][1]
            return result_message
