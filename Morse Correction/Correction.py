from tkinter import * 
from tkinter.filedialog import askopenfilename

from difflib import SequenceMatcher

# Hide the GUI
# tkinter.Tk().withdraw()

# ==================== TODO ==================== #
#                                                #
#   1. Check if lines are same length            #
#   2. Check for gaps in received using weights  # 
#      assuming that within the next few words   #
#      the user would be back on track           #
#   3. If we know a word was missed, subtract    #
#      from the score and move on to next index  #
#   4. Score each word, subtract only if the     #
#      word is not exactly the same              #
#                                                #
#   Hopefully with our weighting system it will  #
#   prevent us from marking everything else      #
#   completely wrong since the lists wont be     #
#   matching when using the same index poitner   #
#                                                #
# ============================================== #

class Correction:

    recText = []
    ansText = []

    testRec = ["You", "Yes", "you", "this", "my", "house", "number", "125", "514", "2222", "got", "it"]
    testAns = ["You", "Yes", "you", "Hey", "this", "my", "house", "number", "125", "514", "2222", "got", "it"]

    testIndex = 0

    # Open the file search system and store the location of the selected file
    def getFileData(self, context):
        fileData = []
        winTitle = "Select File"
        allowedFTypes = [("Text Files", "*.txt")]
        fPath = askopenfilename(initialdir = "./", title = winTitle, filetypes = allowedFTypes)
        try:
            with open(fPath) as fp:
                for line in fp:
                    if line != "\n":
                        fileData.append(line.strip())
                    else:
                        continue
        except IOError as e:
            print("No file selected." + str(e))
        if context == "Rec":
            self.recText = fileData.copy()
            fileData = []
        if context == "Ans":
            self.ansText = fileData.copy()
            print(len(self.ansText))
            fileData = []

    def evaluateText(self):
        maxScore = self.getMaxScore(self)
        print(maxScore)
        #maxValue =
        #for line in ansText
        # ratioValue = SequenceMatcher(None, self.recText, self.ansText).ratio()

    def getMaxScore(self):
        lineCount = 0
        for l in self.ansText:
            if lineCount < len(self.ansText):
                print(l)

    def getAndCompare(self):
        # Get value of current index
        self.testIndex = 3

        rec = self.testRec.copy()
        ans = self.testAns.copy()

        # Assign weights to the list forward and backwards for error testing based off current position
        recStrWeights = []
        ansStrWeights = []

        possibleWeights = [0.4, 0.6, 0.8, 1, 0.8, 0.6, 0.4]
        
        for bf in range(2):
            # Setup backward weights
            if bf == 0:
                for c in range(3):
                    pointer = self.testIndex - c
                    if pointer > 0 and pointer <= self.testIndex:
                        recStrWeights.append([rec[c], possibleWeights[c]])
                        ansStrWeights.append([ans[c], possibleWeights[c]])
            # Setup forward weights
            if bf == 1:
                for c in range(4):
                    pointer = self.testIndex + c
                    if pointer < len(rec):
                        recStrWeights.append([rec[self.testIndex + c], possibleWeights[c+self.testIndex]])
                        ansStrWeights.append([ans[self.testIndex + c], possibleWeights[c+self.testIndex]])
                        
        print("Received and Weights:")             
        print(recStrWeights)
        print("Answers and Weights:")
        print(ansStrWeights)

        # Check string match weights to make sure we arent off track
        results = []
        for w in range(6):
            results.append(self.compare(self, ans[w], rec[w]))
        print(results)

        # TODO: If we notice that the next few weights are completely off then we should
        #       assume that we are off track and something was missed.
            

    def compare(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return a - b
        elif isinstance(a, int) and isinstance(b, int):
            return a - b
        elif isinstance(a, str) and isinstance(b, str):
            return SequenceMatcher(None, a, b).ratio()
        else:
            print("Cannot compare two different data types")
        
            
            
        
        
