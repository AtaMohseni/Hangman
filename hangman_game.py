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
        
        self.words_to_freq =  Frequencies()
        self.available_letters = [chr(x) for x in range(65,91)]
        self.unavailable_letters = []
        self.final_word = [None for x in range(5)]
        
    
    def _prob_evidence_given_word(self,word):
        
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
        #calculate the probability of revieled evidence so far (marginalization)
        summation = 0
        
        for word in self.words_to_freq.keys():
            summation += self._prob_evidence_given_word(word) * self.words_to_freq[word] 
            
        return summation
    
    def _prob_word_given_evidence(self, word,probability_of_evidence):
        return (self._prob_evidence_given_word(word)*self.words_to_freq[word])/(probability_of_evidence)
    
    def _prob_guess_given_word(self,letter,word):
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
        summation = 0
        for word in self.words_to_freq.keys():
            summation += self._prob_guess_given_word(letter,word) * self._prob_word_given_evidence(word,probability_of_evidence)
            
        return summation
    
    
    def guess(self):
        
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
        
        import time
        print ("please choose a 5-letter word in your mind (all upper chase)")
        time.sleep(10)
        
        while None in self.final_word:
            g = self.guess() 
            print ("my guess is letter: \t",g)
            
            value = input("is the letter exist in the word in your mind? (type Yes or No) or type exit:\t")
            
            if str(value.lower()) == "yes":
                
                locations = input("please type the location(s) of the letter in the word, number(s) between 0 to 4 (separated by comma):\t")
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
                
            elif str(value.lower()) == "no":
                self.unavailable_letters.append(str(g))
                
            elif str(value.lower()) == "exit":
                break
            else:
                print("not a valid input")
        

