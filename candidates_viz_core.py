import json
import time
import re
import os

import requests
import numpy as np
import matplotlib.pyplot as plt


api_key = '3fa19afda3a57f68c8f63919bf12b978'
api_token = 'dcd8e68792f9435984a2e7f748a36b44bde35b7773a0f16e4f2e38bac47db4d6'


query = {
   'key': api_key,
   'token': api_token
}
headers = {
   "Accept": "application/json"
}

def get_boards_from_username(username='kevin_bi_bukitvista'):
    url = f"https://api.trello.com/1/members/{username}/boards"

    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query
    )

    return json.loads(response.content)

def get_lists_from_board(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"

    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query
    )

    return json.loads(response.content)

def get_cards_from_list(id_list = '6075440f0e28936699d283d4'):
    url = f'https://api.trello.com/1/lists/{id_list}/cards'
    response = requests.request(
        'GET',
        url,
        params=query
    )
    response_dict = json.loads(response.content)
    return response_dict

def get_checklist_from_card(card_id):
    url = f'https://api.trello.com/1/cards/{card_id}/checklists'
    response = requests.request(
        'GET',
        url,
        params=query
    )
    response_dict = json.loads(response.content)
    return response_dict

def get_card_detail(card_id):
    url = f"https://api.trello.com/1/cards/{card_id}"
    response = requests.request(
        'GET',
        url,
        params=query
    )
    response_dict = json.loads(response.content)
    return response_dict

def data_processing(
  username = 'kevin_bi_bukitvista',
  list_checklist_name_to_compare = ['Career Stage', 'Vital Attributes V2', 'Culture/Leadership Screening'] ,
  board_name = 'TESTING PROJECT',
  list_name = 'TEST KANDIDAT',
):
  #Get all boards from username and filter by the board name
  target_boards = [i for i in [i for i in get_boards_from_username(username) if 'name' in list(i.keys())] if re.match(f'^\s*{board_name}\s*$', i['name'])]

  #Get all lists from the target_boards and filter by the name
  target_lists = [i for i in [i for i in get_lists_from_board(target_boards[0]['id']) if 'name' in list(i.keys())] if re.match(f'^\s*{list_name}\s*$', i['name'])]

  #Get all cards from a list
  cards_id = [i['id'] for i in get_cards_from_list(target_lists[0]['id'])] 

  #Get all checklists from each card
  cards_checklists = [{'card_name': get_card_detail(card_id)['name'], 'checklists': get_checklist_from_card(card_id)} for card_id in cards_id] 

  #Filter the checklist by the checklist name
  selected_cards_checklists = [ {'card_name': card['card_name'], 'checklists': [checklist for checklist in card['checklists'] if checklist['name'].lstrip().rstrip() in list_checklist_name_to_compare] } for card in cards_checklists] 

  #Get all the values from all the checklists with even more filter
  score_types = list(dict.fromkeys([checkItems['name'] for card_checklists in selected_cards_checklists for checklist in card_checklists['checklists'] for checkItems in checklist['checkItems'] if not checkItems['name'].lower().startswith('no')]))

  #convert to numeric point
  all_scores = []
  for name_checklists in selected_cards_checklists:
    name = name_checklists['card_name']
    checklists_check = [({'name': check['name'], 'state': True} if check['state']=='complete' else {'name': check['name'], 'state': False}) for checklist in name_checklists['checklists'] for check in checklist['checkItems']]
    scores = []
    
    for st in score_types:
      found = False
      for cc in checklists_check:
        if cc['name']==st:
          found = True
          if cc['state']:
            scores.append(1)
          else:
            scores.append(0.5)
          break
      if not found:
        scores.append(0.5)
    
    all_scores.append({'name': name, 'scores': scores})

  categories = score_types
  categories = [*categories, categories[0]]
  return categories, all_scores


def visualization(
  categories,
  all_scores,
  candidate_names = ['KANDIDAT 1', 'KANDIDAT 2'],
  show=False
  ):

  label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(categories))

  plt.figure(figsize=(8, 8))
  plt.subplot(polar=True)

  for candidate in candidate_names:
    for name_score in all_scores:
      if candidate==name_score['name']:
        the_scores = name_score['scores']
        the_scores = [*the_scores, the_scores[0]]
        plt.plot(label_loc, the_scores, label=candidate)


  plt.title('Candidates comparison', size=20, y=1.05)
  lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
  plt.legend()

  filename = f'candidates_comparasion-{str(time.ctime()).replace(" ", "_")}.png'
  plt.savefig(filename)

  if show:
    plt.show()
  
  return os.path.join(os.getcwd(), filename)
  

def get_viz(
  username = 'kevin_bi_bukitvista',
  list_checklist_name_to_compare = ['Career Stage', 'Vital Attributes V2', 'Culture/Leadership Screening'] ,
  board_name = 'TESTING PROJECT',
  list_name = 'TEST KANDIDAT',  
  candidate_names = ['KANDIDAT 1', 'KANDIDAT 2'],
  show=False
  ):
  categories, all_scores = data_processing(username, list_checklist_name_to_compare, board_name, list_name)
  return visualization(categories, all_scores, candidate_names, show=show)

if __name__=='__main__':
  print(get_viz(show=False))