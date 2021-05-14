from game import *

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
