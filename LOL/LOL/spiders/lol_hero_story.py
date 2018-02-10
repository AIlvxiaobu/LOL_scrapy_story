import scrapy
from LOL.items import LolItem
import re

class LOLSpider(scrapy.Spider):
    def get_start_urls():
        lol_summoner="Aatrox,Ahri,Akali,Alistar,Amumu,Anivia,Annie,Ashe,AurelionSol,Azir,Bard,Blitzcrank,Brand,Braum,Caitlyn,Camille,Cassiopeia,Chogath,Corki,Darius,Diana,Draven,DrMundo,Ekko,Elise,Evelynn,Ezreal,Fiddlesticks,Fiora,Fizz,Galio,Gangplank,Garen,Gnar,Gragas,Graves,Hecarim,Heimerdinger,Illaoi,Irelia,Ivern,Janna,JarvanIV,Jax,Jayce,Jhin,Jinx,Kalista,Karma,Karthus,Kassadin,Katarina,Kayle,Kayn,Kennen,Khazix,Kindred,Kled,KogMaw,Leblanc,LeeSin,Leona,Lissandra,Lucian,Lulu,Lux,Malphite,Malzahar,Maokai,MasterYi,MissFortune,MonkeyKing,Mordekaiser,Morgana,Nami,Nasus,Nautilus,Nidalee,Nocturne,Nunu,Olaf,Orianna,Ornn,Pantheon,Poppy,Quinn,Rakan,Rammus,RekSai,Renekton,Rengar,Riven,Rumble,Ryze,Sejuani,Shaco,Shen,Shyvana,Singed,SionSivir,Skarner,Sona,Soraka,Swain,Syndra,TahmKench,Taliya,Talon,Taric,Teemo,Thresh,Tristana,Trundle,Tryndamere,TwistedFate,Twitch,Udyr,Urgot,Varus,Vayne,Veigar,Velkoz,Vi,Viktor,Vladimir,Volibear,Warwick,Xayah,Xerath,XinZhao,Yasuo,Yorick,Zac,Zed,Ziggs,Zilean,Zoe,Zyra"
        # lol_summoner = "Janna"
        lol_summoner = lol_summoner.split(",")
        start_urls = []
        for summoner in lol_summoner:
            url = "http://yz.lol.qq.com/zh_CN/story/champion/"
            summoner = url + summoner + "/"
            start_urls.append(summoner)
        return start_urls

    name = "lol_hero_story"
    allowed_domains = ["http://yz.lol.qq.com/zh_CN/story/"]
    start_urls = get_start_urls()


    def parse(self, response):
        print("-------------------我进入《英雄联盟宇宙》界面了--------------------")
        lolItem = LolItem()
        lolItem['name'] = response.xpath('//span[@class="alt__5Tm"]/text()').extract_first() #extract_first()返回第一个元素，无结果返回None
        
        if response.xpath('//p[@id="CatchElement"]/p/text()').extract_first() == None:
        # allStory = response.xpath('//p[@id="CatchElement"]/p/text()').extract() #extract()返回结果为selector list列表
            summonerHtml = response.text
            summonerHtml = summonerHtml.replace("\r","").replace("\n","").replace("<p>","").replace("</p>","").strip()
            summoner_re = r'showFirstLetterEffect__2JK">(.+?)</div>'
            bbb = re.compile(summoner_re , re.S)
            aaa = bbb.findall(summonerHtml)
            lolItem['story'] = aaa[0]
        else:
            lolItem['story'] = response.xpath('//p[@id="CatchElement"]/text()').extract()
        yield lolItem
        print("-------------------我离开《英雄联盟宇宙》界面了--------------------")  
        