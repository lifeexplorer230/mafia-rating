"""
Модели данных для системы рейтинга Мафии
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Role(Enum):
    """Роли игроков"""
    CIVILIAN = "Мирный"
    MAFIA = "Мафия"
    DON = "Дон"
    SHERIFF = "Шериф"


class Team(Enum):
    """Команды"""
    CIVILIANS = "Мирные"
    MAFIA = "Мафия"


@dataclass
class Player:
    """Игрок в партии"""
    name: str
    role: Role
    killed_when: str = "0"  # "0" = жив, "1D", "2N" и т.д.
    checked_players: List[str] = field(default_factory=list)  # для Шерифа

    def is_alive(self) -> bool:
        """Проверка, жив ли игрок"""
        return self.killed_when == "0" or not self.killed_when

    def killed_by_vote(self) -> bool:
        """Убит голосованием (днем)"""
        return self.killed_when and "D" in self.killed_when.upper()

    def killed_at_night(self) -> bool:
        """Убит ночью"""
        return self.killed_when and "N" in self.killed_when.upper()

    def get_kill_day(self) -> int:
        """Получить день убийства"""
        if self.is_alive():
            return 0
        try:
            return int(''.join(filter(str.isdigit, self.killed_when)))
        except ValueError:
            return 0

    def get_team(self) -> Team:
        """Получить команду игрока"""
        if self.role in (Role.MAFIA, Role.DON):
            return Team.MAFIA
        return Team.CIVILIANS


@dataclass
class GameAnalysis:
    """Результаты анализа игры"""
    winner: Team
    is_guessing: bool  # Была ли угадайка
    clean_civilian_win: bool  # Чистая победа мирных
    dry_mafia_win: bool  # Победа мафии в сухую
    alive_players_count: int
    guessing_players: List[str] = field(default_factory=list)  # Имена игроков, участвовавших в угадайке


@dataclass
class RatingBreakdown:
    """Детализация начисления баллов"""
    description: str
    points: int


@dataclass
class RatingResult:
    """Результат подсчета рейтинга для игрока"""
    player: Player
    breakdowns: List[RatingBreakdown] = field(default_factory=list)

    @property
    def total_points(self) -> int:
        """Итоговые баллы"""
        return sum(b.points for b in self.breakdowns)

    def add_points(self, description: str, points: int):
        """Добавить баллы"""
        if points != 0:
            self.breakdowns.append(RatingBreakdown(description, points))
