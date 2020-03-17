from bs4 import BeautifulSoup
import requests

class SkybuilderRankPlayer:
    def __init__(self,dc,server,rank,rank_change,name,fc,score,score_change):
        self.dcgroup = dc
        self.worldname = server
        self.rank = rank
        self.rank_change = rank_change
        self.name = name
        self.fc = fc
        self.score = score
        self.score_change = score_change

def url_build(datacenter, world, job):
    # class, worldname, dcgroup
    default_url = 'na.finalfantasyxiv.com/lodestone/ishgardian_restoration/ranking/'
    ff_job = ('carpenter','blacksmith','armorer','goldsmith','leatherworker','weaver','alchemist','culinarian','miner','botanist','fisher')
    ff_dcgroup = ('Elemental','Gaia','Mana')
    ff_elemental_world = ('Aegis','Atomos','Carbuncle','Garuda','Gungnir','Kujata','Ramuh','Tonberry','Typhon','Unicorn')
    ff_gaia_world = ('Alexander','Bahamut','Durandal','Fenrir','Ifrit','Ridill','Tiamat,Ultima','Valefor','Yojimbo','Zeromus')
    ff_mana_world = ('Anima', 'Asura', 'Belias', 'Chocobo', 'Hades', 'Ixion', 'Mandragora', 'Masamune', 'Pandaemonium', 'Shinryu','Titan')

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
    for r in current_ranklist:
        r_rank = r.find('p',{'class': 'ranking-order'}).string

        if r.find('p',{'class': 'ranking-prev_order__rank_down'}):
            r_rankChange = '-' + r.find('p',{'class': 'ranking-prev_order__rank_down'}).string
        elif r.find('p',{'class': 'ranking-prev_order__rank_up'}):
            r_rankChange = '+' + r.find('p', {'class': 'ranking-prev_order__rank_up'}).string
        else:
            r_rankChange = '0'

        r_name = r.find('div',{'class': 'ranking-name'}).find('p').string

        if not r.find('div', {'class': 'ranking-fc'}):
            r_fc = ' '
        else:
            r_fc = r.find('div', {'class': 'ranking-fc'}).find('p').string

        r_score = r.find('div', {'class': 'ranking-score'}).find('p').string

        if r.find('div', {'class': 'ranking-score'}).find('span'):
            r_scorechange = r.find('div', {'class': 'ranking-score'}).find('span').string
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
    print (r.rank, " ", r.name," ",r.worldname, " ", r.dcgroup, " ")


