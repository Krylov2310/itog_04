import json
import csv
import os

import matplotlib.pyplot as plt
import heapq
from typing import List, Dict, Tuple, Optional

from graph import DeliveryGraph
from main import get_file_dir, defoliate_base_csv, fieldnames, defoliate_base_json
from point import DeliveryPoint


class DataCollector:
    def __init__(self):
        self.points: List[DeliveryPoint] = []
        self.graph = DeliveryGraph()

    def add_point_manually(self) -> None:
        print("\n--- Ввод пункта доставки вручную ---")
        try:
            name = input('Название пункта: ').strip()
            if not name:
                print('\033[31mОшибка: название не может быть пустым!\033[0m')
                return
            x = float(input('Координата X: '))
            y = float(input('Координата Y: '))
            weight = float(input('Вес груза (кг, по умолчанию 0): ') or 0)
            notes = input('Примечание: ').strip()
            point = DeliveryPoint(name, x, y, weight, notes)
            self.points.append(point)
            print(f'Пункт "{name}" добавлен успешно!\n')
        except ValueError as e:
            print(f'Ошибка ввода: {e}. Пожалуйста, введите числа для координат и веса.\n')

    def load_from_csv(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            get_file_dir()
            print(f'Ошибка: файл {filepath} не найден.\nПоиск файла по умолчанию: {defoliate_base_csv}')
            filepath = defoliate_base_csv
            self.load_from_csv(filepath)
            return
        try:
            with open(filepath, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row: Dict[str, str]  # Явная подсказка типа
                    try:
                        point = DeliveryPoint(
                            name=str(row[fieldnames[0]]),
                            x=float(row[fieldnames[1]]),
                            y=float(row[fieldnames[2]]),
                            weight=float(row.get(fieldnames[3], 0)),
                            notes=row.get(fieldnames[4], '')
                        )
                        self.points.append(point)
                    except (KeyError, ValueError) as e:
                        print(
                            f'\033[31mОшибка в строке {reader.line_num}: \033[0m{e}\033[31m. Пропускаем строку!\033[0m')
            print(f'\033[32mЗагружено \033[0m{len(self.points)} \033[32mпунктов из \033[0m{filepath}\033[0m\n')
        except Exception as e:
            print(f'\033[31mОшибка при чтении CSV: \033[0m{e}\n')

    def load_from_json(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            get_file_dir()
            print(f'\033[31mОшибка: файл \033[0m{filepath} \033[31mне найден.\n'
                  f'Поиск файла по умолчанию: \033[0m{defoliate_base_json}')
            filepath = defoliate_base_json
            self.load_from_json(filepath)
            return
        try:
            with open(filepath, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    try:
                        point = DeliveryPoint(
                            name=item[fieldnames[0]],
                            x=float(item[fieldnames[1]]),
                            y=float(item[fieldnames[2]]),
                            weight=float(item.get(fieldnames[3], 0)),
                            notes=item.get(fieldnames[4], '')
                        )
                        self.points.append(point)
                    except (KeyError, ValueError) as e:
                        print(f'\033[31mОшибка в элементе: \033[0m{e}\033[31m. Пропускаем элемент!\033[0m')
            print(f'\033[32mЗагружено \033[0m{len(self.points)} \033[32mпунктов из \033[0m{filepath}.\n')
        except json.JSONDecodeError as e:
            print(f'\033[31mОшибка JSON: \033[0m{e}\n')
        except Exception as e:
            print(f'\033[31mОшибка при чтении JSON: \033[0m{e}\n')

    def show_points(self) -> None:
        if not self.points:
            print('\033[31mНет данных о пунктах доставки!\033[0m\n')
            return
        print('\n\033[33m--- Список пунктов доставки ---\033[0m')
        for i, point in enumerate(self.points, 1):
            print(f'{i}. {point}')
        print()

    def save_to_csv(self, filepath: str) -> None:
        try:
            with open(filepath, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for point in self.points:
                    writer.writerow(point.to_dict())
            print(f'\033[32mДанные сохранены в \033[0m{filepath}.\n')
        except Exception as e:
            print(f'\033[31mОшибка при сохранении в CSV: \033[0m{e}\n')

    def save_to_json(self, filepath: str) -> None:
        try:
            data = [point.to_dict() for point in self.points]
            with open(filepath, mode='w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            print(f'\033[32mДанные сохранены в \033[0m{filepath}.\n')
        except Exception as e:
            print(f'\033[31mОшибка при сохранении в JSON: \033[0m{e}\n')

    def remove_node(self, name: str) -> None:
        idx = None
        for i, point in enumerate(self.points):
            if point.name == name:
                idx = i
                break
        if idx is None:
            print(f'\033[31mПункт "{name}" не найден!\033[0m\n')
            return
        removed_point = self.points.pop(idx)
        print(f'\033[32mПункт "{removed_point.name}" удалён!\033[0m\n')
        if name in self.graph.nodes:
            del self.graph.nodes[name]
            for key in list(self.graph.edges.keys()):
                if name in key:
                    del self.graph.edges[key]

    def update_graph(self, speed_kmh: float = 60.0, cost_per_km: float = 15.0):
        self.graph = DeliveryGraph()
        for point in self.points:
            self.graph.add_node(point)
        self.graph.build_edges(speed_kmh, cost_per_km)
        print(f'\033[32mГраф обновлён: {len(self.points)} узлов, {len(self.graph.edges)} рёбер.\033[0m\n')

    def calculate_distance_between(self, name1: str, name2: str) -> Optional[float]:
        p1 = next((p for p in self.points if p.name == name1), None)
        p2 = next((p for p in self.points if p.name == name2), None)
        if not p1 or not p2:
            print('\033[31mОдин из пунктов не найден!\033[0m')
            return None
        return self.graph.calculate_distance(p1, p2)

    def plot_network(self):
        if not self.graph.nodes:
            print('\033[31mГраф пуст, ничего не отобразить!\033[0m\n')
            return
        plt.figure(figsize=(10, 8))
        plt.title('Сеть доставки: пункты и связи', fontsize=16)
        xs = [p.x for p in self.graph.nodes.values()]
        ys = [p.y for p in self.graph.nodes.values()]
        names = [p.name for p in self.graph.nodes.values()]
        plt.scatter(xs, ys, s=100, c='blue', alpha=0.7, zorder=5)
        for i, name in enumerate(names):
            plt.annotate(name, (xs[i], ys[i]), textcoords='offset points',
                         xytext=(0, 10), ha='center', fontsize=10)
        drawn_edges = set()
        for (u, v), weights in self.graph.edges.items():
            if (u, v) in drawn_edges or (v, u) in drawn_edges:
                continue
            drawn_edges.add((u, v))
            p1 = self.graph.nodes[u]
            p2 = self.graph.nodes[v]
            plt.plot([p1.x, p2.x], [p1.y, p2.y], 'gray', alpha=0.5, linewidth=1)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def find_shortest_path(self, start: str, end: str, weight_type: str) -> Optional[Tuple[List[str], float]]:
        if start not in self.graph.nodes or end not in self.graph.nodes:
            print("\033[31mОдин из пунктов не найден!\033[0m")
            return None
        distances = {name: float('inf') for name in self.graph.nodes}
        # previous = {name: None for name in self.graph.nodes}
        previous: Dict[str, Optional[str]] = {name: None for name in self.graph.nodes}
        distances[start] = 0
        pq = [(0.0, start)]
        while pq:
            current_dist, current = heapq.heappop(pq)
            if current == end:
                break
            if current_dist > distances[current]:
                continue
            for neighbor in self.graph.nodes:
                if (current, neighbor) not in self.graph.edges:
                    continue
                weight = self.graph.get_edge(current, neighbor, weight_type)
                if weight is None:
                    continue
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        if path[0] != start:
            print(f"\033[31mПуть от {start} до {end} не найден!\033[0m")
            return None
        return path, distances[end]
