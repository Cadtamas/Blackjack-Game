# -*-coding:utf-8;-*-
#################################
#       BLACK JACK GAME         #
#################################

from tkinter import*
from random import randrange


class MenuBar(Frame):
    """Drop-down menu"""
    def __init__(self,boss=None):
        Frame.__init__(self,borderwidth=2,relief=GROOVE)

        #### <FILE> menü ####
        fileMenu=Menubutton(self,text='Game')
        fileMenu.pack(side=LEFT,padx=5)
        me1=Menu(fileMenu)
        me1.add_command(label='Restart',underline=0,command=boss.reset)
        me1.add_command(label='End',underline=0,command=boss.quit)
        fileMenu.configure(menu=me1)

class ControlPanel(Frame):
    """Control panels"""
    def __init__(self,boss,player="Player 1"):
        Frame.__init__(self)
        self.player=player
        self.appli=boss
        self.money=1500
        self.mlab=Label(self,text="Cash: 1500 $")
        self.mlab.pack()
        self.bet=IntVar()
        Label(self,text="Bet:")
        self.e=Entry(self,textvariable=self.bet,width=10)
        self.e.pack(side=TOP)
        self.bet.set("300")
        self.chk=IntVar()           #Tkinter object variable for the checkbutton
        self.chkB=Checkbutton(self,text=self.player.id,variable=self.chk,command=self.enablePlayer)
        self.chkB.pack(side=TOP)

        #Game buttons:
        self.b1=Button(self,text="Double",state=DISABLED,command=self.doub )
        self.b1.pack(side=LEFT,padx=5,pady=5)
        self.b2=Button(self,text="Hit",state=DISABLED,command=self.hi )
        self.b2.pack(side=LEFT,padx=5,pady=5)
        self.b3=Button(self,text="Stand",state=DISABLED,command=self.stan )
        self.b3.pack(side=LEFT,padx=5,pady=5)
        self.pack(padx=5,pady=5,side=LEFT)

    def enablePlayer(self):
        "Change the player's status"
        if self.player.boss.master.gamestate==0:
            v=self.chk.get()
            #self.b2.configure(state=[DISABLED,NORMAL] [v])
            self.player.boss.master.startB.configure(state=[DISABLED,NORMAL] [v]) #Change the start button state, if it's Disabled
            if self.player.status==0:
                self.player.status=1
            else:
                self.player.status=0

    def doub(self):
        "Call the master's <double> method "
        self.player.boss.master.double()

    def hi(self):
        "Call the master's <hit> method "
        self.player.boss.master.hit(self.player.id)

    def stan(self):
        "Call the master's <stand> method "
        self.player.boss.master.stand(self.player.id)

    def setBank(self,p):
        "Change the player's bank account"
        self.money+=p
        self.mlab.config(text='Cash: %s $' % self.money)

class Player():
    """Player datas"""
    def __init__(self,boss,id,x,y):
        self.boss=boss                  #canvas identification
        self.appli=boss.master          #The application's reference
        self.id=id                      #player id
        self.x,self.y=x,y               #player's place on the canvas
        self.status=0                   #if player's status is 0, the player is inactive
        self.score=0                    #the player's current score
        self.cards=[]                   #current cards in hand
        self.cpics={}                   #the cards pictures
        self.message="%s set the bet, and press <Start>" %(self.id)

