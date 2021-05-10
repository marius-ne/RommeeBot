from random import choice, sample
from pprint import pprint
import math

PICS = [i for i in range(1,14)]                              #mal 2 da jede Karte zweimal im Stapel
COLS = [i for i in range(1,5)]                               #praktisch für random.sample()
STPL = [(col,pic) for col in COLS for pic in PICS] * 2       #liste von tuples aller karten

DECK = []
G_DECKS = {}
DISCARD = []
OTHER_PLAYERS = 2
DECK_SIZE = 13

def create():
    for i in range(DECK_SIZE):
        try:
            c = tuple([int(i) for i in input(f'{i+1}te Handkarte? ').split(',')])
        except Exception:
            print('ERROR, TRY AGAIN')
            c = tuple([int(i) for i in input(f'{i+1}te Handkarte? ').split(',')])

        DECK.append(c)
        try:
            STPL.remove(c)
        except ValueError:
            print('VALUE ERROR 1')
    for p in range(OTHER_PLAYERS):
        G_DECKS[p] = []
    print('')

    try:
        first = tuple([int(i) for i in input('Erste offene Karte? ').split(',')])
    except Exception:
        print('ERROR, TRY AGAIN')
        first = tuple([int(i) for i in input('Erste offene Karte? ').split(',')])
    STPL.remove(first)
    DISCARD.append(first)
    print('LET THE GAME BEGIN\n')

def rand_deck(size):
    """Nimmt eine Teilmenge des Gesamtdecks.
       Nicht random.choice(), da hier ein Eintrag mehr
       als zweimal genommen werden kann.
       Daher DECK_GES Menge von zwei kompletten Kartensets."""
    return sample(population=STPL,k=size)

# def grp_filter(deck):
#     grps = []
#     for c in deck:
#         members = []
#         col, pic = c
#         o_cols = [color for color in COLS if color != col]
#         for color in o_cols:
#             if (color,pic) in deck:
#                 members.append((color,pic))
#         if len(members) >= 2:
#             grps.extend(members.append(c))
#     print([c for c in deck if c not in grps])

def vict_check(deck):
    covered = []
    for card in deck:
        if card not in covered:
            if (card[0],card[1]+1) in deck and (card[0],card[1]-1) in deck or (card[0],card[1]+1) in deck and (card[0],card[1]+2) in deck or (card[0],card[1]-1) in deck and (card[0],card[1]-2) in deck:
                covered.append(card)
            col, pic = card
            o_cols = [c for c in COLS if c!=col]
            grp = []
            for c in o_cols:
                if (c,pic) in deck:
                    grp.append((c,pic))
            if len(grp) >= 3:
                covered.extend(grp)
    if len(covered) >= len(deck)-1:
        return True
    else:
        return False
    
def eval(deck,card):
    """
    1. Karte mit vollständiger Reihe nach oben oder unten
    2. Karte mit vollständiger Gruppe
    3. Karte mit unvollständiger Gruppe und unvollständiger Reihe
    4. Karte mit unvollständiger Gruppe
    5. Karte mit unvollständiger Reihe
    6. Karte die schon im Deck ist
    """
    val_g = 0               #value für gruppe
    val_s = 0               #value für sequence

    if card in deck:
        col, pic = card
        o_cols = [c for c in COLS if c != col]
        count = 0
        for color in o_cols:
            if (color,pic) in deck:
                count += 1
        if (card[0],card[1]+1) in deck and (card[0],card[1]-1) in deck:
            deck = [dc for dc in deck if dc != (card[0],card[1]+1) and dc != (card[0],card[1]-1)]
        elif (card[0],card[1]+1) in deck and (card[0],card[1]+2) in deck:
            deck = [dc for dc in deck if dc != (card[0],card[1]+1) and dc != (card[0],card[1]+2)]
        elif (card[0],card[1]-1) in deck and (card[0],card[1]-2) in deck:
            deck = [dc for dc in deck if dc != (card[0],card[1]-1) and dc != (card[0],card[1]-2)]
        elif count >= 2:
            deck = [dc for dc in deck if dc[1] != pic]
        else:
            return card, -5

    if (card[0],card[1]+1) in deck and (card[0],card[1]-1) in deck:
        val_s += 5
    elif (card[0],card[1]+1) in deck and (card[0],card[1]+2) in deck:
        val_s += 5
    elif (card[0],card[1]-1) in deck and (card[0],card[1]-2) in deck:
        val_s += 5

    for c in deck:
        col = c[0]
        pic = c[1]
        if col == card[0]:
            if card[1] == pic + 1 or card[1] == pic - 1:
                val_s += 5
        elif pic == card[1]:
            val_g += 7
    val = val_g + val_s
    return card, val

def choose(deck,card):
    #prüft wert der offenen karte
    card_val = eval(deck,card)[1]

    #inner list_comp nimmt jede karte im deck außer prüfkarte damit keine dopplung
    #outer nimmt jede karte im deck und prüft den wert gegen das deck (ohne die karte selber)
    #danach der average im deck mit sum(values) / len(deck)
    stpl_ges = 0
    for c in STPL:
        stpl_ges += eval(deck,c)[1]
    stpl_val = stpl_ges / len(STPL)

    if card_val >= stpl_val:
        return True
    else:
        return False

