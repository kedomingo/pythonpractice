# -*- coding: UTF-8 -*-
import sys
from itertools import combinations

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def cardsort(x):
    return getCardValue(x) + getCardSuitValue(x)

def cardsortAceLow(x):
    return getCardValue(x, acehigh=False) + getCardSuitValue(x)

def scoresort(hand):
    return getCardsScore(hand)

def getCardsScore(cards):
    score = 0
    # special case for full house. use lowest pair possible
    if isFullhouse(cards):
        threeKinds = findThreeOfAKind(cards)
        threeKinds = threeKinds[0]
        pair = diff(cards, threeKinds)
        return 7000 * (getCardsScore(threeKinds) + (1 / getCardsScore(pair)))

    for card in cards:
        score += getCardValue(card) + getCardSuitValue(card)
    multiplier = 1
    if isStraightFlush(cards):
        multiplier = 900000
    elif hasFourOfAKind(cards):
        multiplier = 80000
    elif isFlush(cards):
        multiplier = 6000
    elif isStraight(cards):
        multiplier = 500
    elif hasThreeOfAKind(cards):
        multiplier = 40
    elif hasTwoPairs(cards):
        multiplier = 30
    elif hasPair(cards):
        multiplier = 2
    return multiplier * score

def getCardValue(card, acehigh=True):
    val = card[:-1]
    val = val.lower()
    val = 11 if val == 'j' else val
    val = 12 if val == 'q' else val
    val = 13 if val == 'k' else val
    val = 14 if val == 'a' else val
    val = 1 if val == 14 and not acehigh else val
    return int(val)

def getCardSuitValue(card):
    suit = card[-1]
    suit = 0.1 if suit == 'c' else suit
    suit = 0.2 if suit == 's' else suit
    suit = 0.3 if suit == 'h' else suit
    suit = 0.4 if suit == 'd' else suit
    return suit

def isFullhouse(cards):
    threeKinds = findThreeOfAKind(cards)
    if len(threeKinds) != 1:
        return False
    threeKinds = threeKinds[0]
    pair = diff(cards, threeKinds)
    return isPair(pair)

def isPair(cards):
    return len(cards) == 2 and getCardValue(cards[0]) == getCardValue(cards[1])

def isStraightFlush(cards):
    return isStraight(cards) and isFlush(cards)

def isFlush(cards):
    suit = None
    for card in cards:
        if suit == None:
            suit = getCardSuitValue(card)
            continue;
        if getCardSuitValue(card) != suit:
            return False;
    return True;

def isStraight(cards, acehigh=True):
    if acehigh:
        cards = sorted(cards, key=cardsort)
    else:
        cards = sorted(cards, key=cardsortAceLow)

    last = None
    for card in cards:
        if last == None:
            last = getCardValue(card, acehigh=False)
            continue;
        if getCardValue(card) - 1 != last and getCardValue(card, acehigh=False) - 1 != last:
            # base case: 2nd attempt: acehigh = false
            if not acehigh:
                return False;
            return isStraight(cards, acehigh=False)
        # ace high can only happen when it is last. no need to account for it here
        last = getCardValue(card)
    return True;

def isNOfAKind(cards):
    value = None
    for card in cards:
        if value == None:
            value = getCardValue(card)
            continue;
        if getCardValue(card) != value:
            return False;
    return True;

def hasFourOfAKind(cards):
    return len(findFourOfAKind(cards)) == 1

def hasThreeOfAKind(cards):
    return len(findThreeOfAKind(cards)) == 1

def hasTwoPairs(cards):
    return len(findPairs(cards)) == 2

def hasPair(cards):
    return len(findPairs(cards)) == 1

def findFlush(hand, sort = False):
    if sort:
        hand = sorted(hand, key=cardsort)
    combis = combinations(hand, 5)
    flushes = [];
    for cards in combis:
        if isFlush(cards):
            flushes.append(list(cards))
    return flushes

