import numpy as np
import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        'custom': 'ScraperBot/1.0',
    }
)

class Prediction:
    @staticmethod
    def gethistory():
        response = scraper.get('https://api.bloxflip.com/games/roulette')
        data = response.json()['history'][:16]
        winningColors = [game["winningColor"] for game in data]
        return winningColors
    
    @staticmethod
    def predict():
        games = Prediction.gethistory()
        
        X_train = []
        y_train = []
        
        for i in range(1, len(games)):
            X_train.append(games[i-1])
            y_train.append(games[i])
        
        unique = list(set(X_train))
        colortoindex = {color: i for i, color in enumerate(unique)}
        indextocolor = {i: color for i, color in enumerate(unique)}
        Xtrainencodedd = np.array([colortoindex[color] for color in X_train])
        transition_matrix = np.zeros((len(unique), len(unique)))
        for i in range(1, len(Xtrainencodedd)):
            transition_matrix[Xtrainencodedd[i-1], Xtrainencodedd[i]] += 1
        transition_matrix /= transition_matrix.sum(axis=1, keepdims=True)
        lastcolor = colortoindex[games[-1]]
        predictionencoded = np.argmax(transition_matrix[lastcolor])
        prediction = indextocolor[predictionencoded]
        
        return prediction
