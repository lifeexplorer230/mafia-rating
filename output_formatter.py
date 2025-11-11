"""
Форматтер вывода результатов
"""
from typing import List
from models import RatingResult, GameAnalysis


class OutputFormatter:
    """Форматирует и выводит результаты на экран"""

    def print_results(self, results: List[RatingResult], analysis: GameAnalysis):
        """Вывести результаты игры"""
        print()
        print("=" * 60)
        print("РЕЗУЛЬТАТЫ ИГРЫ")
        print("=" * 60)
        print()

        # Информация об игре
        print(f"🏆 Победитель: {analysis.winner.value}")
        if analysis.is_guessing:
            print("🎲 Была угадайка!")
        if analysis.clean_civilian_win:
            print("✨ Чистая победа мирных!")
        if analysis.dry_mafia_win:
            print("💧 Победа мафии в сухую!")
        print()
        print("-" * 60)

        # Результаты по игрокам
        for result in results:
            self._print_player_result(result)
            print("-" * 60)

        print()

    def _print_player_result(self, result: RatingResult):
        """Вывести результат для одного игрока"""
        player = result.player
        print()
        print(f"👤 {player.name} ({player.role.value})")

        if result.breakdowns:
            for breakdown in result.breakdowns:
                sign = "+" if breakdown.points >= 0 else ""
                print(f"   {breakdown.description}: {sign}{breakdown.points}")
        else:
            print("   Нет начисленных баллов")

        # Итоговый балл
        total = result.total_points
        sign = "+" if total >= 0 else ""
        print()
        print(f"   ⭐ ИТОГО: {sign}{total}")
        print()
