from database import Database
from typing import Dict


class StatisticsCalculator:

    def __init__(self, db: Database):
        self.db = db

    def calculate_completed_count(self) -> int:
        stats = self.db.get_statistics()
        return stats.get('completed_count', 0)

    def calculate_avg_completion_time(self) -> float:
        stats = self.db.get_statistics()
        return stats.get('avg_completion_days', 0.0)

    def get_problem_statistics(self) -> list:
        stats = self.db.get_statistics()
        return stats.get('problem_stats', [])

    def generate_report(self) -> str:
        report = "=" * 50 + "\n"
        report += "ОТЧЕТ ПО СТАТИСТИКЕ СЕРВИСНОГО ЦЕНТРА\n"
        report += "=" * 50 + "\n\n"

        completed = self.calculate_completed_count()
        report += f"Количество выполненных заявок: {completed}\n"

        avg_time = self.calculate_avg_completion_time()
        report += f"Среднее время выполнения заявки: {avg_time} дней\n\n"

        report += "Статистика по типам техники:\n"
        report += "-" * 30 + "\n"

        for stat in self.get_problem_statistics():
            report += f"{stat['type']}: {stat['total']} заявок "
            report += f"(выполнено: {stat['completed']})\n"

        report += "\n" + "=" * 50 + "\n"
        return report