import os

file_path = "./resources/settings/high_scores.txt"

def load_high_scores():
    try:
        with open(file_path, "r") as file:
            scores = {}
            for line in file.readlines():
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    player_name, score = parts
                    scores[player_name] = int(score)
                else:
                    print('Erro ao ler pontuações: linha inválida')
            return scores
    except FileNotFoundError:
        return {}

def save_high_scores(scores):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        for player_name, score in scores.items():
            file.write(f"{player_name}: {score}\n")

def update_high_score(player_name, new_score):
    scores = load_high_scores()
    if player_name in scores:
        if new_score > scores[player_name]:
            scores[player_name] = new_score
    else:
        scores[player_name] = new_score
    save_high_scores(scores)
