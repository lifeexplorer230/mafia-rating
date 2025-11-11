#!/usr/bin/env python3
"""
Система рейтинга Мафии v2
Точка входа в приложение
"""

from input_handler import InputHandler
from game_analyzer import GameAnalyzer
from rating_calculator import RatingCalculator
from output_formatter import OutputFormatter
from session_manager import SessionManager
from session_output import SessionOutputFormatter


def get_games_count(input_handler: InputHandler) -> int:
    """Запросить количество игр за игровой день"""
    print("=" * 60)
    print("СИСТЕМА РЕЙТИНГА МАФИИ v2")
    print("=" * 60)
    print()

    while True:
        try:
            count_str = input_handler._safe_input("Сколько игр будет сыграно за игровой день? ").strip()
            count = int(count_str)
            if count < 1:
                print("Количество игр должно быть хотя бы 1. Попробуйте снова.")
                continue
            if count > 20:
                print("Слишком много игр! Максимум 20. Попробуйте снова.")
                continue
            return count
        except ValueError:
            print("Введите число!")


def play_single_game(game_number: int, total_games: int, input_handler: InputHandler):
    """Провести одну игру и вернуть результаты"""
    # Разделитель между играми
    session_formatter = SessionOutputFormatter()
    session_formatter.format_game_separator(game_number, total_games)

    # 1. Получаем данные от пользователя
    players = input_handler.get_players()

    if not players:
        print("Не введено ни одного игрока. Пропускаем игру.")
        return None

    # 2. Анализируем игру
    analyzer = GameAnalyzer(players)
    analysis = analyzer.analyze()

    # 3. Рассчитываем рейтинг
    calculator = RatingCalculator(players, analysis, analyzer)
    results = calculator.calculate_all()

    # 4. Выводим результаты текущей игры
    formatter = OutputFormatter()
    formatter.print_results(results, analysis)

    return results


def main():
    """Главная функция приложения"""
    try:
        input_handler = InputHandler()

        # 1. Запрашиваем количество игр
        total_games = get_games_count(input_handler)
        print(f"\n✅ Будет сыграно игр: {total_games}")
        print()

        # 2. Создаём менеджер сессии
        session = SessionManager(total_games)

        # 3. Проводим каждую игру
        for game_num in range(1, total_games + 1):
            results = play_single_game(game_num, total_games, input_handler)

            if results:
                session.add_game_results(results)

        # 4. Выводим итоговый рейтинг
        session_formatter = SessionOutputFormatter()
        session_formatter.format_final_rating(session)

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\n\nОшибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
