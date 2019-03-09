#########################################
#                                       #
#        Written by Chad MacLean        #
#         Current Version: 1.1          #
#                                       #
# ======== Contact Information ======== #
#   Email: billysprogrammer@gmail.com   #
#                                       #
#########################################

import random
import subprocess
import datetime

class Generation:

    # Number of code groups in each message for the respective WPM.
    messageGroups = [[],[],[],[],[], [8, 8], [12, 11], [15, 15], [19, 19], [20, 20], [25, 23]]

    callsigns = ["XQ098", "KER21", "NRIO", "ZLQP", "NVB67", "OQP22", "FHHF", "QAPL", "ZRTU", "XQI44", "LQOM", "MMZ35",
                 "JKLP"]
    locations = ["LBSN", "FORD", "GENT", "BSEV", "BSIX", "ARMC", "GYMT", "FOOD", "MCDO", "TIMS", "MUSE", "MIRX", "DELA",
                 "RRDH", "STGS", "LSTR", "MRKT", "PENT"]
    qCodes = ["QTC", "QSA", "QTR", "QSL", "QSM", "QSV", "QTV", "QRV", "QRE", "QTH", "QTO", "QAL", "QAH", "QBD", "QRU"]

    # Usable characters only purpose is when optional arg withErrors is True, to only use these characters
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZäéöü"
    numbers = "1234567890"
    usableCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZäéöü1234567890"

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

    # Gets the current time for the transmitted message
    def getTime(self):
        currentHour = datetime.datetime.now().hour
        currentMinutes = datetime.datetime.now().minute

        if currentMinutes < 10:
            currentMinutes = "0" + str(currentMinutes)

        currentTime = str(currentHour) + str(currentMinutes)
        return currentTime

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
        groupsPerMessage = self.groupsPerMessage
        
        wordblock = ""
        wordset = ""

        # Beginning of creating the output for the text file
        output = "SMX " + str(self.wordsPerMinute) + " WPM\n\n"

        output += mrx + " DE " + mtx + " QTC " + totalMessages + " GA IMI K\n"
        output += mtx + " DE " + mrx + " OK GA K\n\n"

        # TODO: Make a way to generate a specific format based off the argument passed to the generation function

        messageCounter = 1
        currentMessage = "01"

        messageDict = [self.letters, self.numbers]
        
        for m in range(self.totalMessages):
            charOrNum = random.randint(0, 10)
            messageSample = messageDict[1] if charOrNum >= 5 else messageDict[0]

            if messageCounter < 10:
                currentMessage = "0" + str(messageCounter)
            
            output += mtx + " NR " + currentMessage + " GR " + str(groupsPerMessage) + " " + self.getTime(self) + " BT\n"
            
            for g in range(groupsPerMessage):
                sample = random.sample(messageSample, 5)
                wordset = "".join(sample)
                wordblock += wordset + " "
            if messageCounter < self.totalMessages:
                output += wordblock + "AR\n"
                worset = ""
                wordblock = ""
                messageCounter += 1
            else:
                output += wordblock + "SK\n\n"
                
        output += "END E E E E E"
        self.message = output
        # Unless the error argument has been made true, this is the end of the output generation
        
        if self.withErrors:
            self.generate_errors(self)

    def formatOutput(self, formatSelection = 0):
        totalCodeBlocks = self.messageGroups[self.wordsPerMinute][0] + self.messageGroups[self.wordsPerMinute][1]
        totalMessages = random.randint(1, 5)
        groupsPerMessage = round(totalCodeBlocks / totalMessages)
        codeBlockRemaining = totalCodeBlocks - (groupsPerMessage * totalMessages)

        self.totalMessages = totalMessages
        self.groupsPerMessage = groupsPerMessage-totalMessages if totalMessages > 2 else (groupsPerMessage + round(groupsPerMessage*.3))
        

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
    def output_to_file(self):
        self.fileName = "morse" + str(self.wordsPerMinute) + "wpm"
        file = open(self.fileName + ".txt", "w+")
        file.write(self.message)
        file.close()

    # Call ebook2cw which makes the morse audio based off the message in the text file
    def generate_morse_audio(self):
        wpm = str(self.wordsPerMinute)
        args = 'ebook2cw.bat ' + wpm + " morse" + wpm + 'wpm "morse' + wpm + 'wpm.txt"'
        subprocess.call(args)

    # For ease of use, this function calls everything in the correct order to complete the generation.
    def do_all(self, wpm, errors = False):
        self.withErrors = errors
        self.__setspeed__(self, wpm)
        self.generate_output(self)
        self.output_to_file(self)
        self.generate_morse_audio(self)

