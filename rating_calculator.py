"""
Калькулятор рейтинга - начисляет баллы игрокам по правилам
"""
from typing import List
from models import Player, GameAnalysis, RatingResult, Role, Team
from game_analyzer import GameAnalyzer


class RatingCalculator:
    """Рассчитывает рейтинг игроков"""

    def __init__(self, players: List[Player], analysis: GameAnalysis, analyzer: GameAnalyzer):
        self.players = players
        self.analysis = analysis
        self.analyzer = analyzer

    def calculate_all(self) -> List[RatingResult]:
        """Рассчитать рейтинг для всех игроков"""
        results = []
        for player in self.players:
            result = self._calculate_player_rating(player)
            results.append(result)
        return results

    def _calculate_player_rating(self, player: Player) -> RatingResult:
        """Рассчитать рейтинг для одного игрока"""
        result = RatingResult(player=player)

        # Определяем победил ли игрок
        player_won = player.get_team() == self.analysis.winner

        # Базовые баллы за победу/поражение по роли
        if player.role == Role.CIVILIAN:
            self._calculate_civilian_points(player, player_won, result)
        elif player.role == Role.MAFIA:
            self._calculate_mafia_points(player, player_won, result)
        elif player.role == Role.DON:
            self._calculate_don_points(player, player_won, result)
        elif player.role == Role.SHERIFF:
            self._calculate_sheriff_points(player, player_won, result)

        return result

    def _calculate_civilian_points(self, player: Player, won: bool, result: RatingResult):
        """Начислить баллы мирному"""
        if won:
            result.add_points("Победа за Мирного", +4)

            # Чистая победа
            if self.analysis.clean_civilian_win:
                result.add_points("Чистая победа", +1)

            # Угадайка (только для игроков, которые участвовали)
            if self.analysis.is_guessing and player.name in self.analysis.guessing_players:
                result.add_points("Победа в угадайке", +2)

    def _calculate_mafia_points(self, player: Player, won: bool, result: RatingResult):
        """Начислить баллы обычной мафии"""
        if won:
            result.add_points("Победа за Мафию", +5)

            # Победа в сухую
            if self.analysis.dry_mafia_win:
                result.add_points("Победа в сухую", +1)

            # Угадайка (только для игроков, которые участвовали)
            if self.analysis.is_guessing and player.name in self.analysis.guessing_players:
                result.add_points("Победа в угадайке", +3)

    def _calculate_don_points(self, player: Player, won: bool, result: RatingResult):
        """Начислить баллы Дону"""
        if won:
            # Базовая победа за Мафию (Дон - часть команды мафии)
            result.add_points("Победа за Мафию", +5)

            # Победа за Дона (дополнительно)
            result.add_points("Победа за Дона", +3)

            # Не покидал стола
            if player.is_alive():
                result.add_points("Не покидал стола", +1)

            # Победа в сухую (как часть мафии)
            if self.analysis.dry_mafia_win:
                result.add_points("Победа в сухую", +1)

            # Угадайка (только для игроков, которые участвовали)
            if self.analysis.is_guessing and player.name in self.analysis.guessing_players:
                result.add_points("Победа в угадайке", +3)
        else:
            # Поражение за Дона
            result.add_points("Поражение за Дона", -3)

    def _calculate_sheriff_points(self, player: Player, won: bool, result: RatingResult):
        """Начислить баллы Шерифу"""
        if won:
            # Базовая победа за Мирных (Шериф - часть команды мирных)
            result.add_points("Победа за Мирного", +4)

            # Победа за Шерифа (дополнительно)
            result.add_points("Победа за Шерифа", +3)

            # Не покидал стола
            if player.is_alive():
                result.add_points("Не покидал стола", +2)

            # Угадайка (только для игроков, которые участвовали)
            if self.analysis.is_guessing and player.name in self.analysis.guessing_players:
                result.add_points("Победа в угадайке", +2)
        else:
            # Поражение за Шерифа
            result.add_points("Поражение за Шерифа", -3)

            # Покинул игру ДНЁМ в 1-й или 2-й день (только если убит голосованием!)
            kill_day = player.get_kill_day()
            if player.killed_by_vote() and kill_day in (1, 2):
                result.add_points("Покинул игру в 1-й или 2-й день", -1)

        # Проверки (начисляются всегда)
        black_checks, red_checks = self.analyzer.get_sheriff_checks(player)

        if black_checks >= 3:
            result.add_points("3 черные проверки", +3)

        if red_checks >= 3:
            result.add_points("3 красные проверки", +2)
