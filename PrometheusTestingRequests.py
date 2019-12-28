##Webscrapper
from googlesearch import search as ser

from bs4 import BeautifulSoup
import requests
import numpy as np
import os
from PIL import Image


def Str_to_Tokens (d):
    if isinstance(d,list):
        start = np.zeroes(len(d),300)
    for i in len(start):
        start[i] = glove[d[i]]
    else:
        return Str_to_Tokens(list(d))

class Prompter:
    def __init__(self):
        self.Country = input('Please enter your country name: ')
        self.Committe= input('Please enter the name of your committee: ')
        self.Topic = input('Please enter the topic: ')
        print( f"So, you are in the {self.Committe} as {self.Country} discussing {self.Topic}")
        self.Number_of_Questions = input("How many questions do you have for your background guide: ")
        self.Questions =[]
        self.FileName = self.Commitee + "_" + self.Country + "_" + self.Topic
        if self.Number_of_Questions.isnumeric() and self.Number_of_Questions>0:
            for i in range(self.Number_of_Questions):
                self.x = input('Enter your background guide questions with lines between each of them: ')
                self.Questions.append(self.x)
        else:
            print("You are not entering the correct boxes! ")
            #Quit
    #def __call__(self, *args, **kwargs):
        #for p in PuncRemover:

        #self.List =[self.Country.split(" ") + self.Committe.split(" ") + self.Topic.split(" ")] #Find a way to get rid of stop words
        #PuncRemover


Websites=[]





class Scrapper: #Only need the source part
    def __init__(self):
   
        self.source= set() #A set of all sources to be worked with
    
def comb (h):
    l = []
    for i in range(len(h*5)):
        for x in (h):
            l.append((x + " " + h[random.randint(len(h))]))
    l = set(l)
    l= list(l)
    assert isinstance(l, list)
    return l

def do():
    LII=False #constructor variable to see if the last item was an image# 
    print(f"LII is {LII} first")
    Test = Scrapper()
    query = "Autonomous Underwater Vehicle Battery" ##########################CHange Later
    dub=15
    dun=10
    while len(Test.source) <20: #number we want
        for h in ser(query, tld="co.in", num=dun, stop=dub, pause=2): #look up stop and tld
            if "wiki" in h or ".com" in h or ".net" in h: #Gets rid of .net and .com
                if "times" in h or "post" in h: #Will we keep this?
                    Test.source.add(h)
                continue
            else:
                try:
                    Test.source.add(h)
                except:
                    print("Print something might be missing ")
                    print("Error 1")
        dun*=2
        dub*=2

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    try:
        os.chdir(desktop)
    except:
        print("Error 2 with path change")

    if not os.path.exists("MUN"):
        os.mkdir("MUN", 0o0755)
        print("A new directory is on your Desktop called \'MUN\' your file is in there")
        os.chdir("MUN")
    else:
        os.chdir("MUN")
        print("Check the \'MUN\' folder for this")
        print(f"If the folder is not visible, find it with {os.getcwd()}")
    writtenText=""
    sourcesInOrder=[]
    with open("TestNumber1","w+", encoding = 'utf-8') as file: # Change this to country, and other stuff
        Source = list(Test.source) # sets are unscriptable
        
        ##########################Actual scrapper
        
        for h in range(len(Source)):
            fullPageContent = requests.get(Source[h])
            if fullPageContent.status_code!=200:
                print ("Error Number 3 with page access")
                print ("Your program will run but the following source will not be in the document")
                print("\n")
                print (f"{Source[h]}")
                continue
            try:
                if "html" in Source[h]:
                    soup = BeautifulSoup(fullPageContent.content,'html.parser')
                else:
                    soup = BeautifulSoup(fullPageContent.content,'lxml')
                soup.prettify()
                file.write(f"Source #{h+1}: {Source[h]} \n")
                
                for tag in ["p","img"]:#Useful tags
                    for paragraphs in soup.find_all(tag):
                        paragraphs.name="Useful"
                for x in soup.find_all('Useful'):
                    print(x)
                    if x.get_text == None:
                        print ("Error Number 4 with HTML parsing")
                        print ("Your program will run but the following source will not be in the document")
                        print ("\n")
                        print (f"{Source[h]}")
                        continue
                    if x["src"]is not None :
                        try:
                            Img =Image.open(x["src"]);
                            file.write(Img)#image
                            file.write()#caption
                            if LII == False:
                                LII = True
                            print(f"LII is {LII} second")
                            continue
                        except Exception as ex:
                            print("Error Number 5 with what seemed to be an image but isn't actually, my b")
                            print(ex)
                    if LII==True and x["caption"]!=None:
                        print(f"LII is {LII} third")
                        file.write("\n")
                        file.write(x["caption"])
                        file.write("\n")
                    LII = False
                    print(f"LII is {LII} fourth")
                    file.write(x.get_text())
                    writtenText+=x.get_text()
                    sourcesInOrder.append(Source[h])
                writtenText+=" "
                file.write("\n")
                file.write(f"End of Source: #{h+1} \n\n")
                print(f"{h} is done")
            except Exception as ex:
                print(f"Source {Source[h]} is messing up with \n{ex}")
    
    return writtenText, sourcesInOrder


##