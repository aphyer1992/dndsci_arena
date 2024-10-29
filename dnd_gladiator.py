import random
import math
import itertools

random.seed('arena')

races = [
    {'name': 'Human', 'power': 0, 'speed' : 0},
    {'name': 'Dwarf', 'power': 3, 'speed' : -3},
    {'name': 'Elf', 'power': -3, 'speed' : 3},
]

classes = [
    {'name': 'Knight', 'power': 12, 'speed' : 2},
    {'name': 'Warrior', 'power': 10, 'speed' : 4},
    {'name': 'Ranger', 'power': 8, 'speed' : 6},
    {'name': 'Monk', 'power': 6, 'speed' : 8},
    {'name': 'Fencer', 'power': 4, 'speed' : 10},
    {'name': 'Ninja', 'power': 2, 'speed' : 12},
]

legends = [
    {'level': 7, 'class': 'Ninja', 'race': 'Elf', 'boots': 4, 'gauntlets': 3, 'active': True },  # boots will to 2
    {'level': 7, 'class': 'Knight', 'race': 'Elf', 'boots': 3, 'gauntlets': 3, 'active': True },
    {'level': 7, 'class': 'Monk', 'race': 'Dwarf', 'boots': 1, 'gauntlets': 4, 'active': True },  # boots will to 3
    {'level': 7, 'class': 'Warrior', 'race': 'Human', 'boots': 2, 'gauntlets': 2, 'active': True },  # gauntlets will to 3
]

winstruct = {}

for i in range(-6, 7):
    winstruct[i] = [0,0,0] #w,l,d


for r1 in range(6):
    for r2 in range(6):
        for i in range(-6, 7):
            res = r1 + i - r2
            if res > 0:
                winstruct[i][0] += 1
            elif res < 0:
                winstruct[i][1] += 1
            else:
                winstruct[i][2] += 1

winrates = {}
for i in range(-6, 7):
    [win, loss, draw] = winstruct[i]
    winrates[i] = (win + (draw / 2))/ (win + loss + draw)

# char = [level, class, race, boots, gauntlets]
# charstats = [level, class, race, boots, gauntlets, fullname, power, speed]
def add_stats(char):
    if type(char['class']) == type('string'):
        char['class'] = [c for c in classes if c['name'] == char['class']][0]

    if type(char['race']) == type('string'):
        char['race'] = [r for r in races if r['name'] == char['race']][0]
        
    char['power'] = char['level'] + char['race']['power'] + char['class']['power'] + char['gauntlets']
    char['speed'] = char['level'] + char['race']['speed'] + char['class']['speed'] + char['boots']

    fullname = 'Level {} {} {}'.format(char['level'], char['race']['name'], char['class']['name'])
    if char['boots'] > 0 or char['gauntlets'] > 0:
        fullname = fullname + ' with'
    if char['boots'] > 0:
        fullname = fullname + ' +{} Boots of Speed'.format(char['boots'])
    if char['boots'] > 0 and char['gauntlets'] > 0:
        fullname = fullname + ' and'
    if char['gauntlets'] > 0:
        fullname = fullname + ' +{} Gauntlets of Power'.format(char['gauntlets'])

    char['fullname'] = fullname

    return(char)

legends = [ add_stats(l) for l in legends ]

def write_log_row(log_row, mode='a'):
        log_string = ','.join([str(e) for e in log_row])+"\n"
        f = open('gladiator_output_2.csv', mode)
        f.write(log_string)

def setup_logs():
    row = []
    for color in ['Red', 'Black']:
        row.append(color + '_Gladiator')
        row.append(color + '_Level')
        row.append(color + '_Race')
        row.append(color + '_Class')
        row.append(color + '_Boots')
        row.append(color + '_Gauntlets')
    row.append('Winner')
    write_log_row(row, mode='w')

def generate_char(level=math.ceil(random.random() * 6 )):
    char ={
        'level' : level,
        'race': random.choice(races),
        'class': random.choice(classes),
        'boots': math.ceil((random.random() * 3.4) + (level * 0.1))-1,
        'gauntlets': math.ceil((random.random() * 3.4) + (level * 0.1))-1,
        }

    char = add_stats(char)
    return(char)


