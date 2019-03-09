Thank you for checking out my Morse File Generator Version 1. I will give out credit where is due at the bottom of this file.

This program was created in Python version 3.7.2 and should be run alongside the IDLE shell, as it was the only way this was tested. if you are more experienced
and know how to run this program elsewhere and create the same result expected, feel free to do so.

This is very easy to use, open Generation.py with IDLE and run the script. The shell will open and you can use the following command to generate your morse files.

Generation.do_all(Generation, WPM, ERRORS)

The only two things you can change are WPM and ERRORS. The following values are valid:

WPM: 5-10
ERRORS: True/False

It is pretty self explanitory, but I will provide an example.

Generation.do_all(Generation, 7, False)

This will generate a text document answer sheet and the accompanied morse audio file with a very easily understood file name. In this case they would as follows:

morse7wpm.txt
morse7wpm0000.mp3

The text document is the answer key, the mp3 is the audio file to transcribe.

========== CREDITS ==========

Myself, Chad MacLean (chad.maclean@forces.gc.ca), for creating the python script.

Fabian Kurz, for creating LCWO.net and the ebook2cw program included in this folder. Without them, I could not generate the morse audio based off the text file.
https://lcwo.net/
http://fkurz.net/ham/ebook2cw.html

========== LICENSE ==========

This python script is free to be modified, no credit is necessary to be given since it is too basic for me to care. This was just a fun project of mine while
I was learning morse code. Feel free to make it better!

However, please follow the license for the ebook2cw program as indicated on Fabian's website. 

Enjoy!