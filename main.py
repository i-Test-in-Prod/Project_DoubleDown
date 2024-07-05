import random
import time

def Clubs(Deck):
    ClubList = []
    for x in Deck:
        x = str(x) + '♣'
        ClubList.append(x)
    return ClubList

def Diamonds(Deck):
    DiamondsList = []
    for x in Deck:
        x = str(x) + '♦'
        DiamondsList.append(x)
    return DiamondsList

def Hearts(Deck):
    HeartsList = []
    for x in Deck:
        x = str(x) + '♥'
        HeartsList.append(x)
    return HeartsList

def Spades(Deck):
    SpadesList = []
    for x in Deck:
        x = str(x) + '♠'
        SpadesList.append(x)
    return SpadesList

def create_deck(cardRanks):
    suits = ['♣', '♦', '♥', '♠']
    ranks = cardRanks
    # creates a list of dictionaries with keys 'rank' and 'suit'. 
    deck = [[str(rank) + suit] for suit in suits for rank in ranks]
    random.shuffle(deck)
    # print(deck)
    return deck

def card_value(card):
    # print(f"Card is: {card}")
    card = str(card)[2:-3]
    if card in ['2','3','4','5','6','7','8','9']:
        return int(card)
    elif card in ['10','J','Q','K']:
        return 10
    else: # Ace
        return 11

def ace_value(cardInHand,currHandSum): # determine if ace is 11 or 1
    if currHandSum + 11 > 21:
        return 1
    else: 
        return 11

def next_card(shoe,currHand,currHandSum):
    pulled_card = shoe.pop()
    currHand.append(pulled_card)
    cardValue = card_value(pulled_card)
    # """ if cardValue = 11:
    #     cardValue = ace_value(currHand,currHandSum) """
    new_hand_sum = currHandSum + cardValue
    return currHand, new_hand_sum

def deal(deck): # gives the player then dealer a card 2x
    PlayerHand = []
    DealerHand = []
    shoe = deck
    PlayerHand, playerHandTotal = next_card(shoe,PlayerHand,0)
    DealerHand, dealerTotal = next_card(shoe,DealerHand,0)
    PlayerHand, playerHandTotal = next_card(shoe,PlayerHand,playerHandTotal)
    DealerHand, dealerTotal = next_card(shoe,DealerHand,dealerTotal)
    # playerHandTotal = card_value(PlayerHand) 
    # DealerHand.append(next_card(shoe))
    # dealerTotal = card_value(DealerHand)
    # print(f"DealerHand: {DealerHand} | Dealer total: {dealerTotal}")
    # print(f"Dealer: {DealerHand[0]} | {card_value(DealerHand[0])}")
    # print(f"PlayerHand: {PlayerHand} | {playerHandTotal}")
    return DealerHand, dealerTotal, PlayerHand,playerHandTotal

def dealer_check_hole_card(DealerHand,dealerTotal):
    print(f"Uh-oh, Dealer showing {card_value(DealerHand[0])}!")
    time.sleep(1)
    print("Checking hole card...")
    time.sleep(1)
    if dealerTotal == 21:
        print("Ouch! Dealer has Blackjack 😡")
        alive_bust = "bust" # maybe need to rename, but for now is just indicating that dealer does not need to take action
        return "Home"
    else: 
        print("Whew, Dealer does not have Blackjack 😤")
        alive_bust = "alive"
        return "NotHome"

def offer_insurance(): # block that defines actions to take for players taking insurance
    # insurance offered here
    if input("Take insurance? Y/N: ") != "Y":
        return "N"
    else:
        return "Y"

def end_of_hand(dealerTotal,playerHandTotal): # block that compares scores and announces result.
    print(">>>Hand is over!")
    time.sleep(1)
    print(f"Dealer: {dealerTotal} | {DealerHand}")
    print(f"Player: {playerHandTotal} | {PlayerHand}")
    time.sleep(1)
    # if dealer busts or player > dealer
    if dealerTotal > 21 or (playerHandTotal > dealerTotal and playerHandTotal <= 21):
        print("You win!")
    elif dealerTotal == playerHandTotal:
        print("Push!")
    else:
        print("You lose, better luck next time!")
    # reset_hand() # not yet defined
    # playerHandTotal = 0

