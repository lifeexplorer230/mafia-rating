"""
Обработчик ввода данных с консоли
"""
import sys
from typing import List
from models import Player, Role


class InputHandler:
    """Обрабатывает ввод данных от пользователя"""

    ROLE_MAP = {
        "1": Role.CIVILIAN,
        "2": Role.SHERIFF,
        "3": Role.MAFIA,
        "4": Role.DON,
        "мирный": Role.CIVILIAN,
        "шериф": Role.SHERIFF,
        "мафия": Role.MAFIA,
        "дон": Role.DON,
    }

    def __init__(self):
        """Инициализация с настройкой кодировки"""
        # Настройка кодировки для stdin/stdout
        if hasattr(sys.stdin, 'reconfigure'):
            try:
                sys.stdin.reconfigure(encoding='utf-8', errors='replace')
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            except:
                pass

    def _safe_input(self, prompt: str) -> str:
        """Безопасный ввод с обработкой разных кодировок"""
        try:
            return input(prompt)
        except UnicodeDecodeError:
            # Пробуем с другой кодировкой
            try:
                import locale
                encoding = locale.getpreferredencoding()
                sys.stdin = open(sys.stdin.fileno(), 'r', encoding=encoding, errors='replace')
                return input(prompt)
            except:
                print("\nОШИБКА: Проблема с кодировкой терминала.")
                print("Используйте только английские буквы для имен или настройте UTF-8 в терминале.")
                return ""

    def get_players(self) -> List[Player]:
        """Получить список игроков от пользователя"""
        players = []
        REQUIRED_PLAYERS = 10

        print(f"Введите данные для {REQUIRED_PLAYERS} игроков.")
        print()

        # Ввод ровно 10 игроков
        for player_num in range(1, REQUIRED_PLAYERS + 1):
            print(f"--- Игрок {player_num} ---")

            # Имя
            name = self._safe_input("Имя: ").strip()
            if not name:
                print("Имя не может быть пустым!")
                name = self._safe_input("Имя: ").strip()

            # Роль
            role = self._get_role()

            # Когда убит
            killed_when = self._get_killed_when()

            # Создаем игрока (проверки для Шерифа запросим позже)
            player = Player(
                name=name,
                role=role,
                killed_when=killed_when,
                checked_players=[]
            )
            players.append(player)
            print()

        # Валидация состава
        self._validate_roles(players)

        # ПОСЛЕ ввода всех игроков запрашиваем проверки Шерифа
        self._get_sheriff_checks_after_all(players)

        return players

    def _get_role(self) -> Role:
        """Получить роль игрока"""
        print("Роль (1-Мирный, 2-Шериф, 3-Мафия, 4-Дон): ", end="")
        while True:
            role_input = self._safe_input("").strip().lower()
            if role_input in self.ROLE_MAP:
                return self.ROLE_MAP[role_input]
            print("Неверный ввод. Введите 1, 2, 3 или 4: ", end="")

    def _get_killed_when(self) -> str:
        """Получить информацию о том, когда убит игрок"""
        while True:
            killed = self._safe_input("Когда убит (0-жив, 1D/1N/2D/2N...): ").strip().upper()

            # Жив
            if not killed or killed == "0":
                return "0"

            # Проверка формата: должно быть цифра + D или N
            if len(killed) >= 2:
                # Извлекаем число и букву
                day_part = killed[:-1]  # всё кроме последнего символа
                letter = killed[-1]     # последний символ

                # Проверяем: число + (D или N)
                if day_part.isdigit() and letter in ('D', 'N'):
                    return killed

            print("Неверный формат! Используйте: 0 (жив), 1D, 2N, 3D и т.д.")
            print("Где число - это день, D - убит днём, N - убит ночью")
            print("Попробуйте снова: ", end="")

    def _get_sheriff_checks_after_all(self, players: List[Player]):
        """Запросить проверки Шерифа ПОСЛЕ ввода всех игроков"""
        # Находим Шерифа
        sheriff = None
        for p in players:
            if p.role == Role.SHERIFF:
                sheriff = p
                break

        if not sheriff:
            return  # Нет Шерифа (не должно произойти после валидации)

        print(f"\n--- Проверки для {sheriff.name} (Шериф) ---")
        checked_names = self._get_checked_players(players)
        sheriff.checked_players = checked_names
        print()

    def _get_checked_players(self, players: List[Player]) -> List[str]:
        """Получить список проверенных игроков (для Шерифа)"""
        if not players:
            return []

        # Показываем список игроков с номерами
        print("Список игроков:")
        for i, p in enumerate(players, 1):
            print(f"  {i}. {p.name}")

        checked_str = self._safe_input("Кого проверил (номера через запятую, например 1,3,5): ").strip()
        if not checked_str:
            return []

        # Разбиваем по запятым и проверяем
        checked_names = []
        for num_str in checked_str.split(","):
            num_str = num_str.strip()
            if not num_str:
                continue

            try:
                num = int(num_str)
                if 1 <= num <= len(players):
                    # Конвертируем номер в имя игрока
                    checked_names.append(players[num - 1].name)
                else:
                    print(f"⚠️  Номер {num} вне диапазона (1-{len(players)}), пропущен")
            except ValueError:
                print(f"⚠️  '{num_str}' не является числом, пропущен")

        return checked_names

    def _validate_roles(self, players: List[Player]):
        """Валидация состава: должен быть ровно 1 Шериф и 1 Дон"""
        sheriffs = [p for p in players if p.role == Role.SHERIFF]
        dons = [p for p in players if p.role == Role.DON]

        # Проверка Шерифов
        if len(sheriffs) == 0:
            print("\n⚠️  ОШИБКА: В игре должен быть Шериф!")
            self._fix_missing_role(players, Role.SHERIFF, "Шериф")
        elif len(sheriffs) > 1:
            print(f"\n⚠️  ОШИБКА: Шерифов должно быть 1, а указано {len(sheriffs)}!")
            self._fix_duplicate_role(players, sheriffs, "Шериф")

        # Проверка Донов
        if len(dons) == 0:
            print("\n⚠️  ОШИБКА: В игре должен быть Дон!")
            self._fix_missing_role(players, Role.DON, "Дон")
        elif len(dons) > 1:
            print(f"\n⚠️  ОШИБКА: Донов должно быть 1, а указано {len(dons)}!")
            self._fix_duplicate_role(players, dons, "Дон")

        print("\n✅ Состав проверен и исправлен!")

    def _fix_missing_role(self, players: List[Player], target_role: Role, role_name: str):
        """Исправить отсутствие роли"""
        print(f"\nУкажите, кто из игроков является {role_name}:")
        for i, p in enumerate(players, 1):
            print(f"  {i}. {p.name} ({p.role.value})")

        while True:
            try:
                choice = int(self._safe_input(f"Номер игрока (1-{len(players)}): "))
                if 1 <= choice <= len(players):
                    players[choice - 1].role = target_role
                    print(f"✅ {players[choice - 1].name} теперь {role_name}")
                    break
                else:
                    print(f"Введите число от 1 до {len(players)}")
            except ValueError:
                print("Введите число!")

    def _fix_duplicate_role(self, players: List[Player], duplicates: List[Player], role_name: str):
        """Исправить дублирование роли"""
        print(f"\nНайдено несколько игроков с ролью {role_name}:")
        for i, p in enumerate(duplicates, 1):
            player_num = players.index(p) + 1
            print(f"  {player_num}. {p.name}")

        print(f"\nКакой из них действительно {role_name}?")
        for i, p in enumerate(duplicates, 1):
            player_num = players.index(p) + 1
            answer = self._safe_input(f"{player_num}. {p.name} - это {role_name}? (да/нет): ").strip().lower()
            if answer in ('да', 'yes', 'y', 'д'):
                print(f"✅ {p.name} остаётся {role_name}")
                # Остальных делаем Мирными
                for other in duplicates:
                    if other != p:
                        other.role = Role.CIVILIAN
                        print(f"   {other.name} изменён на Мирный")
                break
