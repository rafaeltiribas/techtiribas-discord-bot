from random import choice, randint
import requests

URL='https://raw.githubusercontent.com/rafaeltiribas/techtiribas/main/roadmap/README.md'




def get_response(user_input: str) -> str:
    lowered = user_input.lower()
    
    if lowered == '':
        return 'Mensagem vazia'
    elif 'salve' in lowered:
        return 'Salvi'
    elif 'roll dice' in lowered:
        return f'Dado: {randint(1, 20)}'
    elif 'roadmap da live' in lowered:
        response = requests.get(URL)
        return response.text