def get_winrate(c1, c2, verbose=False):
    if verbose:
        print('Speed/Power is {}/{} vs {}/{}\n'.format(c1['speed'], c1['power'], c2['speed'], c2['power']))
    pow_diff = c1['power'] - c2['power']
    if c1['speed'] > c2['speed']:
        pow_diff += 8
    elif c1['speed'] < c2['speed']:
        pow_diff -= 8


    pow_diff = max(pow_diff, -6)
    pow_diff = min(pow_diff, 6)
    c1_winrate = winrates[pow_diff]
    return(c1_winrate)

def fight_chars(c1, c2, verbose=False, log=False):
    c1_winrate = get_winrate(c1, c2)
    
    #if pow_diff >= 0:
    #    c2_winrate = 0.5 * (pow(0.8, pow_diff))
    #    c1_winrate = 1 - c2_winrate   
    #else:
    #    c1_winrate = 0.5 * (pow(0.8, abs(pow_diff)))

    if verbose:
        print('Red Gladiator:\n{}\n(Power {}, Speed {})\nBlue Gladiator:\n{}\n(Power {}, Speed {})\nRed Winrate is {:.2f}%'.format(
            c1['fullname'], c1['power'], c1['speed'],
            c2['fullname'], c2['power'], c2['speed'],
            c1_winrate * 100))

    if random.random() < c1_winrate:
        result = True
    else:
        result = False

    if log:
        row = []
        for char in [c1, c2]:
            row.append(char['fullname'])
            row.append(char['level'])
            row.append(char['race']['name'])
            row.append(char['class']['name'])
            row.append(char['boots'])
            row.append(char['gauntlets'])

        row.append('Red' if result else 'Black')
        write_log_row(row)

    return(result)

def gen_dataset():
    setup_logs()
    tournaments_run = 0
    while tournaments_run < 1226:
        if tournaments_run % 50 == 0:
            print(tournaments_run)
        if tournaments_run == 453:
            legends[2]['boots'] = 3
            legends[2] = add_stats(legends[2])
        if tournaments_run == 882:
            legends[3]['gauntlets'] = 3
            legends[3] = add_stats(legends[2])  # THIS IS A BUG
        if tournaments_run == 1189:
            legends[0]['boots'] = 2
            legends[0] = add_stats(legends[0])
                       
        competitors = []
        legends_included = []
        while(len(competitors) < 64):
            level = min([math.ceil(random.random() * 7), math.ceil(random.random() * 7), math.ceil(random.random() * 7)])
            if level == 7 and (len(legends_included) >= len(legends)):
                level = 6
            if level == 7:
                added = False
                while not added:
                    to_add = math.floor(random.random() * len(legends))
                    if tournaments_run > 1189 and random.random() < 0.2:
                        to_add = 0
                    if to_add not in legends_included:
                        legends_included.append(to_add)
                        competitors.append(legends[to_add])
                        added = True
            else:
                competitors.append(generate_char(level))
        
        while(len(competitors) > 1):
            winners = []
            for i in range(int(len(competitors)/2)):
                c1 = competitors[2*i]
                c2 = competitors[(2*i) + 1]
                result = fight_chars(c1, c2, log=True)
                if result:
                    winners.append(c1)
                else:
                    winners.append(c2)
            competitors = winners
            
        tournaments_run += 1        
        while random.random() < 0.7: # interspersed with duels, more frequent than tournaments
            duel_level = random.choice([3,4,5,6])
            competitors = []
            legends_included = []
            while(len(competitors) < 2):
                level = min([random.choice([duel_level - 1, duel_level, duel_level + 1]), random.choice([duel_level - 1, duel_level, duel_level + 1])])
                if level == 7 and (len(legends_included) >= len(legends)):
                    level = 6
                if level == 7:
                    added = False
                    while not added:
                        to_add = math.floor(random.random() * len(legends))
                        if tournaments_run > 1189 and random.random() < 0.2:
                            to_add = 0
                        if to_add not in legends_included:
                            legends_included.append(to_add)
                            competitors.append(legends[to_add])
                            added = True
                else:
                    competitors.append(generate_char(level))
                
            [c1, c2] = competitors
            fight_chars(c1, c2, log=True)
           
