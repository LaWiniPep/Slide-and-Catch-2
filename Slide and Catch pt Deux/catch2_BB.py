import pygame, simpleGE, random, json

"""
catch.py
slide and catch game
Alex
"""

class Egg(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Egg.png")
        self.setSize(35,25)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        #move it to the top
        self.y = 10
        
        #x is random 0 - scrren width
        self.x = random.randint(0, self.screenWidth)
        
        #dy is random minSpeed to maxSpeed
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
        
class Duck(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Duck.png")
        self.setSize(80,50)
        self.position = (250, 350)
        self.moveSpeed = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed

class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        self.score = 0

class LblTimer(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "TimeLeft: 10"
        self.center = (500, 30)
        

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Olympic.jpg")
        
        self.sndEgg = simpleGE.Sound("Quack.wav")
        self.numEggs = 3
        self.score = 0
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 60
        self.lblTime = LblTimer()
        
        self.lblScore = LblScore()
        
        self.duck = Duck(self)
        
        self.eggs = []
        
        for i in range(self.numEggs):
            self.eggs.append(Egg(self))
        
        self.sprites = [self.duck,
                        *self.eggs,
                        self.lblScore,
                        self.lblTime]
        

        
    def process(self):
        for egg in self.eggs:
            if egg.collidesWith(self.duck):
                egg.reset()
                self.sndEgg.play()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Timer Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score}")
            self.stop()
            
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore, highScore):
        super().__init__()
        self.setImage("Olympic.jpg")
        self.response = "Quit"
        self.prevScore = prevScore
        self.highScore = highScore
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "Congrats! You are a duck!",
        "Move left and right with the arrow keys",
        "Catch the eggs!",
        "How many can you catch?",
        "QUACK"]
        
        self.directions.center = (320, 240)
        self.directions.size = (500,250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        self.lblHighScore = simpleGE.Label()
        self.lblHighScore.center = (320, 50)
        self.lblHighScore.text = f"High Score: {self.highScore}"
        
        
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (320,400)       
        self.lblScore.text = f"Last Score: {self.prevScore}"
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore,
                        self.lblHighScore]
    
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
            
def saveHighScore(high_score, filename="highScore.json"):
    with open(filename, "w") as file:
        json.dump({"highScore": high_score}, file)
        
def loadHighScore(filename="highScore.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data.get("highScore", 0)
    except FileNotFoundError:
        return 0

def main():
    
    keepGoing = True
    lastScore = 0
    highScore = loadHighScore()
    while keepGoing:
        
        instructions = Instructions(lastScore, highScore)
        instructions.start()
        
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
            if lastScore > highScore:
                highScore = lastScore
        else:
            keepGoing = False
     
    saveHighScore(highScore)
    
if __name__ == "__main__":
    main()