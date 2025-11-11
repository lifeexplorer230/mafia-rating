#!/usr/bin/env python3
"""
Система рейтинга Мафии v2
Точка входа в приложение
"""

from input_handler import InputHandler
from game_analyzer import GameAnalyzer
from rating_calculator import RatingCalculator
from output_formatter import OutputFormatter


def main():
    """Главная функция приложения"""
    try:
        # 1. Получаем данные от пользователя
        input_handler = InputHandler()
        players = input_handler.get_players()

        if not players:
            print("Не введено ни одного игрока. Завершение.")
            return

        # 2. Анализируем игру
        analyzer = GameAnalyzer(players)
        analysis = analyzer.analyze()

        # 3. Рассчитываем рейтинг
        calculator = RatingCalculator(players, analysis, analyzer)
        results = calculator.calculate_all()

        # 4. Выводим результаты
        formatter = OutputFormatter()
        formatter.print_results(results, analysis)

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\n\nОшибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