#gen_dataset()
            

def test_scenario():
    npc_chars = [
        { 'level': 7, 'race': 'Elf', 'class': 'Ninja', 'gauntlets': 3, 'boots': 2 },     # POW 9 / SPEED 24
        { 'level': 6, 'race': 'Human', 'class': 'Warrior', 'gauntlets': 1, 'boots': 3 }, # POW 17 / SPEED 13
        { 'level': 6, 'race': 'Human', 'class': 'Knight', 'gauntlets': 2, 'boots': 3 },  # POW 20 / SPEED 11
        { 'level': 6, 'race': 'Dwarf', 'class': 'Monk', 'gauntlets': 2, 'boots': 3 },    # POW 17 / SPEED 14
    ]

     # POW 20 / SPEED 14
    #{'level': 7, 'class': 'Warrior', 'race': 'Human', 'boots': 2, 'gauntlets': 2, 'active': True },  # gauntlets will to 3

    npc_chars = [add_stats(char) for char in npc_chars]

    player_chars = [
        { 'level': 6, 'race': 'Elf', 'class': 'Fencer' },     # POW 6 / SPEED 18
        { 'level': 6, 'race': 'Elf', 'class': 'Knight' },     # POW 15 / SPEED 11  
        { 'level': 5, 'race': 'Dwarf', 'class': 'Warrior' },  # POW 18 / SPEED 6
        { 'level': 5, 'race': 'Human', 'class': 'Ranger' },   # POW 13 / SPEED 11
        { 'level': 5, 'race': 'Dwarf', 'class': 'Ninja' },    # POW 10 / SPEED 14
        { 'level': 5, 'race': 'Human', 'class': 'Monk' },     # POW 11 / SPEED 13
    ]

    char_matchups = list(itertools.permutations(player_chars, 4))
    gauntlet_matchups = list(itertools.permutations([0,1,2,3],4))
    boot_matchups = list(itertools.permutations([4,1,2,3],4))
    best = 0
    tied = 1
    total = 0
    runs = 0

    for c in char_matchups:
        for g in gauntlet_matchups:
            for b in boot_matchups:
                challengers = []
                for i in range(4):
                    challenger = {}
                    challenger['level'] = c[i]['level']
                    challenger['race'] = c[i]['race']
                    challenger['class'] = c[i]['class']
                    challenger['gauntlets'] = g[i]
                    challenger['boots'] = b[i]
                    challengers.append(add_stats(challenger))
                wins = 0
                for i in range(4):
                    wins = wins + get_winrate(challengers[i], npc_chars[i])
                total = total + wins
                runs = runs + 1
                show = False
                if wins == best:
                    tied += 1
                elif wins > best:
                    print('\nNew best of {} with:\n'.format(wins))
                    best = wins
                    tied = 1
                    show = True
                if show:
                    for i in range(4):
                        print('Fight {} with {}'.format(npc_chars[i]['fullname'], challengers[i]['fullname']))

    print('Best score was {} with {} ties'.format(best, tied))
    print('Average score was {} wins'.format(total/runs))

#test_scenario()

