#!/usr/bin/env python3
"""
Тест валидации и чистой победы
"""

from models import Player, Role
from game_analyzer import GameAnalyzer
from rating_calculator import RatingCalculator
from output_formatter import OutputFormatter


def test_clean_win_correct():
    """
    Правильная чистая победа:
    - Все мафиози убиты днём
    - Ни один мирный не убит днём
    """
    print("\n" + "="*60)
    print("ТЕСТ: Правильная чистая победа")
    print("="*60)

    players = [
        Player("Мирный1", Role.CIVILIAN, "1N"),  # убит ночью - ОК
        Player("Мирный2", Role.CIVILIAN, "0"),
        Player("Мирный3", Role.CIVILIAN, "2N"),  # убит ночью - ОК
        Player("Мирный4", Role.CIVILIAN, "0"),
        Player("Мирный5", Role.CIVILIAN, "0"),
        Player("Мирный6", Role.CIVILIAN, "0"),
        Player("Шериф", Role.SHERIFF, "0"),
        Player("Дон", Role.DON, "2D"),      # убит днём - ОК
        Player("Мафия1", Role.MAFIA, "1D"), # убит днём - ОК
        Player("Мафия2", Role.MAFIA, "3D"), # убит днём - ОК
    ]

    analyzer = GameAnalyzer(players)
    analysis = analyzer.analyze()

    print(f"Победитель: {analysis.winner.value}")
    print(f"Чистая победа: {'ДА' if analysis.clean_civilian_win else 'НЕТ'}")
    print("✅ Ожидается: Чистая победа ДА")


def test_clean_win_false():
    """
    НЕ чистая победа:
    - Все мафиози убиты днём
    - НО мирный был убит днём (ошибочно)
    """
    print("\n" + "="*60)
    print("ТЕСТ: НЕ чистая победа (мирный убит днём)")
    print("="*60)

    players = [
        Player("Мирный1", Role.CIVILIAN, "1D"),  # убит днём - ПЛОХО!
        Player("Мирный2", Role.CIVILIAN, "0"),
        Player("Мирный3", Role.CIVILIAN, "2N"),
        Player("Мирный4", Role.CIVILIAN, "0"),
        Player("Мирный5", Role.CIVILIAN, "0"),
        Player("Мирный6", Role.CIVILIAN, "0"),
        Player("Шериф", Role.SHERIFF, "0"),
        Player("Дон", Role.DON, "2D"),
        Player("Мафия1", Role.MAFIA, "3D"),
        Player("Мафия2", Role.MAFIA, "4D"),
    ]

    analyzer = GameAnalyzer(players)
    analysis = analyzer.analyze()

    print(f"Победитель: {analysis.winner.value}")
    print(f"Чистая победа: {'ДА' if analysis.clean_civilian_win else 'НЕТ'}")
    print("✅ Ожидается: Чистая победа НЕТ")


if __name__ == "__main__":
    test_clean_win_correct()
    test_clean_win_false()
    print("\n" + "="*60)
    print("ТЕСТЫ ЗАВЕРШЕНЫ")
    print("="*60 + "\n")
