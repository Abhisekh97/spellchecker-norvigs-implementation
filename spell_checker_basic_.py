
import sys
import re # regular expression library; for tokenization of words
from collections import Counter # collections library; counter: dict subclass for counting hashable objects
# import matplotlib.pyplot as plt # for data visualization
import numpy as np
import pandas as pd
import os
print(os.getcwd())
print(os.listdir())


def process_data(file_name):
    """
    Input:
        A file_name which is found in your current directory. You just have to read it in.
    Output:
        words: a list containing all the words in the corpus (text file you read) in lower case.
    """
    words = [] # return this variable correctly


    f = open(file_name, 'r+')
    file_content = f.read()
    # convert all letters to lower case
    file_content = file_content.lower()
    #Convert every word to lower case and return them in a list.
    words = re.findall(r'\w+', file_content)
    ### END CODE HERE ###

    return words

word_l = process_data('shakespeare.txt')
vocab = set(word_l)  # this will be your new vocabulary
with open("vocab.txt", 'w') as file:
   for words in word_l:
      file.writelines(words + "\n")

print(f"The first ten words in the text are: \n{word_l[0:10]}")
print(f"There are {len(vocab)} unique words in the vocabulary.")

def get_count(word_l):
  word_count_dict = Counter(word_l)
  return word_count_dict

word_count_dict = get_count(word_l)
with open("word_count_dict.txt", 'w') as file:
   for key, value in word_count_dict.items():
      file.writelines(key + " " + str(value) + "\n")

def get_probs(word_count_dict):
  m = len(word_l)
  probs = dict()
  with open("probability.txt", 'w') as file:
    for word, count in word_count_dict.items():
      probs[word] = count/m
      file.writelines(word + " " + str(probs[word]) + "\n")
  
  return probs

probs = get_probs(word_count_dict)
print(f"Length of probs is {len(probs)}")
print(f"P('thee') is {probs['thee']:.4f}")

sys.exit()

"""<a name='2'></a>
## 2 - String Manipulations

Now that you have computed $P(w_i)$ for all the words in the corpus, you will write a few functions to manipulate strings so that you can edit the erroneous strings and return the right spellings of the words. In this section, you will implement four functions:

* `delete_letter`: given a word, it returns all the possible strings that have **one character removed**.
* `switch_letter`: given a word, it returns all the possible strings that have **two adjacent letters switched**.
* `replace_letter`: given a word, it returns all the possible strings that have **one character replaced by another different letter**.
* `insert_letter`: given a word, it returns all the possible strings that have an **additional character inserted**.

"""

def delete_letter(word):
  # nice ->
  deleted_list = [word[:i] + word[i+1:] for i in range(len(word))]
  return deleted_list

deleted_letter = delete_letter("cans")
print(deleted_letter)

def switch_letter(word):
  switched_letters = [word[:i] + word[i+1] + word[i]+ word[i+2:] for i in range(len(word) -1) ]
  return switched_letters

def replace_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word
    Output:
        replaces: a list of all possible strings where we replaced one letter from the original word.
    '''



    replace_l = []
    split_l = []
    replace_set = set()

    split_l = [(word[:i], word[i:]) for i in range(len(word)+1)]
    for i in range(ord('a'), ord('z')+1):
        for l, r in split_l:
            if r:
                new_word = l+ chr(i)+ r[1:]
                if new_word != word:
                    replace_set.add(new_word)

    replace_l = sorted(list(replace_set))

    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")

    return replace_l

replace_l = replace_letter(word='can',
                              verbose=True)

def insert_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word
    Output:
        inserts: a set of all possible strings with one new letter inserted at every offset
    '''
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    split_l = []


    split_l = [(word[:i], word[i:]) for i in range(len(word)+1)]
    for l, r in split_l:
        for i in range(len(letters)):
            new_word = l+letters[i]+r
            insert_l.append(new_word)


    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")

    return insert_l

insert_l = insert_letter('at', True)
print(f"Number of strings output by insert_letter('at') is {len(insert_l)}")