def scorer():
    npc_chars = {
        'A': { 'level': 6, 'race': 'Human', 'class': 'Warrior', 'gauntlets': 1, 'boots': 3 }, # POW 17 / SPEED 13
        'B': { 'level': 6, 'race': 'Human', 'class': 'Knight', 'gauntlets': 2, 'boots': 3 },  # POW 20 / SPEED 11
        'C': { 'level': 7, 'race': 'Elf', 'class': 'Ninja', 'gauntlets': 3, 'boots': 2 },     # POW 9 / SPEED 24
        'D': { 'level': 6, 'race': 'Dwarf', 'class': 'Monk', 'gauntlets': 2, 'boots': 3 },    # POW 17 / SPEED 14
    }

     # POW 20 / SPEED 14
    #{'level': 7, 'class': 'Warrior', 'race': 'Human', 'boots': 2, 'gauntlets': 2, 'active': True },  # gauntlets will to 3

    for k in npc_chars.keys():
        npc_chars[k] = add_stats(npc_chars[k])

    player_chars = [
        { 'name' : 'U', 'level': 5, 'race': 'Dwarf', 'class': 'Ninja' },    # POW 10 / SPEED 14  
        { 'name' : 'V', 'level': 5, 'race': 'Dwarf', 'class': 'Warrior' },  # POW 18 / SPEED 6
        { 'name' : 'W', 'level': 5, 'race': 'Human', 'class': 'Ranger' },   # POW 13 / SPEED 11
        { 'name' : 'X', 'level': 5, 'race': 'Human', 'class': 'Monk' },     # POW 11 / SPEED 13
        { 'name' : 'Y', 'level': 5, 'race': 'Elf', 'class': 'Fencer' },     # POW 6 / SPEED 18
        { 'name' : 'Z', 'level': 6, 'race': 'Elf', 'class': 'Knight' },     # POW 15 / SPEED 11
    ]

    players = [
        {
            'player' : 'optimal',
            'A': { 'hero' : 'W', 'boots' : 3, 'gauntlets' : 0},
            'B': { 'hero' : 'Z', 'boots' : 1, 'gauntlets' : 1},
            'C': { 'hero' : 'V', 'boots' : 0, 'gauntlets' : 3},
            'D': { 'hero' : 'X', 'boots' : 2, 'gauntlets' : 2},
        },
        
        {
            'player' : 'simon',
            'A': { 'hero' : 'W', 'boots' : 3, 'gauntlets' : 1},
            'B': { 'hero' : 'Z', 'boots' : 1, 'gauntlets' : 2},
            'C': { 'hero' : 'V', 'boots' : 0, 'gauntlets' : 0},
            'D': { 'hero' : 'X', 'boots' : 2, 'gauntlets' : 3},
        },
        
        {
            'player' : 'abstractapplic',
            'A': { 'hero' : 'Y', 'boots' : 3, 'gauntlets' : 1},
            'B': { 'hero' : 'W', 'boots' : 0, 'gauntlets' : 0},
            'C': { 'hero' : 'Z', 'boots' : 2, 'gauntlets' : 3},
            'D': { 'hero' : 'U', 'boots' : 1, 'gauntlets' : 2},
        },
        
        {
            'player' : 'abstractapplic v2',
            'A': { 'hero' : 'U', 'boots' : 3, 'gauntlets' : 0},
            'B': { 'hero' : 'X', 'boots' : 2, 'gauntlets' : 1},
            'C': { 'hero' : 'V', 'boots' : 0, 'gauntlets' : 3},
            'D': { 'hero' : 'Y', 'boots' : 1, 'gauntlets' : 2},
        },
        {
            'player' : 'Yonge',
            'A': { 'hero' : 'U', 'boots' : 1, 'gauntlets' : 2},
            'B': { 'hero' : 'Z', 'boots' : 3, 'gauntlets' : 1},
            'C': { 'hero' : 'V', 'boots' : 2, 'gauntlets' : 3},
            'D': { 'hero' : 'X', 'boots' : 4, 'gauntlets' : 0},
        },
        
        {
            'player' : 'Lorxus',
            'A': { 'hero' : 'W', 'boots' : 2, 'gauntlets' : 1},
            'B': { 'hero' : 'V', 'boots' : 4, 'gauntlets' : 3},
            'C': { 'hero' : 'X', 'boots' : 1, 'gauntlets' : 2},
            'D': { 'hero' : 'Y', 'boots' : 3, 'gauntlets' : 0},
        },
    ]

    for p in players:
        print('\n\nScoring {} solution:\n'.format(p['player']))
        total= 0
        for champ in ['A', 'B', 'C', 'D']:
            challenger = [c for c in player_chars if c['name' ] == p[champ]['hero']][0]
            challenger['boots'] = p[champ]['boots']
            challenger['gauntlets'] = p[champ]['gauntlets']
            challenger = add_stats(challenger)
            winrate = get_winrate(challenger, npc_chars[champ], verbose=True)
            print('Winrate against {} is {:.2f}%'.format(champ, 100*winrate))
            total = total + winrate
        print('Overall score is {}'.format(total))
    
