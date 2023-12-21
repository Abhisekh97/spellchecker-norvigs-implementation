from time import time
vocab = None
with open("vocab.txt") as file:
    vocab = file.read()
    vocab = vocab.split('\n')

print(vocab)
probability_dict = {}
with open("probability.txt") as file:
    for line in file:
        key, val = line.split()
        probability_dict[key] = float(val)
print(probability_dict)
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

    # if verbose: print(f"Input word = {word} \\nsplit_l = {split_l} \\n replace_l {replace_l}")
    if verbose: print('Input word = {} \n split_l = {}\n replace_l {}'.format(word, split_l, replace_l))


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


    if verbose: 
        print("Input word {} \n split_l = {} \n insert_l = {insert_l}".format(word, split_l))

    return insert_l



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



if __name__ == '__main__':
    while True:
        
        print("Enter text to correct")
        t = input()
        print("Input Text:",t)
        st = time() 
        print("Corrected Text :",get_corrections(t,probability_dict, vocab, 2, True))

        print("Time Elapsed : {} ms".format(round((time()-st)*1000,3)))