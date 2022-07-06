import requests
import os
import re
from time import sleep
from tqdm import tqdm

tr_arr = requests.get("https://api.qurancdn.com/api/v4/resources/translations").json()["translations"]

ch_inf = requests.get("https://api.qurancdn.com/api/v4/chapters?language=en").json()["chapters"]

tr_url = "https://api.qurancdn.com/api/v4/verses/by_chapter/{}?language=en&words=false&translations={}&page=1&per_page=300"
ar_url = "https://api.qurancdn.com/api/v4/quran/verses/uthmani?chapter_number={}"

# first save the arabic one in seperated folder
try:
    os.mkdir("../quran/")
    os.mkdir("../quran/ar/")
except:
    pass

for i in tqdm(range(114), desc="ar"):
  a_r = requests.get(ar_url.format(str(i+1)))
  a_v = a_r.json()["verses"]
  psv = ""
  for j in range(len(a_v)):
    psv += "{}\n".format(a_v[j]["text_uthmani"])
  f = open("../quran/ar/{}.psv".format(str(i+1)), "w", encoding="utf-8")
  f.write(psv)
  f.close()

for k in range(len(tr_arr)):
  try:
      os.mkdir("../quran/{}".format(str(tr_arr[k]["id"])))
  except:
      print("\'{}\' directory already exists".format(str(tr_arr[k]["id"])))
  for i in tqdm(range(114), desc=("%d index" % k)):
    t_r = requests.get(tr_url.format(str(i+1), str(tr_arr[k]["id"])))
    t_v = t_r.json()["verses"]
    psv = ""
    for j in range(len(t_v)):
      psv += "{}\n".format(re.sub(re.compile('\s\s+'), " ", re.sub(re.compile("<[^<]+?>\d*"), " ", t_v[j]["translations"][0]["text"]).replace("\r\n", "").replace("\n", "").replace("\xa0","")))
    f = open("../quran/{}/{}.psv".format(str(tr_arr[k]["id"]), str(i+1)), "w", encoding="utf-8")
    f.write(psv)
    f.close()
  sleep(5)


dTS = ""
for i in tqdm(range(len(ch_inf))):
  dTS += "Surah {} ({} - {})\n".format(ch_inf[i]["name_simple"], ch_inf[i]["name_arabic"], ch_inf[i]["translated_name"]["name"])
f = open("../quran/chapters.txt", "w", encoding="utf-8")
f.write(dTS)
f.close()
