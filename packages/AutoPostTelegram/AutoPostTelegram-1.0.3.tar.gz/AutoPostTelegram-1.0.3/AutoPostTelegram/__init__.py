import datetime as dt
import random
import datetime
import requests 

version = "1.0.2"
dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
indian_time = dt_India.strftime('%d-%b-%y %H:%M:%S')

def response(r):
    if r['ok'] is True:
        print('[' + indian_time + ']', 'OK:', r['ok'], ';#' + str(r['result']['message_id']))
    else:
        print('[' + indian_time + ']', 'OK:', r['ok'], '; Error:',r['error_code'],'\n',r['description'],)

class auto():
  """
  Parameters:
      - token : bot token of your bot you can generate it from @botfather
  """
  def __init__(self, token):
      self.token = token
      self.animememe_url = "https://meme-api.herokuapp.com/gimme/{}"
      self.subreddits = ["Animememes", "Wholesomeanimemes", "Narutomemes", "JojoMemes", "Onepiecememes", "Memepiece", "AnimeFunny", "AnimeMirchi" "AnimeMeme", "AttackOnTitanmemes", "DankAnimeMemes", "Anime_Memes", "AnimeAnimemes", "GreatestAnimeMemes", "Goodanimemes", "animemes"]
      self.animegif_url = "https://nekos.best/api/v2/{}"
      self.subpoints = ["baka", "bite", "blush", "bored", "cry", "cuddle", "dance", "facepalm", "feed", "handhold", "happy", "highfive", "hug", "laugh", "pat", "poke", "pout", "punch", "shoot", "shrug", "slap", "sleep", "smile", "smug", "stare", "think", "thumbsup", "tickle", "wave", "wink", "yeet"]
      self.fact_url = "https://some-random-api.ml/animal/{}"
      self.subani = ["dog", "cat", "panda", "fox", "red_panda", "koala", "bird", "raccoon", "kangaroo"]
      self.animechan_url = "https://animechan.vercel.app/api/random"
      self.pkmnmeme_url = "https://meme-api.herokuapp.com/gimme/pokemonmemes"
  def animememe(self, chat):
      try:
          meme = random.choice(self.subreddits)
          animememe_url = requests.get(self.animememe_url.format(meme)).json()['url']
          anime_name = requests.get(self.animememe_url.format(meme)).json()['title']
          anime_post = requests.get(self.animememe_url.format(meme)).json()['postLink']
          r = requests.get(
              "https://api.telegram.org/bot" + self.token + "/sendPhoto?chat_id=" + chat + "&photo=" + animememe_url + f"&caption=[{anime_name}]({anime_post})" + "&parse_mode=MarkdownV2").json()
          response(r)
      except Exception as e:
          return "Something Error Occured Report To telegram.me/Aasf_CyberKing\n\n{}".format(e)

  def animegif(self, chat):
      try:
          animegif_url = requests.get(self.animegif_url.format(random.choice(self.subpoints))).json()["results"][0]["url"]
          r = requests.get(
              "https://api.telegram.org/bot" + self.token + "/sendVideo?chat_id=" + chat + "&video=" + animegif_url).json()
          response(r)
      except Exception as e:
          return "Something Error Occured Report To telegram.me/Aasf_CyberKing\n\n{}".format(e)

  def animequote(self, chat):
      try:
          q = requests.get(self.animechan_url).json()
          q_ani = q['anime']
          q_q = q['quote']
          q_chr = q['character']
          caption = f"""
<b>➢ Anime:</b> `{q_ani}`
<b>➢ Character:</b> `{q_chr}`
<b>➢ Quote:</b> `{q_q}`"""
          r = requests.get(
              "https://api.telegram.org/bot" + self.token + "/sendMessage?chat_id=" + chat + f"&text={caption}" + "&parse_mode=MarkdownV2").json()
          response(r)
      except Exception as e:
          return "Something Error Occured Report To telegram.me/Aasf_CyberKing\n\n{}".format(e)

  def animalfact(self, chat):
      try:
         animal = random.choice(self.subani)
         fact_url = requests.get(self.fact_url.format(animal)).json()["image"]
         fact_fact = requests.get(self.fact_url.format(animal)).json()["fact"]
         r = requests.get(
             "https://api.telegram.org/bot" + self.token + "/sendPhoto?chat_id=" + chat + "&photo=" + fact_url + f"&caption={fact_fact}").json()
         response(r)
      except Exception as e:
          return "Something Error Occured Report To telegram.me/Aasf_CyberKing\n\n{}".format(e)

  def pkmnmeme(self, chat):
      try:
          pkmn = requests.get(self.pkmnmeme_url).json()['url']
          pkmn_name = requests.get(self.pkmnmeme_url).json()['title']
          r = requests.get(
              "https://api.telegram.org/bot" + self.token + "/sendPhoto?chat_id=" + chat + "&photo=" + pkmn + f"&caption='`{pkmn_name}`'" + "&parse_mode=MarkdownV2").json()
          response(r)
      except Exception as e:
          return "Something Error Occured Report To telegram.me/Aasf_CyberKing\n\n{}".format(e)

  def endpoints():
      try:
          return """
• animeme - Post Random Anime Meme [Photo]
• animegifs - Post Random Anime Gifs [Gif]
• animequote - Post Random Anime Quotes [Text]
• animalfact - Post Random Animals Fact [Photo]
• pkmnmeme - Post Random Pokemon Memes [Photo]
"""
      except Exception as e:
          return "Something Error Occured Report To telegram.me/Aasf_CyberKing\n\n{}".format(e)