def h_print(card):
    col = {1:'karo',2:'herz',3:'pik',4:'kreuz'}
    pic = {1:'Ass',2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:'Bube',12:'Dame',13:'König'}
    return f'{col[card[0]]}   {pic[card[1]]}'

def discard(deck,mins):
    """Falls es mehrere min() values gibt entscheidet diese
       Funktion welche Karte weggeworfen werden soll.
       Selbst wenn zwei Karten den gleichen Wert in eval()
       bekommen, könnte eine der Kombinationen schon blockiert sein."""
    
    candidates = []
    for m in mins:
        col = m[0]
        pic = m[1]
        o_cols = [color for color in COLS if color != col] #Other colors
        for color in o_cols:
            if (color,pic+1) in deck and (color,pic-1) in deck:
                candidates.append(m)
            elif (color,pic+1) in deck and (color,pic+2) in deck:
                candidates.append(m)
            elif (color,pic-1) in deck and (color,pic-2) in deck:
                candidates.append(m)
    if candidates:
        print(f'{mins} -> {candidates}')
        return choice(candidates)
    else:
        for m in mins:
            col = m[0]
            pic = m[1]
            o_cols = [color for color in COLS if color != col] #Other colors
            for color in o_cols:
                if (color,pic+1) in deck or (color,pic-1) in deck:
                    candidates.append(m)
                elif (color,pic+1) in deck or (color,pic+2) in deck:
                    candidates.append(m)
                elif (color,pic-1) in deck or (color,pic-2) in deck:
                    candidates.append(m)
        if candidates:
            print(f'{mins} -> N/A -> {set(candidates)}')
            return choice(candidates)
        else:
            print(f'{mins} -> N/A -> N/A')
            return choice(mins)

def my_turn(deck,card):
    global STPL
    if choose(deck,card):
        print('Nimm offene Karte.')
        deck.append(card)
        try:
            DISCARD.remove(card)
        except ValueError:
            print('VALUE ERROR 2',sep=)
    else:
        print('Nimm vom Stapel.')
        try:
            draw = tuple([int(i) for i in input('Welche hast du gezogen? ').split(',')])
        except Exception:
            print('ERROR, TRY AGAIN')
            draw = tuple([int(i) for i in input('Welche hast du gezogen? ').split(',')])
        deck.append(draw)
        try:
            STPL.remove(draw)
        except ValueError:
            print('VALUE ERROR 4')

    vals = {}
    #Gets value für jede karte im deck, im dict ist ein value eine liste an karten
    #discard ist eine aus der liste mit kleinstem wert (key) zufällig ausgewählte
    for c in deck:
        #falls karte mehrmals drin wäre erste list-comp ein problem
        if deck.count(c) <= 1:
            v = eval([dc for dc in deck if dc != c],c)[1]
        else:
            comp = [dc for dc in deck if dc != c]
            comp.append(c)
            v = eval(comp,c)[1]
        if v in vals:
            vals[v].append(c)
        else:
            vals[v] = [c]
    #Manchmal haben mehrere Karten den gleichen val,
    #dafür eigene Evaluationsfunktion (discard())
    minis = vals[min(list(vals.keys()))]
    if len(minis) <= 1:
        disc = minis[0]
    else:
        disc = discard(deck,minis)
        print(f'{minis}')
    print(f'Wirf {h_print(disc)} ab.')

    try:
        deck.remove(disc)
    except ValueError:
        print('VALUE ERROR 5')
    DISCARD.append(disc)
    print(deck,'\n')
    if vict_check(deck):
        print('-----VICTORY-----!')
    else:
        pass

def other_turn(no,deck):
    print(f'SPIELER {no}')
    inp = input('Welche wurde genommen? ')
    if inp:
        try:
            c = tuple([int(i) for i in inp.split(',')])
        except Exception:
            print('ERROR, TRY AGAIN')
            inp = input('Welche wurde genommen? ')
            c = tuple([int(i) for i in inp.split(',')])
    else:
        c = ''

    if not c:
        pass
    else:
        deck.append(c)
        try:
            DISCARD.remove(c)
        except ValueError:
            print('VALUE ERROR 6')
    try:
        d = tuple([int(i) for i in input('Welche wurde abgeworfen? ').split(',')])
    except Exception:
        print('ERROR, TRY AGAIN')
        d = tuple([int(i) for i in input('Welche wurde abgeworfen? ').split(',')])

    try:
        deck.remove(d)
    except ValueError:
        print('VALUE ERROR 7')
    DISCARD.append(d)
    try:
        STPL.remove(d)
    except ValueError:
        print('VALUE ERROR 8')
    print(deck)

if __name__ == '__main__':
    create()
    
    while True:
        print('PLAYER YOU')
        try:
            op = tuple([int(i) for i in input('Welche Karte liegt offen? ').split(',')])
        except Exception:
            print('ERROR, TRY AGAIN')
            op = tuple([int(i) for i in input('Welche Karte liegt offen? ').split(',')])

        my_turn(DECK, op)
        print('\n')
        for player in range(OTHER_PLAYERS):
            other_turn(player,G_DECKS[player])
            print('\n')
