#########################################
#                                       #
#        Written by Chad MacLean        #
#         Current Version: 1.1.1        #
#                                       #
# ======== Contact Information ======== #
#   Email: billysprogrammer@gmail.com   #
#                                       #
#########################################

import random
import subprocess

class Generation:

    # Number of code groups in each message for the respective WPM.
    messageGroups = [[],[],[],[],[], [7, 6], [9, 9], [11, 11], [15, 15], [18, 17], [20, 19], [23, 22], [25, 25], [28, 27], [30, 30], [33, 33]]

    callsigns = ["XQ098", "KER21", "NRIO", "ZLQP", "NVB67", "OQP22", "FHHF", "QAPL", "ZRTU", "XQI44", "LQOM", "MMZ35",
                 "JKLP"]
    locations = ["LBSN", "FORD", "GENT", "BSEV", "BSIX", "ARMC", "GYMT", "FOOD", "MCDO", "TIMS", "MUSE", "MIRX", "DELA",
                 "RRDH", "STGS", "LSTR", "MRKT", "PENT"]
    qCodes = ["QTC", "QSA", "QTR", "QSL", "QSM", "QSV", "QTV", "QRV", "QRE", "QTH", "QTO", "QAL", "QAH", "QBD", "QRU"]

    # Usable characters only purpose is when optional arg withErrors is True, to only use these characters
    numbers = "1234567890"

    # Default values
    wordsPerMinute = 5
    morsetx = ""
    morserx = ""
    characterErrorRate = 1.1

    # Format values
    totalMessages = 0
    groupsPerMessage = 0

    # Output message and output file name
    fileName = ""
    message = ""

    # Optional arguments, TODO: Complete functions for all optional arguments
    withErrors = False
    numbersOnly = False
    lettersOnly = False
    messageStyle = 0

    # Set the words per minute
    def __setspeed__(self, wpm):
        self.wordsPerMinute = wpm

    # Randomly choose a receiver and transmitter from the callsigns and assign them.
    def setmorse_rxtx(self):
        morserx = random.choice(self.callsigns);
        morsetx = random.choice(self.callsigns);
        if morserx != morsetx:
            self.morserx = morserx
            self.morsetx = morsetx
        else:
            self.setmorse_rxtx(self)

    # Generate the message
    def generate_output(self):
        self.setmorse_rxtx(self)
        self.formatOutput(self)
        
        mrx = self.morserx
        mtx = self.morsetx
        totalMessages = str(self.totalMessages)
        groupsPerMessage = str(self.groupsPerMessage)
        
        wordblock = ""
        wordset = ""

        output = "SMX " + str(self.wordsPerMinute) + " WPM\n"

        mrx3x = mrx + " " + mrx + " " + mrx
        mtx2x = mtx + " " + mtx

        output += mrx3x + " DE " + mtx2x + " QTC 2 GA IMI K\n"
        output += mtx + " DE " + mrx + " OK GA K\n\n"

        output += mtx + " NR 01 GR " + str(self.messageGroups[self.wordsPerMinute][0]) + " 1300 BT\n"
        breakCounter = 0
        for i in range(self.messageGroups[self.wordsPerMinute][0]):
            sample = random.sample(self.numbers, 5)
            wordset = "".join(sample)
            wordblock += wordset + " "
            if breakCounter == 9:
                wordblock += "\n"
                breakCounter = 0
            else:
                breakCounter += 1
        output += wordblock + "AR\n\n"

        wordblock = ""
        wordset = ""
        output += mtx + " NR 02 GR " + str(self.messageGroups[self.wordsPerMinute][1]) + " 1300 BT\n"
        breakCounter = 0
        for i in range(self.messageGroups[self.wordsPerMinute][1]):
            sample = random.sample(self.numbers, 5)
            wordset = "".join(sample)
            wordblock += wordset + " "
            if breakCounter == 9:
                wordblock += "\n"
                breakCounter = 0
            else:
                breakCounter += 1
        output += wordblock + "SK\n\n"
        output += "END E E E E E"
        self.message = output
        
        if self.withErrors:
            self.generate_errors(self)

    def formatOutput(self, formatSelection = 0):
        totalCodeBlocks = self.messageGroups[self.wordsPerMinute][0] + self.messageGroups[self.wordsPerMinute][1]
        totalMessages = random.randint(1, 5)
        groupsPerMessage = round(totalCodeBlocks / totalMessages)
        codeBlockRemaining = totalCodeBlocks - (groupsPerMessage * totalMessages)

        self.totalMessages = totalMessages
        self.groupsPerMessage = groupsPerMessage

    # If withErrors is True, based off characterErrorRate, make mistakes in the message after it is created.
    def generate_errors(self):
        message = ""
        totalErrors = 0
        for i, c in enumerate(self.message):
            randNum = round(random.uniform(0, 100))
            randChar = random.choice(self.usableCharacters)
            if self.characterErrorRate > randNum:
                message += randChar
                totalErrors += 1
            else:
                message += c
            self.message = message

    # Create the text file for the morse, contents are the message previously generated.
    def output_to_file(self, count = 0):
        if count > 0:
            self.fileName = "morse" + str(self.wordsPerMinute) + "wpm_numbers" + str(count) + "0000"
            file = open(self.fileName + ".txt", "w+")
            file.write(self.message)
            file.close()
        else:
            self.fileName = "morse" + str(self.wordsPerMinute) + "wpm_numbers0000"
            file = open(self.fileName + ".txt", "w+")
            file.write(self.message)
            file.close()
    
    # Call ebook2cw which makes the morse audio based off the message in the text file
    def generate_morse_audio(self, count = 0):
        if count > 0:
            wpm = str(self.wordsPerMinute)
            args = 'ebook2cw.bat ' + wpm + " morse" + wpm + 'wpm_numbers' + str(count) + ' "morse' + wpm + 'wpm_numbers' + str(count) + '0000.txt"'
            subprocess.call(args)
        else:
            wpm = str(self.wordsPerMinute)
            args = 'ebook2cw.bat ' + wpm + " morse" + wpm + 'wpm_numbers "morse' + wpm + 'wpm_numbers0000.txt"'
            subprocess.call(args)

    # For ease of use, this function calls everything in the correct order to complete the generation.
    def do_all(self, wpmMin = 5, wpmMax = 5, errors = False, repeat = 0):
        if repeat > 0:
            for r in range(1, repeat+1):
                for w in range(wpmMin, wpmMax+1):
                    self.withErrors = errors
                    self.__setspeed__(self, w)
                    self.generate_output(self)
                    self.output_to_file(self, r)
                    self.generate_morse_audio(self, r)

