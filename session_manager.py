"""
Менеджер игровой сессии - управляет несколькими играми за день
"""
from typing import List, Dict
from collections import defaultdict
from models import RatingResult


class PlayerStats:
    """Статистика игрока за игровой день"""
    def __init__(self, name: str):
        self.name = name
        self.total_points = 0
        self.games_played = 0
        self.game_results = []  # Список результатов по играм

    def add_game_result(self, points: int):
        """Добавить результат игры"""
        self.total_points += points
        self.games_played += 1
        self.game_results.append(points)

    def average_points(self) -> float:
        """Средний балл за игру"""
        if self.games_played == 0:
            return 0.0
        return self.total_points / self.games_played


class SessionManager:
    """Управляет игровой сессией (несколько игр за день)"""

    def __init__(self, total_games: int):
        self.total_games = total_games
        self.current_game = 0
        self.player_stats: Dict[str, PlayerStats] = defaultdict(lambda: PlayerStats(""))

    def add_game_results(self, results: List[RatingResult]):
        """Добавить результаты одной игры"""
        self.current_game += 1

        for result in results:
            player_name = result.player.name

            # Инициализируем, если игрок новый
            if player_name not in self.player_stats:
                self.player_stats[player_name] = PlayerStats(player_name)

            # Добавляем результат игры
            self.player_stats[player_name].add_game_result(result.total_points)

    def get_all_players(self) -> List[PlayerStats]:
        """Получить всех игроков, отсортированных по баллам"""
        players = list(self.player_stats.values())
        # Сортируем: сначала по баллам (убывание), потом по количеству игр (убывание)
        players.sort(key=lambda p: (p.total_points, p.games_played), reverse=True)
        return players

    def get_best_player(self) -> PlayerStats:
        """
        Получить лучшего игрока дня

        Лучший игрок = максимум баллов среди сыгравших 3+ игры
        """
        qualified_players = [p for p in self.player_stats.values() if p.games_played >= 3]

        if not qualified_players:
            return None

        # Сортируем по баллам
        qualified_players.sort(key=lambda p: p.total_points, reverse=True)
        return qualified_players[0]

    def is_complete(self) -> bool:
        """Все ли игры сыграны"""
        return self.current_game >= self.total_games
