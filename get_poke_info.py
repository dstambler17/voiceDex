import requests
import json
import time
import re
import os
from langdetect import detect_langs

class Pokedex:
    @staticmethod
    def get_poke_sprite(name):
        file_name_regex = re.compile(name + '(?:.{0,10})\.png', re.IGNORECASE)
        for root, dirs, files in os.walk('./poke_sprites'):
            matches = [x for x in files if file_name_regex.match(x)]
            sprite_file_name = matches[len(matches) - 1] if name !='Mew' else matches[0]
            print(sprite_file_name)
            return sprite_file_name


    @staticmethod
    def get_poke_info(dex_num):
        '''
        Funtion to call api and get dex info
        '''
        url = 'https://pokeapi.co/api/v2/pokemon-species/' + str(dex_num)
        r = requests.get(url)
        if r.status_code == 200 and dex_num.isdigit():
            data = json.loads(r.text)
            #Get the needed variables
            #Change name to uppercase
            poke_name = data['name']
            name_list = list(poke_name)
            name_list[0] = name_list[0].upper()
            poke_name = ''.join(name_list)

            flavor_text_index = 1 if int(dex_num) < 722 else 2 #If gen 7 and up, this changes
            poke_description = data['flavor_text_entries'][flavor_text_index]['flavor_text']
            print('Name: {}, Description: {}'.format(poke_name, poke_description))
            print(detect_langs(poke_description))

            #if description is japanese try with a different index
            if str(detect_langs(poke_description)[0])[0:2] == 'ja':
                poke_description = data['flavor_text_entries'][2]['flavor_text']
                print('Japanese detected, trying english')
            
            return poke_name, poke_description
            
        else:
            print('Error calling api')
            return None, None