def findStraight(hand, sort = False):
    if sort:
        hand = sorted(hand, key=cardsort)
    combis = combinations(hand, 5)
    straights = []
    for cards in combis:
        if isStraight(cards):
            straights.append(list(cards))
    return straights

def findPairs(hand, sort = False):
    if sort:
        hand = sorted(hand, key=cardsort)
    combis = combinations(hand, 2)
    pairs = [];
    for cards in combis:
        if isNOfAKind(cards):
            pairs.append(list(cards))
    return pairs

def findThreeOfAKind(hand, sort = False):
    if sort:
        hand = sorted(hand, key=cardsort)
    combis = combinations(hand, 3)
    threeKinds = [];
    for cards in combis:
        if isNOfAKind(cards):
            threeKinds.append(list(cards))
    return threeKinds

def findFourOfAKind(hand, sort = False):
    if sort:
        hand = sorted(hand, key=cardsort)
    combis = combinations(hand, 4)
    fourkinds = [];
    for cards in combis:
        if isNOfAKind(cards):
            fourkinds.append(list(cards))
    return fourkinds

def getStraightFlushes(hand):
    flushes = findFlush(hand)
    if flushes == []:
        return []
    straightFlushes = []
    for flush in flushes:
        if isStraight(flush):
            straightFlushes.append(flush)
    return straightFlushes

def getFullHouses(hand):
    threeOfAKinds = findThreeOfAKind(hand)
    if threeOfAKinds == []:
        return []

    threeOfAKinds = sorted(threeOfAKinds, key=scoresort)
    fullHouses = []
    for setThrees in threeOfAKinds:
        whatsLeft = diff(hand, setThrees)
        pairs = findPairs(whatsLeft)
        pairs = sorted(pairs, key=scoresort)
        for pair in pairs:
            fullHouses.append(setThrees + pair)
    return fullHouses

def findBest(hand, cardsneeded):
    if not len(hand):
        return None;

    hand = sorted(hand, key=cardsort)
    if cardsneeded == 5:
        straightFlushes = getStraightFlushes(hand)
        if straightFlushes != []:
            straightFlushes = sorted(straightFlushes, key=scoresort)
            return straightFlushes[-1] #return highest

        fourOfAKinds = findFourOfAKind(hand)
        if fourOfAKinds != []:
            fourOfAKinds = sorted(fourOfAKinds, key=scoresort)
            return fourOfAKinds[-1] #return highest

        fullHouses = getFullHouses(hand)
        if fullHouses != []:
            fullHouses = sorted(fullHouses, key=scoresort)
            return fullHouses[-1] #return highest

        flushes = findFlush(hand)
        if flushes != []:
            flushes = sorted(flushes, key=scoresort)
            return flushes[-1] #return highest

        straights = findStraight(hand)
        if straights != []:
            straights = sorted(straights, key=scoresort)
            return straights[-1] #return highest

        twopairs = findPairs(hand)
        if len(twopairs) >= 2:
            twopairs = sorted(twopairs, key=scoresort)
            return twopairs[-1] + twopairs[-2] #return highest 2

    if cardsneeded == 4:
        fourOfAKinds = findFourOfAKind(hand)
        if fourOfAKinds != []:
            fourOfAKinds = sorted(fourOfAKinds, key=scoresort)
            return fourOfAKinds[-1] #return highest

        # two pairs
        pairs = findPairs(hand)
        if len(pairs) >= 2:
            pairs = sorted(pairs, key=scoresort)
            return pairs[-1] + pairs[-2] #return highest 2 (last 2 elements)


    if cardsneeded >= 3:
        threeOfAKinds = findThreeOfAKind(hand)
        if threeOfAKinds != []:
            threeOfAKinds = sorted(threeOfAKinds, key=scoresort)
            return threeOfAKinds[-1] #return highest

    if cardsneeded >= 2:
        pairs = findPairs(hand)
        if pairs != []:
            pairs = sorted(pairs, key=scoresort)
            return pairs[-1] #return highest

    # nothing, return high card
    return [hand[-1]]

