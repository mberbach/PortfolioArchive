# -*- coding: utf-8 -*-

import builtins
import csv
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

fname = '/stat129/nonprofit-desc.csv'
doc = []
patUn = re.compile(r'^(?=.{1,250}$).*?(native plant|biodiversity|wildlife)', flags=re.IGNORECASE)

# output file, easier to read
with open('wrMOutFi129mb.txt', 'w') as outfile:

    # print() wrap to file out
    def print(*args, **kwargs):
            builtins.print(*args, **kwargs, file=outfile)

    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # is this causing strings that have joined words?
            # aka words with no whitespace between them?
            # I tried creating a solution, but it didn't seem to work
            # maybe I don't understand what is going wrong yet...
            # Print statement issue?
            for dsc in row[2:]:
                if row[2] != '':
                    doc.append(dsc.strip())


    cv = CountVectorizer()
    tv = TfidfVectorizer()
    ncv = CountVectorizer(min_df=15000, max_df=35000)

    sprsDocMx = cv.fit_transform(doc)
    dimSprX = sprsDocMx.shape
    feqDocMx = tv.fit_transform(doc)
    trmDocMx = ncv.fit_transform(doc)

    # From hint
    # pass: vectorizer, matrix
    def matcherDispatcher(mx,v):
        
        for i, sent in enumerate(doc):
            if re.search(patUn, sent):
                break

        row = mx[i, :]
        terms = v.get_feature_names_out()
        _, col = row.nonzero()

        print("Original document: ", doc[i])
        print("""

        Words in matrix:
        ----------------""")
        for i in col:
            print(terms[i])

    # calculates dense matrix byte utilization based on matrix dimensions
    def dnsCalc(dims):
        row = dims[0]
        cols = dims[1]
        byteInCell = 8
        bites = row * cols * byteInCell

        return bites

    # Prints the top ten words based on summarized matrix, to single row
    def topTen(mx, v):
        wc = np.array(mx.sum(axis=0))[0]
        words = np.array(v.get_feature_names_out())
        sorted_indices = np.argsort(wc)[::-1][:10]
        top_words = words[sorted_indices]
        top_counts = wc[sorted_indices]
        return list(zip(top_words, top_counts))


    def signment():
        print('1. What are the dimensions of your matrix?')
        print('Rows by columns: ', dimSprX,'\n')

        print('2. How many bytes of memory are used to represent the matrix in sparse form?')
        print('Memory used by sparse matrix: ', sprsDocMx.data.nbytes, 'Bytes\n')

        print('3. How many bytes of memory would used to represent the matrix in dense form?')
        print('Memory used by dense matrix ', dnsCalc(dimSprX), 'Bytes\n')

        print('4. Which are the top 10 most frequent words? Are they meaningful, or should they be removed?')
        print('Printing listed sets of top words and their associated values: \n')

        print(topTen(sprsDocMx, cv),'\n')

        print(topTen(feqDocMx, tv),'\n')
        
        print('most all of these are not meaningful and should be removed except for maybe the last three\n')

        print('5. Experiment with the min_df, max_df arguments to CountVectorizer. Which values did you choose, and why?')
        print('Printing listed sets of top words with modified min_df and max_df arguements: \n')

        print(topTen(trmDocMx, ncv),'\n')
        
        print('''I chose my max at wround where the higher word count started to become relevant in my opinion.
              I chose the lower word count just to start seeing how much data I could shave off and what effects it had.
              Seems like certain words will still slip by the max/min arguements. I am not sure why.
              For example, in this case the word with appears to exceed the max_df limitation but still appears.\n''')

        print('6. Apply a regular expression to the descriptions to find ONE nonprofit that you find interesting.\nVerify that the bag of words approach does the correct operation on this particular description, both in the counts and the TF-IDF.\n')  
        matcherDispatcher(sprsDocMx,cv)
        print('\nFor TF-IDF matrix:')
        matcherDispatcher(feqDocMx,tv)

    signment()