class BlackJack(Frame):
    """The main program"""
    def __init__(self):
        Frame.__init__(self)
        self.master.title("<<<<<<< BLACK JACK >>>>>>>") #Title in the top of the window
        self.initGame()

    def initGame(self):
        "The first things to do"
        #Menu
        self.mbar=MenuBar(self)     #place the menubar
        self.mbar.pack(side=TOP,expand=NO,fill=X)

        #Canvas
        self.game=Canvas(self,width=900,height=600,bg='forest green',bd=3,relief=SUNKEN)
        self.game.pack(padx=8,pady=8,side=TOP,expand=YES,fill=BOTH)

        self.game.create_line(0,300,920,300,width=3,fill="yellow")
        self.game.create_line(150,300,150,610,width=3,fill="yellow")
        self.game.create_line(300,300,300,610,width=3,fill="yellow")
        self.game.create_line(450,300,450,610,width=3,fill="yellow")
        self.game.create_line(600,300,600,610,width=3,fill="yellow")
        self.game.create_line(750,300,750,610,width=3,fill="yellow")
        self.pack()

        #Players :
        playerlist=["Player 1","Player 2","Player 3","Player 4","Player 5","Player 6"]  #The player's list
        self.players={} #The player's dictionary
        playerpos=[[75,500],[225,500],[375,500],[525,500],[675,500],[825,500]]
        n=0
        for name in  playerlist:
            self.players[name]=Player(self.game,playerlist[n],playerpos[n][0],playerpos[n][1])
            n+=1
        self.dealer=Player(self.game,"Dealer",450,200)
        self.dealer.status=1

        #Control panels :
        self.panel={}    #The control panel's dictionary
        for name in playerlist:
            self.panel[name]=ControlPanel(self,self.players[name])
            self.panel[name].configure(bd=5,relief=GROOVE)

        #Start button :
        self.startB=Button(self,text="START",state=DISABLED,command=self.start)
        self.startB.pack()

        #Texts:
        self.messages={}
        self.score_p={}
        for name in playerlist:
            self.messages[name]=self.game.create_text(self.players[name].x,self.players[name].y-100,
                                                      text=self.players[name].message,
                                                      font=('Times',15,'bold'),fill='yellow',width=145,justify=CENTER)
            self.score_p[name]=self.game.create_text(self.players[name].x,self.players[name].y+100,
                                                      text="Points: %s " %(self.players[name].score),
                                                      font=('Arial',10,'bold'),fill='White',width=145)
        self.dealer_message=self.game.create_text(450,100, text="Ready" , font=('Times',20,'bold'),fill='Red',justify=CENTER)
        self.dealer_score_p=self.game.create_text(450,250, text="Points: %s " %(self.dealer.score) , font=('Arial',10,'bold'),fill='White')

        #The cards deck :
        self.colors=["spades","hearts","diamonds","clubs"]
        self.val=[['2',2,2],['3',3,3],['4',4,4],['5',5,5],['6',6,6],['7',7,7],['8',8,8],['9',9,9],['10',10,10],["jack",10,10],["queen",10,10],["king",10,10],["ace",11,1]]
        #[Cards's name, high value, low value] ---Check the score method for more information.
        self.deck=[]
        for c in self.colors:
            for v,v1,v2 in self.val:
                self.deck.append([c,v,v1,v2])
        self.cardlist=[]        #The current cards
        self.gamestate=0        #Initial state

    def start(self):
        "The initial steps, two cards for every active players, and one for the dealer"
        if self.checkBet(): #Checking the bet for incorrect input or negative bet or too high bet
            #player's turn:
            self.gamestate=1        #First state
            self.cardlist=[]        #Clear the cardlist
            self.showcards(self.dealer.id)  #Clear the dealer's canvas
            for name in self.players:
                self.showcards(name)        #Clear the player's canvas
                if self.players[name].status==1:
                    n=self.shuffle()                                        #get a card
                    self.players[name].cards.append(self.deck[n])           #put it in the player's hand
                    self.score(self.players[name].cards,self.players[name]) #score
                    self.panel[name].money-=self.panel[name].bet.get()      #deduct the amount of the bet
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money)) #Change the label
                    self.panel[name].e.configure(state=DISABLED)            #disable the entry field
                else:   #the inactive players:
                    self.game.itemconfig(self.messages[name],text="%s set the bet, and press <Start>" %(name),font=('Times',15,'bold'),fill='yellow',width=145) #get this message
                    self.game.itemconfig(self.score_p[name],text="Points: 0" )  #and set their score points to 0

            #dealer's turn:
            n= self.shuffle()                           #get a card
            self.dealer.cards.append(self.deck[n])      #put it in the dealer's hand
            self.score(self.dealer.cards,self.dealer)   #calculate the score

            #again the players:
            for name in self.players:
                if self.players[name].status==1:            #The active players only
                    n=self.shuffle()                        #The second card...
                    self.players[name].cards.append(self.deck[n])
                    self.score(self.players[name].cards,self.players[name]) #calculate the score
                    if self.players[name].score==21:        #In case of BLACKJACK...
                        self.stand(name)                    #...press the stand button automatically
                        self.game.itemconfig(self.score_p[name],text='BLACK JACK')      #...change the score point to <BLACK JACK> label
                    else:
                        self.panel[name].b2.configure(state=NORMAL) #Activate the Hit button
                        self.panel[name].b3.configure(state=NORMAL) #Activate the Start button
            self.startB.configure(state=DISABLED)   #Disable the Start button
        else:
            self.nextround()   #If someone sets an invalid bet, a new round will begin until it will be changed to the right value.

    def shuffle(self):
        "Returns a card's index that doesn't contained the actual cardlist"
        while 1:
            n=randrange(0,51)   #get a random number
            if n not in self.cardlist :     #if its not in the actual cardlist:
                self.cardlist.append(n)     #...put it in the cardlist
                break                       #break the while loop
        return n                            #and return with the card's index

    def score(self, cardlist, player):
        "Calculate the <player>'s score based on the <cardlist>"
        x=0                             #the card's high value
        y=0                             #the card's low valus (actually the ace's has two values)
        for card in cardlist:           #iterate the cardlist
            x+=card[2]
            y+=card[3]
            if x>21:                    #I have created a simplified method to decide the ace's value. (11 or 1)...
                player.score=y          #...if the score more than 21, all cards get the low values. (I would like to improve this method later.)
            else:
                player.score=x
        self.showcards(player.id)       #Put the cards picture to the canvas
        #Change the score points in the canvas:
        if player==self.dealer:
            self.game.itemconfig(self.dealer_score_p,text="Points: %s " %(player.score))
        else:
            self.game.itemconfig(self.score_p[player.id],text="Points: %s " %(player.score))
        if player.score>21 and player!=self.dealer:
            self.stand(player.id)       #If the player score is more than 21 the stand button will be pressed

    def showcards(self,name):
        "Place the card gifs to the canvas"
        self.after(100)         #wait a little bit.
        v=''                    #this will be the label that shows the card's names
        if name=="Dealer":
            x=self.dealer.x-30              # x position from the player class
            y=self.dealer.y                 # y postiton from the player class
            for c in self.dealer.cards:
                v=v+c[0]+' '+c[1]+'\n'
                w='cards/'+c[1]+'_of_'+c[0]+'.gif'              #the card's gif name
                self.dealer.cpics[w]=PhotoImage(file=w)
                self.game.create_image(x,y,image=self.dealer.cpics[w])
                x+=10                                                   #slide every card in a little bit
            self.game.itemconfig(self.dealer_message,text=v,font=('Times',10,'bold'),fill='blue')   #change the label

        else:
            if self.players[name].status==1:        #the active players
                x=self.players[name].x-30           #get the x,y coordinates from the player class
                y=self.players[name].y
                for c in self.players[name].cards:
                    v=v+c[0]+' '+c[1]+'\n'
                    w='cards/'+c[1]+'_of_'+c[0]+'.gif'
                    self.players[name].cpics[w]=PhotoImage(file=w)
                    self.game.create_image(x,y,image=self.players[name].cpics[w])
                    x+=10
                self.game.itemconfig(self.messages[name],text=v,font=('Times',10,'bold'),fill='blue')

    def hit(self,name):
        "Get a new card"
        n=self.shuffle()
        self.players[name].cards.append(self.deck[n])
        self.score(self.players[name].cards,self.players[name])

    def stand(self,name):
        "Close the players turn and jump to the next player"
        self.panel[name].b2.configure(state=DISABLED) #Disable the Hit button
        self.panel[name].b3.configure(state=DISABLED) #Disable the Hold button
        self.players[name].status=2                   #Change the player's status
        status_Chk=[]
        for tag in self.players:
            status_Chk.append(self.players[tag].status)
        if 1 not in status_Chk:                 #if all active players hit the stand button or busted...
            while self.dealer.score<17:         #...the dealer's turn comes
                n= self.shuffle()
                self.dealer.cards.append(self.deck[n])
                self.score(self.dealer.cards,self.dealer)
            self.wincheck()                     #check who's win
            self.nextround()                    #next turn begins

    def wincheck(self):
        "Compare the scores"
        for name in self.players:
            if self.players[name].score>21:     #if the player has more than 21 points, the dealer won
                break
            elif self.dealer.score>21:          #if the player has less or egal 21 points and the dealer has more than 21 points:
                if self.players[name].score==21 and len(self.players[name].cards)==2:                #Blackjack
                    self.panel[name].setBank(2.5*self.panel[name].bet.get())                         #Get the money
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))     #show the new amount
                elif self.players[name].score<=21:                                                   #win
                    self.panel[name].setBank(2*self.panel[name].bet.get())                           #Get the money
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))     #show the new amount
            else:                               #if the dealer and the player has less or egal 21 points:
                if self.players[name].score==21 and len(self.players[name].cards)==2:                #Blackjack
                    self.panel[name].setBank(2.5*self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
                elif self.players[name].score<=21 and self.players[name].score>self.dealer.score:    #win
                    self.panel[name].setBank(2*self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
                elif self.players[name].score<=21 and self.players[name].score==self.dealer.score:    #draw
                    self.panel[name].setBank(self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
        #If the player has lost, nothing happens, the amount of money has been already substracted

    def nextround(self):
        "Initialize the next round"
        for name in self.panel:                         #Every players...
            self.panel[name].e.configure(state=NORMAL)  #activate the entry field
            if self.players[name].status==2:            #set the status back to 1
                self.players[name].status=1
            self.players[name].cards=[]                 #clear the player's cardlist
            self.players[name].cpics={}                 #clear the player's picture dictionary
            self.players[name].score=0                  #set the score to 0
            if self.panel[name].money==0:               #If the player has ran out of money:
                self.game.itemconfig(self.messages[name],text="%s, GAME OVER" %(name),font=('Times',15,'bold'),fill='yellow',width=145)     #Give a nice message
                self.players[name].status=0             #set the status to inactive
                self.panel[name].chkB.configure(state=DISABLED)     #disable the check button
        self.startB.configure(state=NORMAL) #Activate the Start button
        self.dealer.score=0               #Clear the dealer's datas...
        self.dealer.cards=[]
        self.dealer.cpics={}
        self.gamestate=0

    def checkBet(self):
        "Check the entry field for invalid bets if everything okay it will return an <1>, else an <0> until every fields get valid values"
        for name in self.panel:
            if self.players[name].status==1:    #Only for the active players
                try:
                    bet=self.panel[name].bet.get()
                    if bet>self.panel[name].money or bet<=0: # if the bet is more then the player's money
                        self.game.itemconfig(self.messages[name],text="%s, the bet must be an integer between 1 and %s" %(name,self.panel[name].money),font=('Times',15,'bold'),fill='yellow',width=145)
                        return 0

                except:                          #if the field get a non-integer value:
                    self.game.itemconfig(self.messages[name],text="%s, the bet must be an integer between 1 and %s" %(name,self.panel[name].money),font=('Times',15,'bold'),fill='yellow',width=145)
                    return 0
        return 1

    def double(self):
        pass

    def reset(self):
        "Reset the game"
        #If you know, how can I delete the players and the control panel objects from the dictionary, please let me know. :)
        for name in self.panel:
            self.panel[name].e.configure(state=NORMAL)
            self.players[name].status=0
            self.players[name].cards=[]
            self.players[name].score=0
            self.panel[name].money=1500
            self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
            self.game.itemconfig(self.messages[name],text="%s set the bet, and press <Start>" %(name),font=('Times',20,'bold'),fill='yellow',width=145)
            self.game.itemconfig(self.score_p[name],text="Points: 0 ")
            self.panel[name].chkB.deselect()
            self.panel[name].chkB.configure(state=NORMAL)
        self.dealer.score=0
        self.dealer.cards=[]
        self.game.itemconfig(self.dealer_message,text="Ready" , font=('Times',20,'bold'),fill='Red')
        self.game.itemconfig(self.dealer_score_p,text="Points: 0 " , font=('Arial',10,'bold'),fill='White')
        self.gamestate=0

if __name__=='__main__':
    BlackJack().mainloop()




__author__ = 'Cadtamas'