def arrangeHand(cards):

    ## Arrange by best bottom to top

    print "Cards:", cards
    # get at most 5 cards
    back = findBest(cards, 5)
    print "Bottom:", back
    remainingcards = diff(cards, back)
    print "Remaining:", remainingcards

    # get at most 5 cards
    middle = findBest(remainingcards, 5)
    print "Middle:", middle
    remainingcards = diff(remainingcards, middle)
    print "Remaining:", remainingcards

    # get at most 3 cards
    front = findBest(remainingcards, 3)
    print "Top:", front
    remainingcards = diff(remainingcards, front)
    print "Remaining:", remainingcards

    print ""
    print "Filling cards"
    print ""

    if remainingcards:
        ## arrange by best top to bottom
        fillCards(front, remainingcards, 3)
        remainingcards = diff(remainingcards, front)
        print "Top:", front
        print "Remaining:", remainingcards

    if remainingcards:
        fillCards(middle, remainingcards, 5)
        remainingcards = diff(remainingcards, middle)
        print "Middle:", middle
        print "Remaining:", remainingcards

    if remainingcards:
        fillCards(back, remainingcards, 5)
        remainingcards = diff(remainingcards, back)
        print "Bottom:", back
        print "Remaining:", remainingcards

    return front, middle, back

def fillCards(hand, cards, howmany):
    if len(hand) >= howmany:
        return hand

    hand += findBest(cards, howmany - len(hand))
    return fillCards(hand, diff(cards, hand), howmany)

def printCard(card):
    suit = card[-1]
    suit = "♣" if suit == 'c' else suit
    suit = "♠" if suit == 's' else suit
    suit = "❤" if suit == 'h' else suit
    suit = "♦" if suit == 'd' else suit
    return (card[0:-1]).upper() + suit

# -- TESTS --
def  testGetCardValue():
    # ace high
    assert getCardValue('ah') == 14
    # ace low
    assert getCardValue('ah', acehigh=False) == 1
testGetCardValue()

def testSorting():
    tests = [
        (['ah', 'ad', 'ac', 'as'], ['ac', 'as', 'ah', 'ad']),
        (['5h', '2d', '4s', 'ah', '3d'], ['ah', '2d', '3d', '4s', '5h']),
    ]
    for test, expected in tests:
        assert sorted(test, key=cardsort) == expected

def testScoreSort():
    tests = [
        ([['3h', '4h', '5h', '6h', '7h'], ['2h', '3h', '4h', '5h', '6h']], [['2h', '3h', '4h', '5h', '6h'], ['3h', '4h', '5h', '6h', '7h']]),
    ]
    for test, expected in tests:
        assert sorted(test, key=scoresort) == expected

def testIsFlush():
    cards = ['ah', '2h', '3h', '4h', '5h']
    assert isFlush(cards) == True
    cards = ['ah', '2h', '3h', '4h', '6d']
    assert isFlush(cards) == False

def testFlush():
    hand = ['ah', '2h', '3h', '4h', '5h', '7c', '10c', '8c', '8d', '8s', '9s', '9d', '9c']
    flushes = [
        ['ah', '2h', '3h', '4h', '5h'],
    ]
    assert findFlush(hand, True) == flushes

def testIsStraight():
    cards = ['2h', '3h', 'ah', '4h', '5h']
    assert isStraight(cards) == True, "Failed ace low test"
    cards = ['ah', '2h', '3h', '4h', '6h']
    assert isStraight(cards) == False
    cards = ['10h', 'jh', 'ah', 'qh', 'kh']
    assert isStraight(cards) == True, "Failed ace high test"
testIsStraight()

def testStraight():
    hand = ['ah', '2h', '3h', '4h', '5h', '6h', '8h', '8c', '8d', '8s', '9s', '9h', '9c']
    straights = [
        ['2h', '3h', '4h', '5h', '6h'],
        ['2h', '3h', '4h', '5h', 'ah']
    ]
    assert findStraight(hand, True) == straights, findStraight(hand, True)
testStraight()