def edit_one_letter(word, allow_switches = True):
    """
    Input:
        word: the string/word for which we will generate all possible wordsthat are one edit away.
    Output:
        edit_one_set: a set of words with one possible edit. Please return a set. and not a list.
    """

    edit_one_set = set()

    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))
    # return this as a set and not a list
    return edit_one_set

def edit_two_letters(word, allow_switches = True):
    '''
    Input:
        word: the input string/word
    Output:
        edit_two_set: a set of strings with all possible two edits
    '''

    edit_two_set = set()

    temp_set = edit_one_letter(word, allow_switches = allow_switches)
    for wd in temp_set:
        if wd:
            edit_one = edit_one_letter(wd, allow_switches = allow_switches)
            edit_two_set.update(edit_one)


    return edit_two_set

tmp_edit_two_set = edit_two_letters("a")
tmp_edit_two_l = sorted(list(tmp_edit_two_set))
print(f"Number of strings with edit distance of two: {len(tmp_edit_two_l)}")
print(f"First 10 strings {tmp_edit_two_l[:10]}")
print(f"Last 10 strings {tmp_edit_two_l[-10:]}")
print(f"The data type of the returned object should be a set {type(tmp_edit_two_set)}")
print(f"Number of strings that are 2 edit distances from 'at' is {len(edit_two_letters('at'))}")

def get_corrections(word, probs, vocab, n=2, verbose = False):
    '''
    Input:
        word: a user entered string to check for suggestions
        probs: a dictionary that maps each word to its probability in the corpus
        vocab: a set containing all the vocabulary
        n: number of possible word corrections you want returned in the dictionary
    Output:
        n_best: a list of tuples with the most probable n corrected words and their probabilities.
        suggestions = list((word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab))
        n_best = [[s, probs[s]] for s in list(reversed(suggestions))]
    '''

    suggestions = []
    n_best = []

    #Step 1: create suggestions as described above
    if word in vocab:
        suggestions.append(word)
    else:
        edit_one_list = edit_one_letter(word)
        candidate1 = edit_one_list.intersection(vocab)
        edit_two_list = edit_two_letters(word)
        candidate2 = edit_two_list.intersection(vocab)
        suggestions = list(candidate1 or candidate2)
    if len(suggestions) == 0:
        suggestions.append(word)
#     suggestions = list((word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab))

    #Step 2: determine probability of suggestions


    #Step 3: Get all your best words and return the most probable top n_suggested words as n_best
    n_best = [[s, probs[s]] for s in suggestions]


    if verbose: print("entered word = ", word, "\nsuggestions = ", suggestions)

    return n_best

my_word = 'dys'
tmp_corrections = get_corrections(my_word, probs, vocab, 2, verbose=True) # keep verbose=True
for i, word_prob in enumerate(tmp_corrections):
  print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")

def min_edit_distance(source, target, ins_cost = 1, del_cost = 1, rep_cost = 2):
  row = len(source)
  col = len(target)
  t = np.zeros((row+1, col+1), dtype= int)
  for i in range(1, row+1):
    t[i][0] = t[i-1][0] + del_cost
  for j in range(1, col+1):
    t[0][j] = t[0][j-1] + ins_cost


  for i in range(1, row+1):
    for j in range(1, col+1):
      if source[i-1] == target[j-1]:
        t[i][j] = t[i-1][j-1]
      else:
        t[i][j] = min(t[i-1][j] + ins_cost, t[i][j-1]+del_cost, t[i-1][j-1]+rep_cost)
  #initialization
  return t, t[row][col]

source =  'play'
target = 'stay'
matrix, min_edits = min_edit_distance(source, target)
print("minimum edits: ",min_edits, "\n")
idx = list('#' + source)
cols = list('#' + target)
df = pd.DataFrame(matrix, index=idx, columns= cols)
print(df)

source =  'eer'
target = 'near'
matrix, min_edits = min_edit_distance(source, target)
print("minimum edits: ",min_edits, "\n")
idx = list(source)
idx.insert(0, '#')
cols = list(target)
cols.insert(0, '#')
df = pd.DataFrame(matrix, index=idx, columns= cols)
print(df)

_, min_edit = min_edit_distance("dys", "days")
print(min_edit)
_, min_edit = min_edit_distance("dys", "dye")
print(min_edit)

