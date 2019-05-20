import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import check_patreon
import cookie

today_date = datetime.today().strftime('%Y/%m/%d')
x = True
# url = "https://wanderinginn.com/" + today_date
url = "https://wanderinginn.com/2019/05/18/"
textfile = open("chapter.txt", "w+")

while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    check_404 = soup.find("article", {"id": "post-0"})
    if check_404 is None:
        page_created = datetime.now()
        post = soup.find("h1", {"class": "entry-title"})
        chapter = post.text.split(':')[1].strip()
        print(chapter)
        print("Chapter is posted")
        x = False
        y = True
        link_url = post.find('a')['href']
        print(link_url)
        textfile.write(link_url)
        textfile.close()
        webhook = DiscordWebhook(url=cookie.spidey_bot)
        embed = DiscordEmbed(title='New chapter', description=chapter, color=000000)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.pippng')
        embed.add_embed_field(name='Link', value=link_url)
        webhook.add_embed(embed)
        webhook.execute()
        while y:
            time.sleep(1)
            y = check_patreon.patreon_check(page_created)

    else:
        print("[" + datetime.today().strftime('%X') + "] Chapter is not created")
        time.sleep(10)
