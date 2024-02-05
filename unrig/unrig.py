import cloudscraper
import random

scraper = cloudscraper.create_scraper(
    browser={
        'custom': 'ScraperBot/1.0',
    }
)

class Unrig:
    @staticmethod
    def unrig(auth):
        headers = {
            'X-Auth-Token': auth
        }
        jason = {'mines': 1, 'betAmount': '5'}
        r = scraper.post('https://api.bloxflip.com/games/mines/create', headers=headers, json=jason).json()
        if not r['success']:
            return 'failed game creation'

        for _ in range(10):
            mine = random.randint(0, 24)
            json = {'cashout': 'false', 'mine': mine}

            r123 = scraper.post('https://api.bloxflip.com/games/mines/action', headers=headers, json=json).json()

            if r123['exploded']:
                return 'exploded'
            else:
                scraper.post('https://api.bloxflip.com/games/mines/action', headers=headers, json={'cashout': True})

        return 'unrigged'