def play_hand(deck,PlayerHand,playerHandTotal): # block of code that defines the playing of a hand
    while playerHandTotal <= 21:
        playerAction = input(f"Hand total: {playerHandTotal} - Hit or Stand? ")
        if playerAction == "Hit":
            deck, PlayerHand, playerHandTotal = player_hit(deck,PlayerHand,playerHandTotal)
            print(f"PlayerHand: {PlayerHand} | {playerHandTotal}")
            time.sleep(1)
        else: # playerAction = STAND
            alive_bust = "alive"
            return deck, PlayerHand, playerHandTotal, alive_bust          
    if playerHandTotal > 21:
        print("BUST!")
        alive_bust = "bust"
        return deck, PlayerHand,playerHandTotal, alive_bust

def dealer_action_s17(deck,DealerHand,dealerTotal): # block of code that defines what the dealer will do
    print("Flipping dealer's hole card...")
    time.sleep(1)
    print(f"Dealer hand: {DealerHand} | {dealerTotal}")
    while dealerTotal < 17:
        print(f"Dealer has {dealerTotal}, dealer hits...")
        time.sleep(1)
        deck, DealerHand, dealerTotal = player_hit(deck,DealerHand,dealerTotal)
        print(DealerHand," | ",dealerTotal)
        time.sleep(1)
    if dealerTotal >= 17 and dealerTotal <= 21:
        # print(deck)
        # print(DealerHand)
        # print(dealerTotal)
        return deck, DealerHand, dealerTotal
    if dealerTotal > 21:
        print("Dealer BUSTS!")
        return deck, DealerHand, dealerTotal

def player_hit(deck,PlayerHand,playerHandTotal):
    shoe = deck
    PlayerHand, playerHandTotal = next_card(shoe,PlayerHand,playerHandTotal)
    return deck, PlayerHand, playerHandTotal
    
# Main Program

cardRanks = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
deck = create_deck(cardRanks)

# deal(deck) 
DealerHand, dealerTotal, PlayerHand, playerHandTotal = deal(deck)

print(f"Dealer: {DealerHand[0]} | {card_value(DealerHand[0])}") # dealer has a fair hand
print(f"PlayerHand: {PlayerHand} | {playerHandTotal}")

# Checking for Blackjack
# if Player dealt Blackjack
if playerHandTotal == 21: # if player's first two cards sum to 21:
    alive_bust = "alive"
    playerBJ = True
    print("Blackjack!")
    time.sleep(1)
    if card_value(DealerHand[0]) == 10: # dealer shows 10, need to check for ace in hole
        if dealer_check_hole_card(DealerHand,dealerTotal) == "Home":
            # dealer and player have blackjack
            alive_bust = "bust" # may need to be re-worked
            print("PUSH! At least it's not a loss...")
        else: # Player has blackjack and dealer not showing a 10 
            print("YES!")
           

# p1 <> blackjack and dealer shows 10
elif card_value(DealerHand[0]) == 10:
    playerBJ = False
    if dealer_check_hole_card(DealerHand,dealerTotal) == "Home":
        # dealer has blackjack
        alive_bust = "bust" # may need to be reworked
        end_of_hand(dealerTotal,playerHandTotal)
    else:
        # neither player has blackjack
        deck, PlayerHand, playerHandTotal, alive_bust = play_hand(deck,PlayerHand,playerHandTotal)

# dealer showing Ace        
elif card_value(DealerHand[0]) == 11:
    playerBJ = False
    insurance = offer_insurance()
    # no one takes insurance
    if insurance != "Y":
        if dealer_check_hole_card(DealerHand,dealerTotal) == "Home":
            #dealer has Ace-up blackjack
            end_of_hand(dealerTotal,playerHandTotal)
        else: 
            # dealer does not have Ace-up blackjack
            deck, PlayerHand, playerHandTotal, alive_bust = play_hand(deck,PlayerHand,playerHandTotal)
    elif insurance != "Y": 
        print("[Insurance was taken]")
else: 
    playerBJ = False
    deck, PlayerHand, playerHandTotal, alive_bust = play_hand(deck,PlayerHand,playerHandTotal)

if alive_bust == "alive" and not playerBJ:
    deck, DealerHand, dealerTotal = dealer_action_s17(deck,DealerHand,dealerTotal)
    
end_of_hand(dealerTotal,playerHandTotal)