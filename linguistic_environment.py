# -*- coding: UTF-8 -*-
# File to show surrounding environment of ipa characters
from flask import Flask
from flask import request
from flask import render_template
import io
import sys

app = Flask(__name__)


@app.route('/')
def form():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def form_post():
    character = request.form['letter']
    optLeft = request.form['optLeft']
    optAlone = request.form['optAlone']
    inputBox = request.form['inputBox']
    words = inputBox.split()
    # Spacing diacritics, non-spacing diacritics, and suprasegmentals
    # http://www.phon.ucl.ac.uk/home/wells/ipa-unicode.htm
    singleCharacters = [u'\u0325', u'\u030A', u'\u0324', u'\u032A', u'\u032C',
                        u'\u0330', u'\u033A', u'\u033C', u'\u033B', u'\u031A', u'\u0339', u'\u0303',
                        u'\u031C', u'\u031F', u'\u0320', u'\u0308', u'\u0334', u'\u026B', u'\u033D',
                        u'\u031D', u'\u0329', u'\u031E', u'\u032F', u'\u0318', u'\u0319', u'\u0306',
                        u'\u030B', u'\u0301', u'\u0304', u'\u0300', u'\u030F', u'\u035C', u'\u0361',
                        u'\u02C8', u'\u02CC', u'\u02D0', u'\u02D0', u'\u02D0', u'\u02B4', u'\u02B0',
                        u'\u02B1', u'\u02B2', u'\u02B7', u'\u02E0', u'\u02DE']
    if optLeft != "":
        for char in optLeft.split():
            singleCharacters.append([char, "left", "defined"])
    if optAlone != "":
        for char in optAlone.split():
            singleCharacters.append([char, "alone", "defined"])

    output = ""
    for j in range(len(words)):
        word = words[j]
        trueSeparation = []
        currentRealIndex = -1
        leftToRightIndex = 0
        while(leftToRightIndex < len(word)):
            nothingHappened = True
            for singleChar in singleCharacters:
                alone = False
                defined = False
                try:  # multicharacter (IE ~ thingy)
                    if len(singleChar) == 3:
                        defined = True
                        if (singleChar[1]) == "alone":
                            alone = True
                        index = word.index(singleChar[0], leftToRightIndex)
                    else:
                        index = word.index(singleChar, leftToRightIndex)
                    if index == leftToRightIndex:
                        nothingHappened = False
                        if defined:
                            if alone:
                                trueSeparation.append([singleChar[0]])
                                currentRealIndex += 1
                                leftToRightIndex += 2
                                break
                            else:
                                trueSeparation[currentRealIndex].append(singleChar[0])
                                leftToRightIndex += 1
                                break
                        else:
                            trueSeparation[currentRealIndex].append(word[leftToRightIndex])
                            leftToRightIndex += 1
                            break
                    else:
                        pass
                except ValueError:  # individual character (IE 'a')
                    pass
            if (nothingHappened):
                trueSeparation.append([word[leftToRightIndex]])
                currentRealIndex += 1
                leftToRightIndex += 1
        for i in range(len(trueSeparation)):
            characterSet = ''.join(trueSeparation[i])
            if characterSet == character:
                if i > 0:  # left environment is not word-beginning
                    left = ''.join(trueSeparation[i - 1])
                else:  # left environment is word beginning
                    left = '#'
                if i < len(trueSeparation) - 1:  # right environment is not word-end
                    right = ''.join(trueSeparation[i + 1])
                else:  # right environment is word end
                    right = '#'
                # save the environment of the desired character and write it to file
                environment = left + '_' + right
                output += (environment.encode('utf-8')) + "\n"
    return output
    # return render_template("index.html", upLetter=character, upOptLeft=optLeft, upOptAlone=optAlone, upInputBox=inputBox, upOutputBox=output)


if __name__ == "__main__":
    app.run()
