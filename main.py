import random
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import math 
import time

app = Flask(__name__)
CORS(app)
total_minutes = 240

def generate_player_stats(player, away_com, home_com, x, home_score, away_score,
                          home_team, away_team):
  global total_minutes
  off_rating = player['offRating']
  three_pct = 0
  fgpct = 0
  ft_pct = 0
  def_rating = player['defRating']
  total_off_rating_home = sum(p['offRating'] for p in home_team['players'])
  total_off_rating_away = sum(p['offRating'] for p in away_team['players'])
  total_def_home = sum(p['defRating'] for p in home_team['players'])
  total_def_away = sum(p['defRating'] for p in away_team['players'])

  random_variation = random.randint(-10, 4)
  random_steals  = random.randint(-7, 7)
  random_blocks = random.randint(-5, 5)

  if x == 1:   
    combined = off_rating + def_rating
    normalized = combined / home_com
    
    minutes_played = round(normalized * total_minutes, 2)
    if minutes_played == 0:
      return {
        'name' : player['name'],
        "minutes_played": 0,
        'points': 0,
        'rebounds': 0,
        'assists': 0,
        'steals': 0,
        'blocks': 0,
        'fga': 0,
        'fgm': 0,
        'fgpct': 0,
        '3pt_made': 0,
        '3pt_att': 0,
        '3pt_pct': 0,
        'fta': 0,
        'ftm': 0,
        'ftpct': 0,
        'turnovers': 0

      }
    points = round(home_score * (off_rating/total_off_rating_home))
    rebounds = round((50+random_variation) * (def_rating/total_def_home))
    off_reb = round(random.randint(0, rebounds) + ((off_rating/100)-3))
    if off_reb < 0:
      off_reb = 0
    def_reb = rebounds - off_reb
    assists = round((26+random_variation) * (off_rating/total_off_rating_home))
    steals = round((7+random_steals) * (def_rating/total_def_home))
    blocks = round((5+random_blocks) * (def_rating/total_def_home))
    turnovers = round(13 * (off_rating/total_off_rating_home) * (minutes_played/total_minutes)*10)
  else: 
    combined = off_rating + def_rating
    normalized = combined / away_com
    minutes_played = round(normalized * total_minutes, 2)
    if minutes_played == 0:
      return {
        'name' : player['name'],
        "minutes_played": 0,
        'points': 0,
        'rebounds': 0,
        'assists': 0,
        'steals': 0,
        'blocks': 0,
        'fga': 0,
        'fgm': 0,
        'fgpct': 0,
        '3pt_made': 0,
        '3pt_att': 0,
        '3pt_pct': 0,
        'fta': 0,
        'ftm': 0,
        'ftpct': 0,
        'turnovers': 0

      }
    points = round(away_score * (off_rating/total_off_rating_away))
    rebounds = round((50+random_variation) * (def_rating/total_def_away))
    off_reb = round(random.randint(0, rebounds) + ((off_rating/100)-3))
    if off_reb < 0:
      off_reb = 0
    def_reb = rebounds - off_reb
    assists = round((26+random_variation) * (off_rating/total_off_rating_away))
    steals = round((7+random_steals) * (def_rating/total_def_away) * (minutes_played/240) * 10)
    blocks = round((5+random_blocks) * (def_rating/total_def_away) * (minutes_played/240) * 10)
    turnovers = round((13) * (off_rating/total_off_rating_away) * (minutes_played/total_minutes) * 10)
    print(minutes_played/total_minutes)
  fga = round((off_rating * minutes_played) / 100)
  if fga == 0:
    fgm = 0
    fgpct = 0
    threept_made = 0
    twopt_made = 0
  else:
    threept_made = random.randint(0, int(points/3))
    threept_att = threept_made + random.randint(3, 6)
    twopt_made = math.ceil((points-(threept_made*3))/2)
    fgm = threept_made+twopt_made
    if off_rating < 75:
      fga = fgm + 9 
    if off_rating > 80:
      fga = fgm + 7
    fgpct = (fgm/fga)
  minutes_played = np.clip(minutes_played, 0, 100)
  ftm = points - (twopt_made*2) - (threept_made*3);
  extra_ft =  round(random.uniform(0, off_rating/10))
  ftm += extra_ft
  fta = ftm + random.randint(0, 4)


  if points < 0:
    points = 0

  extra_points = 0
  if off_rating > 89:
    extra_points = random.randint(5, 15)
    points += extra_points
    assists += random.randint(1, 4)
    fta = ftm + random.randint(0, 2)
    turnovers -= 2
    threept_att = threept_made + random.randint(0, 4)

  if def_rating > 89:
    extra_ast = random.randint(1, 5)
    assists += extra_ast
    rebounds += random.randint(1, 5)
  if off_rating < 70:
    fta = ftm + random.randint(1, 4)
    threept_att = threept_made + random.randint(2, 8)


  if fta != 0 and threept_att != 0:
    three_pct = round(threept_made / threept_att, 2) * 100
    ft_pct = round(ftm / fta, 2) * 100
  
  if x == 1:
    home_score += extra_points + extra_ft
  else:
    away_score += extra_points + extra_ft

  

  if three_pct:
    three_pct = three_pct
  else:
    three_pct = 0





  return {
    'id': player['id'],
    'name' : player['name'],
    "minutes_played": minutes_played,
    'points': points,
    'rebounds': rebounds,
    'off_reb': off_reb,
    'def_reb': def_reb,
    'assists': assists,
    'steals': steals,
    'blocks': blocks,
    'fga': fga,
    'fgm': fgm,
    'fgpct': round((fgpct*100), 2),
    '3pt_made': threept_made,
    '3pt_att': threept_att,
    '3pt_pct': three_pct,
    'fta': fta,
    'ftm': ftm,
    'ftpct': ft_pct,
    'turnovers': turnovers

  }
    

def generate_team_score(team, base_score=70, max_score=120, random_factor=30):
  score_range = max_score - base_score;
  rating = sum(player['offRating'] for player in team['players']) + sum(player['defRating'] for player in team['players'])
  random_variation = random.randint(-random_factor, random_factor)
  team_score = base_score + (rating/(len(team['players']) * 100)) * score_range
  team_score = np.clip(team_score, 80, 121)
  team_score += random_variation - 10
  return int(round(min(max_score, max(base_score, team_score))))

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
  data = request.get_json();
  
  home_team = data['home_team']
  away_team = data['away_team']

  combined_home = 0
  for player in home_team['players']:
    combined_home += player['offRating'] + player['defRating']
  combined_away = 0
  for player in away_team['players']:
    combined_away += player['offRating'] + player['defRating']
  
  home_score = generate_team_score(home_team)
  away_score = generate_team_score(away_team)


  if home_score == away_score:
    r = random.randint(0, 1)
    if r == 1: 
      home_score += 4
    else:
      away_score += 4

  home_player_stats = [generate_player_stats(player, combined_away, combined_home, 1, home_score, away_score, home_team, away_team) for player in home_team['players']]
  away_player_stats = [generate_player_stats(player, combined_away, combined_home, 0, home_score, away_score, home_team, away_team) for player in away_team['players']]

    
  
  time.sleep(1)
  return {
      "home_team":{
        "stats": home_player_stats,
       'score': home_score
      },
      "away_team": {
        "stats":away_player_stats,
        'score': away_score
      }
  }



if __name__ == '__main__':
  app.run(debug=True)