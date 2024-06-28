import re

class Texts:
    @staticmethod
    def get_about_text():
        return Texts.remove_spaces('''this application is created for all type of text editing. this application is created
            as a project for learning the python programming because no one can master anything. this application
            is created in python programming language or written in python. the application uses the back-end
            as python programming and front-end or GUI is made with PyQt5 a python gui library. the application
            uses many icons some of them are built by me and other are built by p.yusukekamiyamane.com , flaticons ''').title()


    @staticmethod
    def get_developers_text():
        return Texts.remove_spaces('''
            this application is written in python by a single / indie developer me jawad.i wrote this application 
            in 3 days or simply working everyday 3 to 4 hours.it is an open source application and can be used by anyone
            except those who want to use it for malicious purposes . it might have some bugs or any other errors. i do my best
            to update this application in every 5 months. and for any other enquiries contact at janonymous9899@gmail.com.
            from palandri , district sudhnoti , AJK - Pakistan
            ''').title()

      

    @staticmethod
    def about_myself():
        return Texts.remove_spaces('''
            myself jawad , a teenager studying in class 10th as well as i am struggling to become a full stack developer and a programmer who
            loves to program in all languages. i am not considering myself as a programmer or a full stack developer
            i can say that i have learned things at Intermediate level but i know which things are advanced or not.
            i have used the computer about 5 years having a coding experience of a 1.5 years. i haven't learned anything
            from school or college or from any other source related to programming and no one taught me execpt some people . they don't taught me how to memorize the code
            or learn by heart rather they taught me in this way that i don't need to memorize anything. about my coding:
            credit goes to [--- Haris Ali Khan, Vishwajeet Kumar, Shardha Khapra And Vinod Bahadur Thapa ---] they taught me
            how to code as well as i am also learning graphic designing . Thanks To --- Imran Ali Dina --- Who Taught Me How To Design
            Something... To Be Continued :)

            ''').title()
    @staticmethod
    def remove_spaces(text):
        xtraSpacesRemovedText = ""
        pattern_to_get_character = re.compile(r"([a-zA-Z0-9-@/\:\.]+)")
        matches = pattern_to_get_character.finditer(text)
        for match in matches:
            xtraSpacesRemovedText += match.group(1) + " "
        return xtraSpacesRemovedText