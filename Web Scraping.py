import requests
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass
from typing import List

# Classes de dados 'Item'
@dataclass
class Item:
    sport_league: str
    event_date_utc: str
    team1: str
    team2: str
    pitcher: str
    period: str
    line_type: str
    price: str
    side: str
    team: str
    spread: float

def parse_betting_data(url):
    try:
        # Solicitação HTTP para obter o conteúdo da página
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            betting_data = []

            # Linhas de Dados
            betting_lines = soup.find_all('tr', class_='betting-line')

            for line in betting_lines:
                cells = line.find_all('td')

                if len(cells) == 11:
                    item = Item(
                        sport_league=cells[0].text.strip(),
                        event_date_utc=cells[1].text.strip(),
                        team1=cells[2].text.strip(),
                        team2=cells[3].text.strip(),
                        pitcher=cells[4].text.strip(),
                        period=cells[5].text.strip(),
                        line_type=cells[6].text.strip(),
                        price=cells[7].text.strip(),
                        side=cells[8].text.strip(),
                        team=cells[9].text.strip(),
                        spread=float(cells[10].text.strip())
                    )

                    betting_data.append(item)

            return betting_data
        else:
            print('Falha ao recuperar o conteúdo:', response.status_code)
            return None
    except Exception as e:
        print(f'Erro ao analisar os dados: {str(e)}')
        return None

def save_to_json(data, output_file):
    if data:
        with open(output_file, 'w') as file:
            json.dump([asdict(item) for item in data], file, indent=4)
        print(f'Dados salvos em {output_file}')

if __name__ == "__main":
    url = 'https://veri.bet/simulator'  # URL VERI BET
    output_file = 'dados_betting.json'  # NOME ARQUIVO DE SAÍDA JSON

    parsed_data = parse_betting_data(url)

    if parsed_data:
        save_to_json(parsed_data, output_file)