def testPair():
    hand = ['as', 'ah', '3h', '4h', '5h', '6h', '7h', '8c', '9d', '10s', 'js', 'qh', 'kc']
    pairs = [
        ['as', 'ah']
    ]
    assert findPairs(hand, True) == pairs

def testThreeOfAKind():
    hand = ['as', 'ah', 'ad', '4h', '5h', '6h', '7h', '8c', '9d', '10s', 'js', 'qh', 'kc']
    sets = [
        ['as', 'ah', 'ad']
    ]
    assert findThreeOfAKind(hand, True) == sets

def testFourOfAKind():
    hand = ['as', 'ah', 'ad', 'ac', '4h', '5h', '6h', '7h', '8c', '9d', '10s', 'js', 'qh']
    sets = [
        ['ac', 'as', 'ah', 'ad']
    ]
    assert findFourOfAKind(hand, True) == sets

def testIsPair():
    cards = ('ah', 'ad')
    assert isPair(cards) == True
    cards = ('ah', '2d')
    assert isPair(cards) == False

def testIsFullHouse():
    cards = ('ah', 'ad', 'as', '2h', '2d')
    assert isFullhouse(cards) == True
    cards = ('ah', 'ad', 'as', '3c', '4h')
    assert isFullhouse(cards) == False

def testFindBest():
    testCases = [
        # four of a kind
        ('Four of a kind', ['as', 'ah', 'ad', 'ac', '4h', '5h', '6h', '7h', '8c', '9d', '10s', 'js', 'qh'], ['ac', 'as', 'ah', 'ad']),
        # straight flush
        ('Straight flush', ['ah', '2h', '3h', '4h', '5h', '5d', '7d', '7h', '8c', '9d', '10s', 'js', 'qh'], ['ah', '2h', '3h', '4h', '5h']),
        # full house - use lowest pair possible
        ('Full house', ['ah', 'as', 'ac', '4h', '4d', '2h', '2c', '7h', '8c', '9d', '10s', 'js', 'qh'], ['ac', 'as', 'ah', '2c', '2h']),
        # Flush
        ('Flush', ['ah', '2h', '8s', '4h', '4d', '2h', 'jc', '7h', '8h', '9d', '10s', 'js', 'qh'], ['2h', '4h', '7h', '8h', 'qh']),
    ]
    for title, hand, expected in testCases:
        assert findBest(hand, 5) == expected, title + ": Found " + str(findBest(hand, 5))


def testArrange():
    testCases = [
        # four of a kind + j, straight, 9,q,k
        ('Four of a kind', ['as', 'ah', 'ad', 'ac', '4h', '5h', '6h', '7h', '8c', '9d', 'js', 'qs', 'kh'], ['ac', 'as', 'ah', 'ad', '4h']),
    ]
    for title, hand, expected in testCases:
        arrangeHand(hand)

#testSorting()
#testScoreSort()
#testIsPair()
#testIsFullHouse()
#testIsFlush()
#testFlush()
#testPair()
#testThreeOfAKind()
#testFourOfAKind()
#testFindBest();
# testArrange();



# test input
# 4 of a kind, flush, pair:
# 5h 6h 7h as  4h ac 8c 9d js ah ad  qs kh
# straight, 2 pairs + kicker, 1 pair high card:
# 3h 4s 5c 6d 7d 9d 9c 10s 10c kh kc 3d 2h
# all pairs
# ah ad 3h 3c 5s 5c 7d 7s 9h 9c js jd qh
# straight ace high
# as 2d 3h 4s 5c jd qd 9d 9c 10s 10c kh kc
# straight ace low
# as 2d 3h 4s 5c jd qd 9d 9c 10s 10c 7h 3c
def main():
    cardsinput = raw_input("Enter your cards: ")
    cards = [x for x in cardsinput.split(' ') if x]
    top, middle, bottom = arrangeHand(cards)
    for card in top:
        sys.stdout.write(printCard(card) + ' ')
    print ""
    for card in middle:
        sys.stdout.write(printCard(card) + ' ')
    print ""
    for card in bottom:
        sys.stdout.write(printCard(card) + ' ')
    print ""

main()
