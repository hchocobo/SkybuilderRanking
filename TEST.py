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


