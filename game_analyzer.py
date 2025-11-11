"""
Анализатор игры - определяет победителя, угадайку, особые условия
"""
from typing import List
from models import Player, GameAnalysis, Team, Role


class GameAnalyzer:
    """Анализирует результаты игры"""

    def __init__(self, players: List[Player]):
        self.players = players

    def analyze(self) -> GameAnalysis:
        """Провести полный анализ игры"""
        alive_players = [p for p in self.players if p.is_alive()]
        alive_count = len(alive_players)

        # Определяем победителя
        winner = self._determine_winner(alive_players)

        # Определяем особые условия
        is_guessing, guessing_players = self._check_guessing()
        clean_civilian_win = self._check_clean_civilian_win(winner)
        dry_mafia_win = self._check_dry_mafia_win(winner)

        return GameAnalysis(
            winner=winner,
            is_guessing=is_guessing,
            clean_civilian_win=clean_civilian_win,
            dry_mafia_win=dry_mafia_win,
            alive_players_count=alive_count,
            guessing_players=guessing_players
        )

    def _determine_winner(self, alive_players: List[Player]) -> Team:
        """
        Определить победителя игры

        Правила:
        - Если мафии не осталось → Мирные победили
        - Если мирных ≤ мафии → Мафия победила
        """
        alive_mafia = [p for p in alive_players if p.get_team() == Team.MAFIA]
        alive_civilians = [p for p in alive_players if p.get_team() == Team.CIVILIANS]

        if len(alive_mafia) == 0:
            return Team.CIVILIANS
        elif len(alive_civilians) <= len(alive_mafia):
            return Team.MAFIA
        else:
            # Это состояние не должно быть достигнуто в конце игры
            return Team.CIVILIANS

    def _check_guessing(self) -> tuple[bool, List[str]]:
        """
        Проверить, была ли угадайка

        Угадайка = на момент последнего голосования было ровно 3 игрока

        Returns:
            (была_угадайка, список_имен_участников)
        """
        # Находим последний день голосования (максимальный день среди убитых днем)
        last_vote_day = 0
        for p in self.players:
            if p.killed_by_vote():
                day = p.get_kill_day()
                if day and day > last_vote_day:
                    last_vote_day = day

        if last_vote_day == 0:
            return (False, [])  # Не было голосований

        # Находим игроков, которые были живы ПЕРЕД последним днем голосования
        # Живы те, кто: жив сейчас ИЛИ убит в день >= last_vote_day
        guessing_players = []
        for p in self.players:
            if p.is_alive():
                # Игрок жив в конце - был жив перед последним голосованием
                guessing_players.append(p.name)
            else:
                kill_day = p.get_kill_day()
                if kill_day and kill_day >= last_vote_day:
                    # Убит в последний день голосования или позже - был жив перед ним
                    guessing_players.append(p.name)

        is_guessing = len(guessing_players) == 3
        return (is_guessing, guessing_players if is_guessing else [])

    def _check_clean_civilian_win(self, winner: Team) -> bool:
        """
        Проверить чистую победу мирных

        Чистая победа = все мафиози убиты днем (голосованием)
        И ни один мирный не был убит днем (голосованием)
        """
        if winner != Team.CIVILIANS:
            return False

        mafia_players = [p for p in self.players if p.get_team() == Team.MAFIA]
        civilian_players = [p for p in self.players if p.get_team() == Team.CIVILIANS]

        # Все мафиози должны быть убиты голосованием (днем)
        all_mafia_killed_by_vote = all(p.killed_by_vote() for p in mafia_players)

        # Ни один мирный не должен быть убит днём (голосованием)
        no_civilian_killed_by_vote = not any(p.killed_by_vote() for p in civilian_players)

        return all_mafia_killed_by_vote and no_civilian_killed_by_vote

    def _check_dry_mafia_win(self, winner: Team) -> bool:
        """
        Проверить победу мафии в сухую

        Победа в сухую = ни один мафиози не убит
        """
        if winner != Team.MAFIA:
            return False

        mafia_players = [p for p in self.players if p.get_team() == Team.MAFIA]

        # Все мафиози должны быть живы
        return all(p.is_alive() for p in mafia_players)

    def get_sheriff_checks(self, sheriff: Player) -> tuple[int, int]:
        """
        Подсчитать черные и красные проверки Шерифа

        Returns:
            (черные_проверки, красные_проверки)
        """
        if sheriff.role != Role.SHERIFF:
            return (0, 0)

        black_checks = 0  # Правильно нашел мафию
        red_checks = 0    # Проверил мирного

        # Создаем словарь игроков для быстрого поиска
        players_dict = {p.name: p for p in self.players}

        for checked_name in sheriff.checked_players:
            checked_name = checked_name.strip()
            if checked_name in players_dict:
                checked_player = players_dict[checked_name]
                if checked_player.get_team() == Team.MAFIA:
                    black_checks += 1
                else:
                    red_checks += 1

        return (black_checks, red_checks)
