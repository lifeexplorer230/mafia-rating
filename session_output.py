"""
Форматирование вывода итогового рейтинга за игровой день
"""
from typing import List
from session_manager import PlayerStats, SessionManager


class SessionOutputFormatter:
    """Форматирует вывод итогового рейтинга"""

    def format_final_rating(self, session: SessionManager):
        """Вывести итоговый рейтинг за игровой день"""
        print("\n" + "=" * 60)
        print("ИТОГОВЫЙ РЕЙТИНГ ИГРОВОГО ДНЯ")
        print("=" * 60)
        print(f"Всего сыграно игр: {session.total_games}")
        print()

        players = session.get_all_players()

        if not players:
            print("Нет данных об играх.")
            return

        # Определяем лучшего игрока
        best_player = session.get_best_player()

        # Выводим таблицу рейтинга
        print(f"{'№':<4} {'Игрок':<20} {'Игры':<8} {'Очки':<10} {'Среднее':<10} {'Статус'}")
        print("-" * 60)

        for i, player in enumerate(players, 1):
            # Форматируем среднее до 2 знаков
            avg = f"{player.average_points():.2f}"

            # Определяем статус
            status = ""
            if best_player and player.name == best_player.name:
                status = "🏆 ЛУЧШИЙ ИГРОК ДНЯ"
            elif player.games_played >= 3:
                status = "✓ Квалифицирован"

            print(f"{i:<4} {player.name:<20} {player.games_played:<8} {player.total_points:<10} {avg:<10} {status}")

        print("-" * 60)

        # Детальная информация о лучшем игроке
        if best_player:
            print()
            print("🏆 " + "=" * 58)
            print(f"   ЛУЧШИЙ ИГРОК ДНЯ: {best_player.name}")
            print("=" * 60)
            print(f"   Сыграно игр: {best_player.games_played}")
            print(f"   Всего баллов: {best_player.total_points}")
            print(f"   Средний балл: {best_player.average_points():.2f}")
            print(f"   Результаты по играм: {', '.join(map(lambda x: f'{x:+d}' if x >= 0 else str(x), best_player.game_results))}")
            print("=" * 60)
        else:
            print()
            print("⚠️  Нет игроков, сыгравших 3 или более игры.")
            print("   Для звания 'Лучший игрок дня' нужно сыграть минимум 3 игры.")

        print()

    def format_game_separator(self, game_number: int, total_games: int):
        """Разделитель между играми"""
        print("\n" + "🎮 " + "=" * 56)
        print(f"   ИГРА {game_number} из {total_games}")
        print("=" * 60 + "\n")