scorer()

def sample_runs():
    level_map = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    boots_map = [[0,0], [0,0], [0,0], [0,0]]
    gauntlets_map = [[0,0], [0,0], [0,0], [0,0]]
    race_wins = {}
    for r in races:
        race_wins[r['name']] = {}
        for r2 in races:
            race_wins[r['name']][r2['name']] = 0

    class_wins = {}
    for c in classes:
        class_wins[c['name']] = {}
        for c2 in classes:
            class_wins[c['name']][c2['name']] = 0

    runs = 0
    while runs < 1e6:
        runs = runs + 1
        c1 = generate_char()
        c2 = generate_char()
        c1_won = fight_chars(c1, c2)
        level_diff = abs(c1['level'] - c2['level'])
        c1_higher = True if c1['level'] >= c2['level'] else False
        higher_win = True if (c1_higher == c1_won) else False
        if higher_win:
            level_map[level_diff][0] += 1
        else:
            level_map[level_diff][1] += 1

        boots_diff = abs(c1['boots'] - c2['boots'])
        c1_higher = True if c1['boots'] >= c2['boots'] else False
        higher_win = True if (c1_higher == c1_won) else False
        if higher_win:
            boots_map[boots_diff][0] += 1
        else:
            boots_map[boots_diff][1] += 1

        gauntlets_diff = abs(c1['gauntlets'] - c2['gauntlets'])
        c1_higher = True if c1['gauntlets'] >= c2['gauntlets'] else False
        higher_win = True if (c1_higher == c1_won) else False
        if higher_win:
            gauntlets_map[gauntlets_diff][0] += 1
        else:
            gauntlets_map[gauntlets_diff][1] += 1

            
        if c1_won:
            race_wins[c1['race']['name']][c2['race']['name']] += 1
            class_wins[c1['class']['name']][c2['class']['name']] += 1
        else:
            race_wins[c2['race']['name']][c1['race']['name']] += 1
            class_wins[c2['class']['name']][c1['class']['name']] += 1

    for i in range(1, 6):
        print('With a {}-level difference between characters, the higher-level one won {:.2f}% of the time ({}:{})'.format(i, 100 * level_map[i][0] / (level_map[i][0] + level_map[i][1]), level_map[i][0], level_map[i][1]))

    for i in range(1, 4):
        print('With a {}-point difference in boots of speed between characters, the one with better boots won {:.2f}% of the time ({}:{})'.format(i, 100 * boots_map[i][0] / (boots_map[i][0] + boots_map[i][1]), boots_map[i][0], boots_map[i][1]))
        print('With a {}-point difference in gauntlets of power between characters, the one with better gauntlets won {:.2f}% of the time ({}:{})'.format(i, 100 * gauntlets_map[i][0] / (gauntlets_map[i][0] + gauntlets_map[i][1]), gauntlets_map[i][0], gauntlets_map[i][1]))


    for r in races:
        w = 0
        l = 0
        for r2 in races:
            r1 = r['name']
            r2 = r2['name']
            if r1 != r2:
                w_temp = race_wins[r1][r2]
                l_temp = race_wins[r2][r1]
                w += w_temp
                l += l_temp
                print('{} vs {}: {:.2f}% winrate ({}:{})'.format(r1, r2, 100 * w_temp / (w_temp + l_temp), w_temp, l_temp))
        print('Overall winrate for {} is {:.2f}% ({}:{})\n'.format( r['name'], 100 * w / (w+l), w, l ))

    for c in classes:
        w = 0
        l = 0
        for c2 in classes:
            c1 = c['name']
            c2 = c2['name']
            if c1 != c2:
                w_temp = class_wins[c1][c2]
                l_temp = class_wins[c2][c1]
                w += w_temp
                l += l_temp
                print('{} vs {}: {:.2f}% winrate ({}:{})'.format(c1, c2, 100 * w_temp / (w_temp + l_temp), w_temp, l_temp))
        print('Overall winrate for {} is {:.2f}% ({}:{})\n'.format(c['name'], 100 * w / (w+l), w, l ))

