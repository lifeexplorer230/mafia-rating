#!/usr/bin/env python3
"""
Тест системы на примере игры
"""

from models import Player, Role
from game_analyzer import GameAnalyzer
from rating_calculator import RatingCalculator
from output_formatter import OutputFormatter


def test_game_1():
    """
    Тестовая игра: Мирные победили чистой победой
    Все мафиози убиты голосованием
    """
    print("\n" + "="*60)
    print("ТЕСТ 1: Чистая победа мирных")
    print("="*60)

    players = [
        Player("Иван", Role.CIVILIAN, "0"),
        Player("Мария", Role.CIVILIAN, "2N"),
        Player("Петр", Role.SHERIFF, "0", ["Алексей", "Сергей", "Ольга"]),
        Player("Алексей", Role.DON, "2D"),
        Player("Сергей", Role.MAFIA, "1D"),
        Player("Ольга", Role.CIVILIAN, "1N"),
        Player("Николай", Role.CIVILIAN, "0"),
    ]

    analyzer = GameAnalyzer(players)
    analysis = analyzer.analyze()

    calculator = RatingCalculator(players, analysis, analyzer)
    results = calculator.calculate_all()

    formatter = OutputFormatter()
    formatter.print_results(results, analysis)


def test_game_2():
    """
    Тестовая игра: Мафия победила в угадайке
    """
    print("\n" + "="*60)
    print("ТЕСТ 2: Мафия победила в угадайке")
    print("="*60)

    players = [
        Player("Игрок1", Role.CIVILIAN, "3N"),
        Player("Игрок2", Role.CIVILIAN, "2D"),
        Player("Игрок3", Role.SHERIFF, "1D"),
        Player("Игрок4", Role.DON, "0"),
        Player("Игрок5", Role.MAFIA, "2N"),
        Player("Игрок6", Role.CIVILIAN, "1N"),
        Player("Игрок7", Role.CIVILIAN, "0"),
        Player("Игрок8", Role.CIVILIAN, "0"),
    ]

    analyzer = GameAnalyzer(players)
    analysis = analyzer.analyze()

    calculator = RatingCalculator(players, analysis, analyzer)
    results = calculator.calculate_all()

    formatter = OutputFormatter()
    formatter.print_results(results, analysis)


def test_game_3():
    """
    Тестовая игра: Шериф с 3 черными проверками
    """
    print("\n" + "="*60)
    print("ТЕСТ 3: Шериф с 3 черными проверками")
    print("="*60)

    players = [
        Player("Шериф1", Role.SHERIFF, "0", ["Дон1", "Мафия1", "Мафия2"]),
        Player("Мирный1", Role.CIVILIAN, "2N"),
        Player("Мирный2", Role.CIVILIAN, "0"),
        Player("Мирный3", Role.CIVILIAN, "1N"),
        Player("Дон1", Role.DON, "3D"),
        Player("Мафия1", Role.MAFIA, "2D"),
        Player("Мафия2", Role.MAFIA, "1D"),
    ]

    analyzer = GameAnalyzer(players)
    analysis = analyzer.analyze()

    calculator = RatingCalculator(players, analysis, analyzer)
    results = calculator.calculate_all()

    formatter = OutputFormatter()
    formatter.print_results(results, analysis)


if __name__ == "__main__":
    test_game_1()
    test_game_2()
    test_game_3()
    print("\n" + "="*60)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
    print("="*60 + "\n")
