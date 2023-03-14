# A Markov Chain Text Generator, trained on an input file
#
# MIT License
#
# Copyright (c) 2023 Rory L.P. McGuire
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import random
import sys

class MarkovModel:
    """A Markov Chain Model trained on input text"""

    class Datum:
        """A single datum for the model"""

        def __init__(self):
            self.dict = {}

        def __repr__(self):
            return f"{self.dict}"

        def add(self, theChar):
            v = 0
            if theChar in self.dict:
                v = self.dict[theChar]
            v = v+1
            self.dict[theChar] = v

        def getRandomNextChar(self):
            return random.choices(list(self.dict.keys()), weights=list(self.dict.values()))[0]

    def __init__(self, baseNum):
        self.baseNum = baseNum
        self.accumulatedData = {}

    def __repr__(self):
        return f"{self.__doc__}\nbaseNum: {self.baseNum}\naccumulatedData: {self.accumulatedData}"

    def processMoreData(self, data):
        # returns anny unused data (just fewer than self.baseNum characters)
        while len(data) > self.baseNum:
            key = data[0:self.baseNum]
            if key in self.accumulatedData:
                datum = self.accumulatedData[key]
                datum.add(data[self.baseNum])
            else:
                datum = self.Datum()
                datum.add(data[self.baseNum])
                self.accumulatedData[key] = datum
            data = data[1:]
        return data

    def randomKey(self):
        index = random.randrange(len(self.accumulatedData))
        iterator = iter(self.accumulatedData.keys())
        which = next(iterator)
        while index > 0:
            which = next(iterator)
            index = index - 1
        return which

    def outputStartingWith(self, start, totalChars):
        if len(start) != self.baseNum:
            print(f"Error: length of prompt should be {self.baseNum}")
            return
        current = start
        print(start, end='')
        totalChars = totalChars - self.baseNum
        while current in self.accumulatedData and totalChars > 0:
            datum = self.accumulatedData[current]
            nextChar = datum.getRandomNextChar()
            print(nextChar, end='')
            totalChars = totalChars - 1
            current = current[1:] + nextChar
        print("")

def maybeStatusPrint(which, howOften):
    if which % howOften != 0:
        return
    pickChar = int(which / howOften) % 4
    if pickChar == 0:
        print('\\\r', end='')
    elif pickChar == 1:
        print('|\r', end='')
    elif pickChar == 2:
        print('/\r', end='')
    else:
        print('-\r', end='')

parser = argparse.ArgumentParser(
           prog='markov-chain-text',
           description='Create a Markov Chain Generator from a given text file and prompt to generate some text')
parser.add_argument('filename', help="input filename")
parser.add_argument('-c', '--count', type=int, default="4", help="base count of chars for chain")
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

mm = MarkovModel(args.count)
print("Parsing input file into model...")
with open(args.filename) as f:
    remaining = ""
    status=0
    for line in f:
        remaining = mm.processMoreData(remaining + line)
        status = status + 1
        maybeStatusPrint(status, 1000)

if args.debug:
    print(mm)

print("Parsing complete.")

print("Enter number of characters to output.")
for line in sys.stdin:
    if line is '\n':
        break
    mm.outputStartingWith(mm.randomKey(), int(line))
