# -*- coding: utf-8 -*-
import random
import os
import itertools

HIT = 'HIT'
STAY = 'STAY'

HUMAN = 'HUMAN'
DEALER = 'DEALER' # computer player

CLUB = 'CLUB'
HEART = 'HEART'
SPADE = 'SPADE'
DIAMOND = 'DIAMOND'

class Card:
    def __init__(self, number, suit):
        if number >= 1 and number <=10:
            self.value = number
        elif number == 11 or number == 12 or number == 13:
            self.value = 10
        else:
            print "wrong number for card"
            sys.exit(-1)
        self.number = number
        self.suit = suit
        #print "Drawn card: ", self.number, self.suit,"(",self.value,")"


class Blackjack:
    """
    Objective of the game: to have the most points.
    Points are awarded to the player whose hand value is closest to 21 without going over.
    -There will be two participants in the game. One human (player) and one computer (dealer).
    -A game includes one shuffled deck of cards.
    -A game is comprised of any number of rounds.
    -A round starts with both the dealer and the player each getting two cards chosen at random from
    the deck.
    --The player's cards will be displayed with the value of the hand.
    --The player will be able to choose to "[H]it" or "[S]tay."
    --If the player "hits" they will be given another card and will be asked to chose "hit" or "stay"
    again.
    --If the player "stays" their turn will be over.
    --If the sum of the card values exceed 21 their turn will be over and they lose the round.
    -When the player is done, the dealer's turn begins as above.
    -Which ever player is closest to 21 without going over is the winner of the round and receives one
    point.
    -If there is a tie then no points are awarded and play continues to the next round.
    -Another round begins until the program is ended (Ctrl-C).
    Deck And Card Values
    -A standard 52 card deck will be used.
    -4 Suits (Hearts, Diamonds, Spades, Clubs).
    -Number cards (Cards 2 - 10) are always worth the face value.
    -Face cards (Jack, Queen, King) are always worth 10.
    -Ace cards are worth either 1 or 11, whichever is most advantageous to the hand.
    """

    def __init__(self):
        self.player_cards = []
        self.dealer_cards = []
        self.max_points = 21
        self.n_cards = 52
        self.current_player = HUMAN
        self.suit2symbol= {}
        self.suit2symbol[HEART] = '♥'
        self.suit2symbol[SPADE] = '♠'
        self.suit2symbol[DIAMOND] = '♦'
        self.suit2symbol[CLUB] = '♣'
        self.remaining_deck = range(1, 52)

        print("\n\n\n\nStarting Blackjack game...\n")#Full deck available: ",self.remaining_deck)

    def play(self):
        self.player_cards = []
        self.dealer_cards = []
        # first round: 2 cards for each player
        for i in range(2):
            self.player_cards.append(self.get_card())
            self.dealer_cards.append(self.get_card())
        print "First round: \n Player got: "
        self.print_cards_and_get_points(HUMAN)
        print "\n Dealer got: "
        self.print_cards_and_get_points(DEALER)
        if self.score_overpasses_max(HUMAN) or self.score_overpasses_max(DEALER):
            self.print_results()
            return
        try:
            # Player's turn
            option = HIT
            while not self.score_overpasses_max(HUMAN) and option != STAY:
                option = self.play_turn(HUMAN)
            if self.score_overpasses_max(HUMAN):
                self.print_results()
                return

            # Dealer's turn
            option = HIT
            while not self.score_overpasses_max(DEALER) and option != STAY:
                option = self.play_turn(DEALER)
            if self.score_overpasses_max(DEALER):
                self.print_results()
        except KeyboardInterrupt:
            print "Blackjack Game ended!"
            self.print_results()

    def score_overpasses_max(self, player):
        points = self.get_points_sum(player)
        if points >= self.max_points:
            return True
        else:
            return False

    def play_turn(self, player):
        """
        Returns the player's turn decision: HIT or STAY
        """
        print "********\nGame score:"#" Player=", self.player_points, " Dealer: ", self.dealer_points
        if player == DEALER:
            self.print_cards_and_get_points(DEALER)
        elif player == HUMAN:
            self.print_cards_and_get_points(HUMAN)
        else:
            print "Error: Wrong player!"
            sys.exit(-1)
        try:
            if player == HUMAN:
                choice = str(raw_input(" [H]it or [S]tay? :"))
                while choice != 'H' and choice != 'S':
                    print "Not a valid option, input H or S"
                    choice = str(raw_input(" [H]it or [S]tay? :"))
                if choice == 'H':
                    self.player_cards.append(self.get_card())
                    self.print_cards_and_get_points(HUMAN)
                    return HIT
                elif choice == 'S':
                    return STAY
            elif player == DEALER:
                return self.play_dealer()
            else:
                print "wrong player in play_turn, call with HUMAN or DEALER"

        except ValueError:
            print "Not a valid option, input H or S"

    def play_dealer(self):
        """
        Safe player dealer stays after he reaches 17 as a safe bet strategy to win,
        while he does not go over 21
        """
        while not self.score_overpasses_max(DEALER) and (self.max_points - self.get_points_sum(DEALER))< 17:
            self.dealer_cards.append(self.get_card())
            self.print_cards_and_get_points(DEALER)
        return STAY

    def print_results(self):
        print "************** GAME ENDS: "
        player_score = self.print_cards_and_get_points(HUMAN)
        dealer_score = self.print_cards_and_get_points(DEALER)
        if player_score > self.max_points:
            print "----> Dealer wins! (P: ",player_score, ", D: ",dealer_score,")"
        elif dealer_score > self.max_points:
            print "----> Player wins! (P: ",player_score, ", D: ",dealer_score,")"
        elif player_score == self.max_points:
            print "----> Player wins! (P: ",player_score, ", D: ",dealer_score,")"
        elif dealer_score == self.max_points:
            print "----> Dealer wins! (P: ",player_score, ", D: ",dealer_score,")"
        elif (self.max_points-dealer_score) > (self.max_points -player_score):
            print "----> Player wins! (P: ",player_score, ", D: ",dealer_score,")"
        elif (self.max_points-dealer_score) < (self.max_points -player_score):
            print "----> Dealer wins! (P: ",player_score, ", D: ",dealer_score,")"
        elif dealer_score == player_score:
            print "----> ----> ----> Tie! (P: ",player_score, ", D: ",dealer_score,")"
        else:
            print "----> ----> ----> Wrong unfeasible option! ",player_score, ", D: ",dealer_score,")"

    def print_cards_and_get_points(self, player):
        if player == DEALER:
            cards = self.dealer_cards[:]
        elif player == HUMAN:
            cards = self.player_cards[:]
        else:
            print "wrong player in get_points_sum: ",player
            sys.exit(-1)
        print player,
        for c in cards:
            print " [",str(c.number), self.suit2symbol[c.suit],"]",
        points = self.get_points_sum(player)
        print " = ", points
        return points

    def get_points_sum(self, player):
        if player == HUMAN:
            cards = self.player_cards[:] # needed to make the full copy
        elif player == DEALER:
            cards = self.dealer_cards[:]
        else:
            print "wrong player in get_points_sum: ",player
            sys.exit(-1)
        cards.sort(key=lambda x: x.number,reverse=True) # if assigned to new var, becomes None (?)
        total = 0
        total_aces = 0
        for c in cards:
            if c.number !=1:
                total += c.value
            else:
                total_aces += 1
        # compute most optimal value for the ACES
        if total_aces>0:
            aces_values = [1, 11]
            possible_hand_values = set()
            # check best score by considering every possible hand punctuation  (there is 2** total aces)
            # cartesian product to obtain all possibilities of hand values list(itertools.product([1,2], repeat=3))
            possibilities = set(list(itertools.product(aces_values, repeat=total_aces)))#combinations(aces_values, 2)) # length of each combination # does not produce same item repetitions
            for combination_tuple in possibilities:
                possible_score = total
                for i in range(len(combination_tuple)):
                    possible_score += combination_tuple[i]
                possible_hand_values.add(possible_score)
            return self.select_best_possible_score(possible_hand_values)
        else:
            return total

    def select_best_possible_score(self, possible_hand_values):
        promising_scores = set()
        for score in possible_hand_values:
            if score <= self.max_points:
                promising_scores.add(score)

        if len(promising_scores)>0:
            return max(promising_scores)
        else:
            # doesnt matter, the game is lost, but choose the min
            return min(possible_hand_values)

    def get_card(self):
        """
        Draws a card from the deck.
        random.sample returns a k length list of unique elements chosen from the population sequence
        (Used for random sampling without replacement).
        """
        #random.sample(xrange(len(mylist)), sample_size)
        card_id = random.sample(self.remaining_deck, 1)[0] # n_cards
        #print "Before taking card: ", card_id, self.remaining_deck
        self.remaining_deck.remove(card_id)
        #print "After taking card: ", self.remaining_deck
        range_per_club = 13 #52/4
        if card_id / range_per_club == 0:
            suit = CLUB
        elif card_id / range_per_club == 1:
            suit = HEART
        elif card_id / range_per_club == 2:
            suit = SPADE
        elif card_id / range_per_club == 3:
            suit = DIAMOND
        else:
            print "Invalid suit error!"
        card_number = (card_id%range_per_club)+1
        print "Got card: ",card_id, "(-> ",card_number,")"
        return Card(card_number, suit)

if __name__ == "__main__":
    bj = Blackjack()
    bj.play()
