import unittest

#helpers
def Count(dice, number):
    return len([y for y in dice if y == number])

def HighestRepeated(dice, minRepeats):
    unique = set(dice)
    repeats = [x for x in unique if Count(dice, x) >= minRepeats]
    return max(repeats) if repeats else 0

def OfAKind(dice, n):
    return HighestRepeated(dice,n) * n

def SumOfSingle(dice, selected):
    return sum([x for x in dice if x == selected])

#strategies
def Chance(dice):
    return sum(dice)

def Pair(dice):
    return OfAKind(dice, 2)

def ThreeOfAKind(dice):
    return OfAKind(dice, 3)

def FourOfAKind(dice):
    return OfAKind(dice, 4)

def SmallStraight(dice):
    return 15 if tuple(sorted(dice)) == (1,2,3,4,5) else 0

def LargeStraight(dice):
    return 20 if tuple(sorted(dice)) == (2,3,4,5,6) else 0

def Ones(dice):
    return SumOfSingle(dice,1)

def Twos(dice):
    return SumOfSingle(dice,2)

def Threes(dice):
    return SumOfSingle(dice,3)

def Fours(dice):
    return SumOfSingle(dice,4)

def Fives(dice):
    return SumOfSingle(dice,5)

def Sixes(dice):
    return SumOfSingle(dice,6)

def Yahtzee(dice):
    return 50 if len(dice) == 5 and len(set(dice)) == 1 else 0

class YahtzeeTest(unittest.TestCase):
    testCases = (
        ((1,2,3,4,5), 1, Ones),
        ((1,2,3,4,5), 2, Twos),
        ((3,2,3,4,3), 9, Threes),
        ((3,2,3,4,3), 0, Sixes),
        ((1,2,3,4,5), 0, Pair), # no pairs found
        ((1,5,3,4,5), 10, Pair), # one pair found
        ((2,2,6,6,4), 12, Pair), # picks highest
        ((2,3,1,3,3), 6, Pair), # only counts two
        ((2,2,6,6,6), 18, ThreeOfAKind),
        ((2,2,4,6,6), 0, ThreeOfAKind), # no threes found
        ((5,5,5,5,5), 15, ThreeOfAKind), # only counts three
        ((6,2,6,6,6), 24, FourOfAKind),
        ((2,6,4,6,6), 0, FourOfAKind), # no fours found
        ((5,5,5,5,5), 20, FourOfAKind), # only counts four
        ((1,2,5,4,3), 15, SmallStraight),
        ((1,2,5,1,3), 0, SmallStraight),
        ((6,2,5,4,3), 20, LargeStraight),
        ((1,2,5,1,3), 0, LargeStraight),
        ((5,5,5,5,5), 50, Yahtzee),
        ((1,5,5,5,5), 0, Yahtzee),
        ((1,2,3,4,5), 15, Chance),
        )

    def testRunAll(self):
        for (dice, expected, strategy) in self.testCases:
            score = strategy(dice)
            self.assertEquals(expected, score, "got {0} expected {1}, testing with {2} on {3}".format(score, expected, strategy.__name__, dice))
        print ('ran {0} test cases'.format(len(self.testCases)))

if __name__ == '__main__':
    unittest.main()