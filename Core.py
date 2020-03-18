from bs4 import BeautifulSoup
import requests
import csv

class SkybuilderRankPlayer:
    def __init__(self,dc,server,rank,rank_change,name,fc,score,score_change):
        self.dcgroup = dc
        self.world = server
        self.rank = rank
        self.rank_change = rank_change
        self.name = name
        self.fc = fc
        self.score = score
        self.score_change = score_change

    def data(self):
        #m_line = '"' + self.rank + '","' + self.rank_change + '","' +  self.name +self.fc + '","' +  self.score + '","' +  self.score_change + '","' +  self.dcgroup + '","' +   self.worldname + '"'
        #m_line = self.rank + ',' + self.rank_change + ',' + self.name + ',' + self.fc + ',' + self.score + ',' + self.score_change + ',' + self.dcgroup + ',' + self.worldname
        m_line = self.rank + self.rank_change + self.name + self.fc + self.score + self.score_change + self.dcgroup + self.world
        print(m_line)
        return m_line

class SkybuilderCrawler:
    def __init__(self, c_ranklist):
        self.ranklist = c_ranklist
        #self.rankdate = c_rankdate

    def SkybuilderCSVWrite(self):
        # filename
        csv_filename = 'skybuilderrank202003.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            #writer.writerow(["Rank","Rank Change", "Name", "FC", "Score", "Score Change", "Data Center", "World"])

            for character in self.ranklist:
                #new_data = str(character.data())
                #print("N: " + new_data)
                #writer.writerow(new_data.)
                csvrow = [character.rank, character.rank_change, character.name, character.fc, character.score, character.score_change, character.dcgroup, character.world]
                writer.writerow(csvrow)

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







def url_build(datacenter, world, job):
    # ('Elemental', 'Mana', 'Gaia') 3
    # ('Aegis','Atomos','Carbuncle','Garuda','Gungnir','Kujata','Ramuh','Tonberry','Typhon','Unicorn')
    # ('Alexander','Bahamut','Durandal','Fenrir','Ifrit','Ridill','Tiamat,Ultima','Valefor','Yojimbo','Zeromus')
    # ('Anima', 'Asura', 'Belias', 'Chocobo', 'Hades', 'Ixion', 'Mandragora', 'Masamune', 'Pandaemonium', 'Shinryu','Titan')

    # ('Aether', 'Primal', 'Crystal') 3
    # ('Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Jenova', 'Midgardsormr', 'Sargatanas', 'Siren') 8
    # ('Behemoth', 'Excalibur', 'Exodus', 'Famfrit', 'Hyperion', 'Lamia', 'Leviathan', 'Ultros') 8
    # ('Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera') 8

    # ('Chaos', 'Light') 3
    # ('Cerberus', 'Louisoix', 'Moogle', 'Omega', 'Ragnarok', 'Spriggan') 6
    # ('Lich', 'Odin', 'Phoenix', 'Shiva', 'Twintania', 'Zodiark') 6

    # class, worldname, dcgroup
    default_url = 'na.finalfantasyxiv.com/lodestone/ishgardian_restoration/ranking/'
    ff_job = ('carpenter','blacksmith','armorer','goldsmith','leatherworker','weaver','alchemist','culinarian','miner','botanist','fisher')
    ff_dcgroup = ('Elemental','Gaia','Mana')
    ff_elemental_world = ('Aegis','Atomos','Carbuncle','Garuda','Gungnir','Kujata','Ramuh','Tonberry','Typhon','Unicorn')
    ff_gaia_world = ('Alexander','Bahamut','Durandal','Fenrir','Ifrit','Ridill','Tiamat,Ultima','Valefor','Yojimbo','Zeromus')
    ff_mana_world = ('Anima', 'Asura', 'Belias', 'Chocobo', 'Hades', 'Ixion', 'Mandragora', 'Masamune', 'Pandaemonium', 'Shinryu','Titan')

    jp_datacenter = (('Aegis','Atomos','Carbuncle','Garuda','Gungnir','Kujata','Ramuh','Tonberry','Typhon','Unicorn'), ('Alexander','Bahamut','Durandal','Fenrir','Ifrit','Ridill','Tiamat,Ultima','Valefor','Yojimbo','Zeromus'), ('Anima', 'Asura', 'Belias', 'Chocobo', 'Hades', 'Ixion', 'Mandragora', 'Masamune', 'Pandaemonium', 'Shinryu','Titan'))

    r_job = ff_job[job] + '?'
    dcgroup = 'dcgroup='+ ff_dcgroup[datacenter] + '#ranking'

    if datacenter == 0:
        worldname = 'worldname=' + ff_elemental_world[world] + '&'
    elif datacenter == 1:
        worldname = 'worldname=' + ff_gaia_world[world] + '&'
    elif datacenter == 2:
        worldname = 'worldname=' + ff_mana_world[world] + '&'
    else:
        worldname = ''

    default_url = "https://" + default_url + r_job + worldname + dcgroup

    return default_url

def build_ranklist(current_ranklist,dc,world):
    rank_list = []
    for rank_character in current_ranklist:
        r_rank = rank_character.find('p',{'class': 'ranking-order'}).string

        if rank_character.find('p',{'class': 'ranking-prev_order__rank_down'}):
            r_rankChange = '-' + rank_character.find('p',{'class': 'ranking-prev_order__rank_down'}).string
        elif rank_character.find('p',{'class': 'ranking-prev_order__rank_up'}):
            r_rankChange = '+' + rank_character.find('p', {'class': 'ranking-prev_order__rank_up'}).string
        else:
            r_rankChange = '0'

        r_name = rank_character.find('div',{'class': 'ranking-name'}).find('p').string

        if not rank_character.find('div', {'class': 'ranking-fc'}):
            r_fc = ' '
        else:
            r_fc = rank_character.find('div', {'class': 'ranking-fc'}).find('p').string

        r_score = rank_character.find('div', {'class': 'ranking-score'}).find('p').string

        if rank_character.find('div', {'class': 'ranking-score'}).find('span'):
            r_scorechange = rank_character.find('div', {'class': 'ranking-score'}).find('span').string
        else:
            r_scorechange = '0'

        #dc,server,rank,rank_change,name,fc,score,score_change):
        rank_list.append(SkybuilderRankPlayer(dc,world,r_rank,r_rankChange,r_name,r_fc,r_score,r_scorechange))
        t_ranklist = tuple(rank_list)
        print(r_rank,' (', r_rankChange,') ', r_name,' |', r_fc, '| ', r_score, ' (', r_scorechange, ')')
    return t_ranklist



url = url_build(0,0,0)
source_data = requests.get(url)

soup = BeautifulSoup(source_data.text,'lxml')

all_top12 = soup.find('div',{'class': 'ranking-soyf'})
all_top100 = soup.find('div',{'class': 'ranking-wrapper'})

c_ranklist = all_top12.find_all('li', {'class': 'ranking-list__item'})
c_ranklist += all_top100.find_all('li', {'class': 'ranking-list__item'})
c_ranklist = build_ranklist(c_ranklist,"Elemental","Ageis")
print("TESTING")

for r in c_ranklist:
    r.data()

character = SkybuilderCrawler(c_ranklist)
character.SkybuilderCSVWrite()
character.SkybuilderCSVRead()
