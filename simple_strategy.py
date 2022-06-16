from enum import Enum, auto

CARDS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11)


class StrategyIndex(Enum):
    SPLIT = auto()
    SOFT = auto()
    HARD = auto()
    SURRENDER = auto()


class BetAction(Enum):
    STAND = auto()
    HIT = auto()
    DOUBLE = auto()
    SPLIT = auto()
    FINISHED = auto()


SIMPLE_STRATEGY = {
    StrategyIndex.SPLIT: {
        11: {n: True for n in CARDS},
        10: {n: False for n in CARDS},
        9: {n: n not in {7, 10, 11} for n in CARDS},
        8: {n: True for n in CARDS},
        7: {n: n < 8 for n in CARDS},
        6: {n: n < 7 for n in CARDS},  # TODO: Y/N if dealer has 2 depends on DAS (Double after Split)
        5: {n: False for n in CARDS},
        4: {n: False for n in CARDS},
        3: {n: n < 8 for n in CARDS},
        2: {n: n < 8 for n in CARDS},
    },
    StrategyIndex.SOFT: {
        21: {n: BetAction.STAND for n in CARDS},
        20: {n: BetAction.STAND for n in CARDS},
        19: {n: BetAction.STAND if n != 6 else BetAction.DOUBLE for n in CARDS},
        18: {
            2: BetAction.DOUBLE, 3: BetAction.DOUBLE, 4: BetAction.DOUBLE, 5: BetAction.DOUBLE, 6: BetAction.DOUBLE,
            7: BetAction.SPLIT, 8: BetAction.SPLIT,
            9: BetAction.STAND, 10: BetAction.STAND, 11: BetAction.STAND,
        },
        17: {
            2: BetAction.HIT,
            3: BetAction.DOUBLE, 4: BetAction.DOUBLE, 5: BetAction.DOUBLE, 6: BetAction.DOUBLE,
            7: BetAction.HIT, 8: BetAction.HIT, 9: BetAction.HIT, 10: BetAction.HIT, 11: BetAction.HIT,
        },
        16: {
            2: BetAction.HIT, 3: BetAction.HIT,
            4: BetAction.DOUBLE, 5: BetAction.DOUBLE, 6: BetAction.DOUBLE,
            7: BetAction.HIT, 8: BetAction.HIT, 9: BetAction.HIT, 10: BetAction.HIT, 11: BetAction.HIT,
        },
        15: {
            2: BetAction.HIT, 3: BetAction.HIT,
            4: BetAction.DOUBLE, 5: BetAction.DOUBLE, 6: BetAction.DOUBLE,
            7: BetAction.HIT, 8: BetAction.HIT, 9: BetAction.HIT, 10: BetAction.HIT, 11: BetAction.HIT,
        },
        14: {
            2: BetAction.HIT, 3: BetAction.HIT, 4: BetAction.HIT,
            5: BetAction.DOUBLE, 6: BetAction.DOUBLE,
            7: BetAction.HIT, 8: BetAction.HIT, 9: BetAction.HIT, 10: BetAction.HIT, 11: BetAction.HIT,
        },
        13: {
            2: BetAction.HIT, 3: BetAction.HIT, 4: BetAction.HIT,
            5: BetAction.DOUBLE, 6: BetAction.DOUBLE,
            7: BetAction.HIT, 8: BetAction.HIT, 9: BetAction.HIT, 10: BetAction.HIT, 11: BetAction.HIT,
        },
    },
    StrategyIndex.HARD: {
        21: {n: BetAction.STAND for n in CARDS},
        20: {n: BetAction.STAND for n in CARDS},
        19: {n: BetAction.STAND for n in CARDS},
        18: {n: BetAction.STAND for n in CARDS},
        17: {n: BetAction.STAND for n in CARDS},
        16: {n: BetAction.STAND if n < 7 else BetAction.HIT for n in CARDS},
        15: {n: BetAction.STAND if n < 7 else BetAction.HIT for n in CARDS},
        14: {n: BetAction.STAND if n < 7 else BetAction.HIT for n in CARDS},
        13: {n: BetAction.STAND if n < 7 else BetAction.HIT for n in CARDS},
        12: {n: BetAction.STAND if 4 > n > 6 else BetAction.HIT for n in CARDS},
        11: {n: BetAction.DOUBLE for n in CARDS},
        10: {n: BetAction.DOUBLE if n < 10 else BetAction.DOUBLE for n in CARDS},
        9: {n: BetAction.DOUBLE if 2 < n < 7 else BetAction.STAND for n in CARDS},
        8: {n: BetAction.DOUBLE if 2 < n < 7 else BetAction.STAND for n in CARDS},
        7: {n: BetAction.HIT for n in CARDS},
        6: {n: BetAction.HIT for n in CARDS},
        5: {n: BetAction.HIT for n in CARDS},
        4: {n: BetAction.HIT for n in CARDS}
    },

    StrategyIndex.SURRENDER: {
        16: {n: n > 8 for n in CARDS},
        15: {n: n == 10 for n in CARDS}
    }
}
