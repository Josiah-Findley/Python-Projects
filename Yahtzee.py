class Game():

    def __init__(self, HumPlayers, AIPlayers):
        super(Game, self).__init__()
        self.AIPlayers = AIPlayers
        self.HumPlayers = HumPlayers
        self.players=[]
        self.askForNames(5, 4)
        print(self.players)




# Asks for Humans Names and adds those and Comp Names to players list
    def askForNames(self, HumPlayers, AIPlayers):
        for x in range(HumPlayers):
            t = True;
            while (t == True):
                try:
                    getnames = input("Enter player "+str(x+1)+"'s name. (3 Letter Abbr.): ")
                    for name in self.players:
                        if (name.casefold() == getnames.casefold()): # Same name as some one else
                            raise NameError("Name Already Taken, please try again.")
                    if(len(getnames)!=3):
                        raise Exception("Name is too long. Please choose only 3 letters.")

                    t = False
                #Error handling
                except NameError as altak:
                    print(altak.args[0])
                except Exception as ntolo:
                    print(ntolo.args[0])
            self.players.append(getnames)
        #Giving the Computer Names
        for x in range(AIPlayers):
            self.players.append("AI"+str(x+1))







def main():
    print("Welcome to Yahtzee!\n")
    Game(4,5)


if __name__== "__main__":
  main()