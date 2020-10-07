
from electrum.util import format_amount

BET_ODDSDIVISOR = 10000
NUMBER_OF_OUTCOMES = 36


def get_odd(bettype, rollno):
    if bettype == "even" or  bettype == "odd":
        return BET_ODDSDIVISOR * 2
    elif bettype == "equal":
        return BET_ODDSDIVISOR * NUMBER_OF_OUTCOMES / dice_number_of_win_case(rollno);
    elif bettype == "notequal":
        return BET_ODDSDIVISOR * NUMBER_OF_OUTCOMES / (NUMBER_OF_OUTCOMES - dice_number_of_win_case(rollno))

    elif bettype == "totalunder":
        numberOfWinCases = 0
        for num in range(2, rollno+1):
            numberOfWinCases += dice_number_of_win_case(num)
        return BET_ODDSDIVISOR * NUMBER_OF_OUTCOMES / numberOfWinCases

    elif bettype == "totalover":
        numberOfWinCases = 0
        for num in range(2, rollno+1):
            numberOfWinCases += dice_number_of_win_case(num)
        return BET_ODDSDIVISOR * NUMBER_OF_OUTCOMES / (NUMBER_OF_OUTCOMES - numberOfWinCases);


    #  sum: 2, 3, 4, 5, 6, 7, 8, 9, 10  11, 12
    # result: 1, 2, 3, 4, 5, 6, 5, 4,  3,  2,  1
def dice_number_of_win_case(rollno):
    return (rollno <= 7) * (rollno-1) + (rollno > 7) * (13 - rollno)
    
def calculate_potential_return(betamount,rollno , bettype):
    odds = int(get_odd(bettype,rollno))
    winningsPermille = betamount * odds
    feePermille = betamount * (odds - BET_ODDSDIVISOR) / 1000 * 10 #nFeePermille
    potential_return = (winningsPermille - feePermille) / BET_ODDSDIVISOR 
    return potential_return



