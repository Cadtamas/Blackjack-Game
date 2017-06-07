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
        self.b4=Button(self,text="Surrender",state=DISABLED,command=self.sur )
        self.b4.pack(side=LEFT,padx=5,pady=5)
        self.pack(padx=5,pady=5,side=LEFT)

    def enablePlayer(self):
        if self.player.boss.master.gamestate==0:
            v=self.chk.get()
            #self.b2.configure(state=[DISABLED,NORMAL] [v])
            self.player.boss.master.startB.configure(state=[DISABLED,NORMAL] [v]) #Change the start button state, if it's Disabled
            if self.player.status==0:
                self.player.status=1
            else:
                self.player.status=0

    def doub(self):
        self.player.boss.master.double()

    def hi(self):
        self.player.boss.master.hit(self.player.id)

    def stan(self):
        self.player.boss.master.stand(self.player.id)

    def sur(self):
        self.player.boss.master.surrender()

    def setBank(self,p):
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
        self.master.title("<<<<<<< BLACK JACK >>>>>>>")
        self.initGame()

    def initGame(self):
        #Menu
        self.mbar=MenuBar(self)
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
        self.players={}
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

        self.deck=[]
        for c in self.colors:
            for v,v1,v2 in self.val:
                self.deck.append([c,v,v1,v2])
        self.cardlist=[]        #The current cards
        self.gamestate=0

    def start(self):
        "The initial steps"
        if self.checkBet():
            #player's turn:
            self.gamestate=1
            self.cardlist=[]
            self.showcards(self.dealer.id)
            for name in self.players:
                self.showcards(name)
                if self.players[name].status==1:
                    n=self.shuffle()            #get a card
                    self.players[name].cards.append(self.deck[n])
                    self.score(self.players[name].cards,self.players[name]) #score
                    self.panel[name].money-=self.panel[name].bet.get()      #We deduct the amount of the bet
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money)) #Change the label
                    self.panel[name].e.configure(state=DISABLED)
                else:
                    self.game.itemconfig(self.messages[name],text="%s set the bet, and press <Start>" %(name),font=('Times',15,'bold'),fill='yellow',width=145)
                    self.game.itemconfig(self.score_p[name],text="Points: 0" )

            #dealer's turn:
            n= self.shuffle()
            self.dealer.cards.append(self.deck[n])
            self.score(self.dealer.cards,self.dealer)

            #again the players:
            for name in self.players:
                if self.players[name].status==1:            #The active players only
                    n=self.shuffle()
                    self.players[name].cards.append(self.deck[n])
                    self.score(self.players[name].cards,self.players[name])
                    if self.players[name].score==21:        #In case of BLACKJACK
                        self.stand(name)
                        self.game.itemconfig(self.score_p[name],text='BLACK JACK')
                    else:
                        self.panel[name].b2.configure(state=NORMAL) #Hit button
                        self.panel[name].b3.configure(state=NORMAL) #Start button
            self.startB.configure(state=DISABLED)
        else:
            self.nextround()

    def shuffle(self):
        while 1:
            n=randrange(0,51)
            if n not in self.cardlist :
                self.cardlist.append(n)
                break
        return n

    def score(self, cardlist, player):
        x=0
        y=0
        for card in cardlist:
            x+=card[2]
            y+=card[3]
            if x>21:
                player.score=y
            else:
                player.score=x
        self.showcards(player.id)
        if player==self.dealer:                                     #We have to change score texts
            self.game.itemconfig(self.dealer_score_p,text="Points: %s " %(player.score))
        else:
            self.game.itemconfig(self.score_p[player.id],text="Points: %s " %(player.score))
        if player.score>21 and player!=self.dealer:
            #self.panel[player.id].stan()
            self.stand(player.id)


    def showcards(self,name):
        self.after(100)
        v=''
        if name=="Dealer":
            x=self.dealer.x-30
            y=self.dealer.y
            for c in self.dealer.cards:
                v=v+c[0]+' '+c[1]+'\n'
                w='cards/'+c[1]+'_of_'+c[0]+'.gif'
                self.dealer.cpics[w]=PhotoImage(file=w)
                self.game.create_image(x,y,image=self.dealer.cpics[w])
                x+=10
            self.game.itemconfig(self.dealer_message,text=v,font=('Times',10,'bold'),fill='blue')

        else:
            if self.players[name].status==1:
                x=self.players[name].x-30
                y=self.players[name].y
                for c in self.players[name].cards:
                    v=v+c[0]+' '+c[1]+'\n'
                    w='cards/'+c[1]+'_of_'+c[0]+'.gif'
                    self.players[name].cpics[w]=PhotoImage(file=w)
                    self.game.create_image(x,y,image=self.players[name].cpics[w])
                    #self.card_images.append(self.game.create_image(x,y,image=PhotoImage(file=w)))
                    x+=10
                self.game.itemconfig(self.messages[name],text=v,font=('Times',10,'bold'),fill='blue')

    def hit(self,name):
        n=self.shuffle()
        self.players[name].cards.append(self.deck[n])
        self.score(self.players[name].cards,self.players[name])

    def stand(self,name):
        self.panel[name].b2.configure(state=DISABLED) #Hit button
        self.panel[name].b3.configure(state=DISABLED) #Start button
        self.players[name].status=2
        status_Chk=[]
        for tag in self.players:
            status_Chk.append(self.players[tag].status)
        if 1 not in status_Chk:                 #if all active players hit the stand button or busted...
            while self.dealer.score<17:
                n= self.shuffle()
                self.dealer.cards.append(self.deck[n])
                self.score(self.dealer.cards,self.dealer)
            self.wincheck()
            self.nextround()

    def wincheck(self):
        for name in self.players:
            if self.players[name].score>21:
                break
            elif self.dealer.score>21:
                if self.players[name].score==21 and len(self.players[name].cards)==2:                #Blackjack
                    self.panel[name].setBank(2.5*self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
                elif self.players[name].score<=21:                                                   #win
                    self.panel[name].setBank(2*self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
            else:
                if self.players[name].score==21 and len(self.players[name].cards)==2:                #Blackjack
                    self.panel[name].setBank(2.5*self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
                elif self.players[name].score<=21 and self.players[name].score>self.dealer.score:    #win
                    self.panel[name].setBank(2*self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))
                elif self.players[name].score<=21 and self.players[name].score==self.dealer.score:    #draw
                    self.panel[name].setBank(self.panel[name].bet.get())
                    self.panel[name].mlab.configure(text="Cash: %s $" %(self.panel[name].money))

    def nextround(self):
        "Initialize the next round"
        for name in self.panel:
            self.panel[name].e.configure(state=NORMAL)
            if self.players[name].status==2:
                self.players[name].status=1
            self.players[name].cards=[]
            self.players[name].cpics={}
            self.players[name].score=0
        self.startB.configure(state=NORMAL)
        self.dealer.score=0
        self.dealer.cards=[]
        self.dealer.cpics={}
        self.gamestate=0

    def checkBet(self):
        for name in self.panel:
            if self.players[name]==1:
                try:
                    bet=self.panel[name].bet.get()
                    if bet>self.panel[name].money or bet<=0:
                        self.game.itemconfig(self.messages[name],text="%s the bet must be an integer between 1 and %s" %(name,self.panel[name].money),font=('Times',15,'bold'),fill='yellow',width=145)
                        return 0

                except:
                    self.game.itemconfig(self.messages[name],text="%s the bet must be an integer between 1 and %s" %(name,self.panel[name].money),font=('Times',15,'bold'),fill='yellow',width=145)
                    return 0
        return 1

    def surrender(self):
        pass

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
        self.dealer.score=0
        self.dealer.cards=[]
        self.game.itemconfig(self.dealer_message,text="Ready" , font=('Times',20,'bold'),fill='Red')
        self.game.itemconfig(self.dealer_score_p,text="Points: 0 " , font=('Arial',10,'bold'),fill='White')
        self.gamestate=0


    def quit(self):
        pass

if __name__=='__main__':
    BlackJack().mainloop()




__author__ = 'Klafa'
