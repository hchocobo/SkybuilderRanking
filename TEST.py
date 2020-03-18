def url_build(region, datacenter, world, job):
# Default skybuilder ranking string
    default_url = "na.finalfantasyxiv.com/lodestone/ishgardian_restoration/ranking/"
    ff_job = ('carpenter','blacksmith','armorer','goldsmith','leatherworker','weaver','alchemist','culinarian','miner','botanist','fisher')
    jp_datacenter = ('Elemental', 'Gaia', 'Mana')
    na_datacenter = ('Aether', 'Primal', 'Crystal')
    eu_datacenter = ('Chaos', 'Light')
    jp_worlds = (('Aegis','Atomos','Carbuncle','Garuda','Gungnir','Kujata','Ramuh','Tonberry','Typhon','Unicorn'), ('Alexander', 'Bahamut', 'Durandal', 'Fenrir', 'Ifrit', 'Ridill', 'Tiamat', 'Ultima', 'Valefor', 'Yojimbo', 'Zeromus'), ('Anima', 'Asura', 'Belias', 'Chocobo', 'Hades', 'Ixion', 'Mandragora', 'Masamune', 'Pandaemonium', 'Shinryu','Titan'))
    na_worlds = (('Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Jenova', 'Midgardsormr', 'Sargatanas', 'Siren'),('Behemoth', 'Excalibur', 'Exodus', 'Famfrit', 'Hyperion', 'Lamia', 'Leviathan', 'Ultros'),('Balmung', 'Brynhildr', 'Coeurl', 'Diabolos', 'Goblin', 'Malboro', 'Mateus', 'Zalera'))
    eu_worlds = (('Cerberus', 'Louisoix', 'Moogle', 'Omega', 'Ragnarok', 'Spriggan'),('Lich', 'Odin', 'Phoenix', 'Shiva', 'Twintania', 'Zodiark'))
# Error checking
    # Check Region default to jp region
    region = region.lower()
    if region != 'jp' or region != 'na' or region != 'eu':
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
    print("MaxWorld: ", max_world)

    # Define datacenter and world
    if region == 'jp':
        # Default DC Elemental
        if datacenter <= 2:
            c_datacenter = jp_datacenter[datacenter]
            max_world = jp_worlds[datacenter]
        else:
            c_datacenter = jp_datacenter[0]
            max_world = jp_worlds[datacenter]

        c_world = jp_worlds[datacenter][world]
    elif region == 'na':
        c_datacenter = na_datacenter[datacenter]
        c_world = na_worlds[datacenter][world]
    elif region == 'eu':
        c_datacenter = eu_datacenter[datacenter]
        c_world = eu_worlds[datacenter][world]
    else:
        c_datacenter = jp_datacenter[datacenter]
        c_world = jp_worlds[datacenter][world]

    print("Datacenter: ", c_datacenter)
    print("World: ", c_world)

    return default_url

