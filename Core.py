from bs4 import BeautifulSoup
import requests
import csv
import datetime

ff_job = (
'carpenter', 'blacksmith', 'armorer', 'goldsmith', 'leatherworker', 'weaver', 'alchemist', 'culinarian', 'miner',
'botanist', 'fisher')

jp_datacenter = ('Elemental', 'Gaia', 'Mana')
na_datacenter = ('Aether', 'Primal', 'Crystal')
eu_datacenter = ('Chaos', 'Light')

jp_worlds = (('Aegis', 'Atomos', 'Carbuncle', 'Garuda', 'Gungnir', 'Kujata', 'Ramuh', 'Tonberry', 'Typhon', 'Unicorn'),
             ('Alexander', 'Bahamut', 'Durandal', 'Fenrir', 'Ifrit', 'Ridill', 'Tiamat', 'Ultima', 'Valefor', 'Yojimbo',
              'Zeromus'), (
             'Anima', 'Asura', 'Belias', 'Chocobo', 'Hades', 'Ixion', 'Mandragora', 'Masamune', 'Pandaemonium',
             'Shinryu', 'Titan'))
na_worlds = (('Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Jenova', 'Midgardsormr', 'Sargatanas', 'Siren'),
             ('Behemoth', 'Excalibur', 'Exodus', 'Famfrit', 'Hyperion', 'Lamia', 'Leviathan', 'Ultros'),
             ('Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera'))
eu_worlds = (('Cerberus', 'Louisoix', 'Moogle', 'Omega', 'Ragnarok', 'Spriggan'),
             ('Lich', 'Odin', 'Phoenix', 'Shiva', 'Twintania', 'Zodiark'))

class SkybuilderRankPlayer:
    def __init__(self, dc, server, rank, rank_change, name, fc, score, score_change, i_job):
        self.dcgroup = dc
        self.world = server
        self.rank = rank
        self.rank_change = rank_change
        self.name = name
        self.fc = fc
        self.score = score
        self.score_change = score_change
        self.job = i_job

    def data(self):
        #m_line = '"' + self.rank + '","' + self.rank_change + '","' +  self.name +self.fc + '","' +  self.score + '","' +  self.score_change + '","' +  self.dcgroup + '","' +   self.worldname + '"'
        #m_line = self.rank + ',' + self.rank_change + ',' + self.name + ',' + self.fc + ',' + self.score + ',' + self.score_change + ',' + self.dcgroup + ',' + self.worldname
        m_line = self.rank + self.rank_change + self.name + self.fc + self.score + self.score_change + self.dcgroup + self.world
        print(m_line)
        return m_line

class SkybuilderCrawler:
    def __init__(self, c_ranklist):
        # Ranklist [world][JOB][CHARACTER]
        self.ranklist = []
        self.ranklist = c_ranklist
        self.maxWorld = len(self.ranklist)
        self.maxJob = 11
        self.maxRank = 100
        #self.rankdate = c_rankdate

    def SkybuilderCSVWrite(self):
        # filename
        current_time = datetime.datetime.now()
        time_stamp = current_time.strftime('%Y%m%d_h%Hm%M')

        csv_filename = 'sr_elemental' + time_stamp + '.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            #writer.writerow(["Rank","Rank Change", "Name", "FC", "Score", "Score Change", "Data Center", "World"])
            w_world = 0
            w_job = 0
            while w_world < self.maxWorld:
                # Loop the world rank info

                while w_job < self.maxJob:
                    # print(datacenter_ranklist[0][0][0].name) print first world(AGEIS) first job(CRP) RANK 1

                    for character in self.ranklist[w_world][w_job]:
                        csvrow = [character.rank, character.rank_change, character.name, character.fc, character.score,
                                  character.score_change, character.dcgroup, character.world, character.job]
                        writer.writerow(csvrow)
                    # rest to first job
                    w_job = w_job + 1
                # loop to next world
                w_job = 0
                w_world = w_world + 1



    def SkybuilderCSVRead(self):
        # filename
        csv_filename = 'skybuilderrank202003.csv'
        with open(csv_filename, 'r', newline='') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            print("Reading file Dictionary")
            # 6 , 7     , 0   , 1          , 2   , 3 , 4    , 5
            # dc, server, rank, rank_change, name, fc, score, score_change
            r_ranklist = []
            for row in rows:
                #r_ranklist.append(SkybuilderRankPlayer(row[6],row[7],row[0],row[1],row[2],row[3],row[4],row[5]))
                print(row[0]," ", row[1], " ", row[2], " ", row[3], " ", row[4], " ", row[5], " ", row[6], " ", row[7])

class ffxiv_world:
    def __init__(self, dc, world, region):
        self.dc = dc
        self.world = world
        self.region = region

