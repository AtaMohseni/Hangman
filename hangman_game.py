# -*- coding: utf-8 -*-

from word_frequencies import Frequencies

class Hangman:
    
    """ This is implementation of Hangman Game beilief network and
    bayesian updates to solve a Hangman Game quickly. To test the performance,
    user will choose a 5-letter words in his/her mind, then the program
    guesses the letters, and user should only tell if the letter exists
    or not in that word. If exists, user should tell the location of that
    letter in the word."""
    
    def __init__(self):
        
        #dictionary that maps words to their frequency or P(W = w)
        self.words_to_freq =  Frequencies()
        #list of available letters to guess
        self.available_letters = [chr(x) for x in range(65,91)]
        #list of unavailable letters (either gussed correctly or guessed incorrecly)
        self.unavailable_letters = []
        # list of chracters to be placed in 5-letter word during the game
        self.final_word = [None for x in range(5)]
        
    
    def _prob_evidence_given_word(self,word):
        
        """ calculates and return the probability of revieled evidence given a word, 
        which is equal to either zero or one. P(E | W = w)"""
        
        prob = 0
        for index in range(len(self.final_word)):
            if self.final_word[index] == None:
                if word[index] in self.unavailable_letters:
                    prob =0
                    return prob
                else:
                    prob = 1
            else:
                if self.final_word[index] == word[index]:
                    prob =1
                else:
                    prob = 0
                    return prob
        return prob
                    
                    
    def _prob_evidence(self):
        
        """calculate the probability of revieled evidence,
        by using marginalization and sum over all words. it needs should 
        be calculated only once before each time we make a guess.
        P(E) = SUM[ P(E | W = w') P(W = w') ] for all w' """
        
        summation = 0
        for word in self.words_to_freq.keys():
            summation += self._prob_evidence_given_word(word) * self.words_to_freq[word] 
            
        return summation
    
    def _prob_word_given_evidence(self, word,probability_of_evidence):
        
        """ calculate probability of a word given evidence using bayes rule.
        P(W = w | E)"""
        
        return (self._prob_evidence_given_word(word)*self.words_to_freq[word])/(probability_of_evidence)
    
    def _prob_guess_given_word(self,letter,word):
        
        """ calculate the probability of a guess for a letter given a word.
        it should return 1 if letter l is in a word in positions that we still
        need to guess.
        P( Li = l for some i in index {0,1,2,3,4} | W = w )"""
        
        prob = 0
        for index in range(len(self.final_word)):
            if self.final_word[index] != None:
                pass
            else:
                if word[index] == letter:
                    prob = 1
                    return prob
        return prob
    
    def _prob_guess_given_evidence(self,letter,probability_of_evidence):
        
        """ calculate the probability of a guess for a word given current
        revealed evidence. it uses marginalization to sum over all words in 
        dictionary.
        P(Li = l for some i in index {0,1,2,3,4} | E) = 
        Sum [ P( Li = l for some i in index {0,1,2,3,4} | W = w ) P(W = w |E)]
        for all w """
        
        summation = 0
        for word in self.words_to_freq.keys():
            summation += self._prob_guess_given_word(letter,word) * self._prob_word_given_evidence(word,probability_of_evidence)
            
        return summation
    
    
    def guess(self):
        """ This method calculates the probability each available letter givern evidence
        and returns the most probable letter as a next guess"""
        
        # initiate the list to calculate probability of next letter as a best guess
        available_letters_probs = [] 
        
        #calculate the probability of revieled evidence so far
        probability_of_evidence = self._prob_evidence()
        
        for letter in self.available_letters:
            available_letters_probs.append(self._prob_guess_given_evidence(letter,probability_of_evidence))
            
        best_index = available_letters_probs.index(max(available_letters_probs))
        best_next_letter = self.available_letters[best_index]
        
               
        return best_next_letter
    
    def play(self):
        
        """ This method starts the game. it asks the user to think of a five
        letter word and keep it unknown, and then program starts guessing
        letters one by one. After each guess, user is asked to confirm wether
        the gussed letter is in that 5 letters unknown word and if it is,
        user is asked to type the index of the guessed letter in the
        unknow word"""
        
        import time
        print ("please think of a 5-letter word in your mind (all upperchase)")
        
        time.sleep(5)
        
        while None in self.final_word:
            g = self.guess() 
            print ("\nmy guess is letter:  ",g)
            value = input("is the letter exist in the word in your mind? (type Yes or No) or type exit:  ")
            
            if str(value.strip().lower()) == "yes":
                
                locations = input("please type the location(s) of the letter in the word, number(s) between 0 to 4 (separated by comma):  ")
                locations = [x.strip() for x in locations.split(',')]
                
                for index in locations:
                    if index.isnumeric():
                        self.final_word[int(index)] = g
                    else:
                        print("not a valid input")
                        break
                    
                self.available_letters.remove(str(g))
                self.unavailable_letters.append(str(g))
                
                print("correct letters sofar: \t", self.final_word)
                
            elif str(value.strip().lower()) == "no":
                self.unavailable_letters.append(str(g))
                
            elif str(value.lower()) == "exit":
                break
                
            else:
                print("not a valid input")
        
        if None not in self.final_word:
            print('Final word is:', "".join(self.final_word))
if __name__ == "__main__":
    game = Hangman()
    game.play()
    
    