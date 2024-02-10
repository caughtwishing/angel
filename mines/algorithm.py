from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        'custom': 'ScraperBot/1.0',
    }
)

class Algorithm:
    def build_grid(self, clicked_spots, mines_location):
        X = []
        y = []
        for tile in range(0, 25):
            row = tile // 5
            col = tile % 5
            adjacent_mines = sum(1 for i in [-1, 0, 1] for j in [-1, 0, 1] if (row+i, col+j) in mines_location)
            feature_vector = [row, col, adjacent_mines]
            if tile in clicked_spots:
                X.append(feature_vector)
                y.append(1)
            else:
                X.append(feature_vector)
                y.append(0)
        return np.array(X), np.array(y)

    def predict(self, clicked_spots, mines_location, safe):
        X_train, y_train = self.build_grid(clicked_spots, mines_location)

        X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state=0)

        rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0)
        rf.fit(X_train, y_train)

        valid_proba = rf.predict_proba(X_valid)
        valid_safe_spots = np.argsort(valid_proba[:, 0])[::-1][:safe]

        train_proba = rf.predict_proba(X_train)
        train_safe_spots = np.argsort(train_proba[:, 0])[::-1][:safe]

        grid = [0] * 25
        for x in train_safe_spots:
            grid[x] = 1
        
        return grid
