import numpy as np
import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        'custom': 'ScraperBot/1.0',
    }
)

class Prediction:
    def getGames(self):
        r = scraper.get('https://api.bloxflip.com/games/crash').json()
        crashPoints = []
        for i in range(10):
            crashPoint = r['history'][i]['crashPoint']
            crashPoints.append(crashPoint)
        return crashPoints

    def predict(self):
        games = np.array(self.getGames())
        X = np.arange(1, len(games) + 1)
        weights = 1 / np.abs(games)
        m, b = np.polyfit(X, games, deg=1, w=weights)
        prediction = m * (len(games) + 1) + b

        return "{:.2f}".format(abs(prediction))
