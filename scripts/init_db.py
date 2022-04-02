import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())
cursor = connection.cursor()

#add star signs into 'signs' table
zodiac_signs = [
  {"sign":"aries", "description":"March 31 - April 19"}, 
  {"sign":"taurus", "description":"April 20 - May 20"}, 
  {"sign":"gemini", "description":"May 21 to June 20"}, 
  {"sign":"cancer", "description":"June 21 - July 22"}, 
  {"sign":"leo", "description":"July 23 - August 22"}, 
  {"sign":"virgo", "description":"August 23 - September 22"}, 
  {"sign":"libra", "description":"September 23 - October 22"}, 
  {"sign":"scorpio", "description":"October 23 - November 21"}, 
  {"sign":"sagittarius", "description":"November 22 - December 21"}, 
  {"sign":"capricorn", "description":"December 22 - January 19"}, 
  {"sign":"aquarius", "description":"January 20 - February 18"}, 
  {"sign":"pisces", "description":"February 19 - March 20"}
]
mbti_types = [ #taken from 16personalities.com
  {"type":"ISTJ", "description":"The Logistician"},
  {"type":"ISFJ", "description":"The Defender"},
  {"type":"INFJ", "description":"The Advocate"},
  {"type":"INTJ", "description":"The Architect"},
  {"type":"ISTP", "description":"The Virtuoso"},
  {"type":"ISFp", "description":"The Adventurer"},
  {"type":"INFP", "description":"The Mediator"},
  {"type":"INTP", "description":"The Logician"},
  {"type":"ESTP", "description":"The Entrepreneur"},
  {"type":"ESFP", "description":"The Entertainer"},
  {"type":"ENFP", "description":"The Campaigner"},
  {"type":"ENTP", "description":"The Debater"},
  {"type":"ESTJ", "description":"The Executive"},
  {"type":"ESFJ", "description":"The Consul"},
  {"type":"ENFJ", "description":"The Protagonist"},
  {"type":"ENTJ", "description":"The Commander"},
]
for sign in zodiac_signs:
    sql = "INSERT INTO signs ('star_sign','sign_description') VALUES ('" + sign["sign"] + "','" + sign['description'] + "');"
    cursor.execute(sql)
    connection.commit()
for type in mbti_types:
    sql = "INSERT INTO personalities ('personality','personality_description') VALUES ('" + type["type"] + "','" + type['description'] + "');"
    cursor.execute(sql)
    connection.commit()
cursor.close()    
connection.close()