def url_build(region, datacenter, world, job):
# Default skybuilder ranking string
    default_url = "finalfantasyxiv.com/lodestone/ishgardian_restoration/ranking/"

    # Check Region default to jp region
    region = region.lower()
    if region != 'jp' and region != 'na' and region != 'eu':
        region = 'jp'

    # Setup Datacenter
    if region != 'eu':
        max_datacenter = 2
    else:
        max_datacenter = 1

    # Datacenter is out of range set it to 0
    if datacenter > max_datacenter:
        datacenter = 0

    # Setup Current datacenter
    if region == 'na':
        cur_dc = na_datacenter[datacenter]
    elif region == 'eu':
        cur_dc = eu_datacenter[datacenter]
    else:
        cur_dc = jp_datacenter[datacenter]

    # Setup Max World Limit
    if region == 'na':
        max_world = len(na_worlds[datacenter])
    elif region == 'eu':
        max_world = len(eu_worlds[datacenter])
    else:
        max_world = len(jp_worlds[datacenter])

    # default to first world when max out
    if world >= max_world:
        world = 0
    # setup current world
    if region == 'na':
        cur_world = na_worlds[datacenter][world]
    elif region == 'eu':
        cur_world = eu_worlds[datacenter][world]
    else:
        cur_world = jp_worlds[datacenter][world]

    # Check job range default to 0
    if job >= len(ff_job):
        job = 0
    #setup Job
    cur_job = ff_job[job]

    # build URL https://na.finalfantasyxiv.com/lodestone/ishgardian_restoration/ranking/ carpenter?worldname=Aegis&dcgroup=Elemental#ranking
    region = 'na'
    default_url = "https://" + region + "." + default_url + cur_job + "?worldname=" + cur_world + "&dcgroup=" + cur_dc + "#ranking"

    return default_url


def build_ranklist(current_ranklist, r_dc, r_world, skr_job):
    rank_list = []
    for rank_character in current_ranklist:
        # get rank
        r_rank = rank_character.find('p',{'class': 'ranking-order'}).string

        # get rank change
        if rank_character.find('p',{'class': 'ranking-prev_order__rank_down'}):
            r_rankChange = '-' + rank_character.find('p',{'class': 'ranking-prev_order__rank_down'}).string
        elif rank_character.find('p',{'class': 'ranking-prev_order__rank_up'}):
            r_rankChange = '+' + rank_character.find('p', {'class': 'ranking-prev_order__rank_up'}).string
        else:
            r_rankChange = '0'

        # get character name
        r_name = rank_character.find('div',{'class': 'ranking-name'}).find('p').string
        # get fc name
        if not rank_character.find('div', {'class': 'ranking-fc'}):
            r_fc = ' '
        else:
            r_fc = rank_character.find('div', {'class': 'ranking-fc'}).find('p').string
        # get score
        r_score = rank_character.find('div', {'class': 'ranking-score'}).find('p').string
        # get score change
        if rank_character.find('div', {'class': 'ranking-score'}).find('span'):
            r_scorechange = rank_character.find('div', {'class': 'ranking-score'}).find('span').string
        else:
            r_scorechange = '0'
        # send data into skybuilder obj _(self, dc, server, rank, rank_change, name, fc, score, score_change, i_job):
        rank_list.append(
            SkybuilderRankPlayer(r_dc, r_world, r_rank, r_rankChange, r_name, r_fc, r_score, r_scorechange, skr_job))
    return rank_list

# URL LOOP for datacenter
r_region = 'jp'
r_dc = 0
r_world = 0
r_job = 0
datacenter_ranklist = []

while (r_world < 10):
    print("R_WORLD: ", r_world)
    world_ranklist = []

    while (r_job < 11):
       url = url_build(r_region, r_dc, r_world, r_job)

       # Grab ranking page
       source_data = requests.get(url)
       soup = BeautifulSoup(source_data.text, 'lxml')
       # Grab top 12
       all_top12 = soup.find('div', {'class': 'ranking-soyf'})
       # Grab remaining 100
       all_top100 = soup.find('div', {'class': 'ranking-wrapper'})
       # build rank list
       c_ranklist = all_top12.find_all('li', {'class': 'ranking-list__item'})
       c_ranklist += all_top100.find_all('li', {'class': 'ranking-list__item'})
       c_ranklist = build_ranklist(c_ranklist, jp_datacenter[r_dc], jp_worlds[r_dc][r_world], ff_job[r_job])
       world_ranklist.append(c_ranklist)
       r_job = r_job + 1
    r_job = 0

    datacenter_ranklist.append(world_ranklist)
    # [WORLD][JOB][character]
    # print(datacenter_ranklist[0][0][0].name) print first world(AGEIS) first job(CRP) RANK 1

    r_world = r_world + 1

Skybuilder_RankList = SkybuilderCrawler(datacenter_ranklist)
Skybuilder_RankList.SkybuilderCSVWrite()
print("Task complete")
