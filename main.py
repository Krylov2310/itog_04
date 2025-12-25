import platform
from collector import *


base_dir = 'base/'
base_name = 'market'
format_scv = '.csv'
format_json = '.json'
defoliate_base_csv = f'{base_dir}{base_name}{format_scv}'
defoliate_base_json = f'{base_dir}{base_name}{format_json}'
fieldnames = ['name', 'x', 'y', 'weight', 'notes']


def get_file_dir():
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    if not os.path.exists(defoliate_base_csv):
        with open(defoliate_base_csv, 'w', encoding='utf-8'):
            pass
    if not os.path.exists(defoliate_base_json):
        with open(defoliate_base_json, 'w', encoding='utf-8'):
            pass


def info(dz, name):
    print(f'\033[33m{dz}\n"{name}"\nСтудент Крылов Эдуард Васильевич\n'
          f'Дата: 25.12.2025г.\033[0m\n')


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def main():
    # global weight_type
    collector = DataCollector()
    print('\033[34mСистема сбора данных о пунктах доставки\033[0m\n')
    while True:
        print('=' * 25)
        print('\033[34mМеню:\033[0m')
        print('=' * 25)
        print('1. Добавить пункт вручную')
        print('2. Загрузить из (CSV/JSON)')
        print('3. Удалить пункт')
        print('4. Показать все пункты')
        print('5. Рассчитать расстояние между пунктами')
        print('6. Показать граф (узлы и рёбра)')
        print('7. Визуализировать сеть на графике')
        print('8. Найти кратчайший путь (Дейкстра)')
        print('9. Сохранить в (CSV/JSON)')
        print('\033[31m0. Выход\033[0m')
        print('=' * 25)

        choice = input('\033[33mВыберите действие (0–9): \033[0m').strip()

        no_format = 'Без расширения'
        clear_screen()

        if choice == '1':
            collector.add_point_manually()
        elif choice == '2':
            print(f'Если "Enter" то {defoliate_base_csv}')
            inp_format = input('1 - CSV, 2 - JSON: ').strip()
            print('=' * 25)
            if not inp_format:
                filepath = defoliate_base_csv
                collector.load_from_csv(filepath)
            elif inp_format == '1':
                print(no_format)
                filepath = input('Имя CSV‑файла: ').strip()
                print('=' * 25)
                if not filepath:
                    filepath = defoliate_base_csv
                else:
                    filepath = base_dir + filepath + format_scv
                collector.load_from_csv(filepath)
            else:
                print(no_format)
                filepath = input('Имя JSON‑файла: ').strip()
                print('=' * 25)
                if not filepath:
                    filepath = defoliate_base_json
                else:
                    filepath = base_dir + filepath + format_json
                collector.load_from_json(filepath)

        elif choice == '3':
            name = input('Название пункта для удаления: ').strip()
            collector.remove_node(name)

        elif choice == '4':
            collector.show_points()

        elif choice == '5':
            collector.update_graph(speed_kmh=60.0, cost_per_km=15.0)
            name1 = input('Название первого пункта: ').strip()
            name2 = input('Название второго пункта: ').strip()
            dist = collector.calculate_distance_between(name1, name2)
            if dist is not None:
                print(f'Расстояние между "{name1}" и "{name2}": {dist:.2f} км\n')

        elif choice == '6':
            collector.update_graph(speed_kmh=60.0, cost_per_km=15.0)
            if not collector.graph.nodes:
                print('\033[31mГраф пуст!\033[0m\n')
            else:
                print('\033[33mУзлы графа:\033[0m')
                for name in collector.graph.nodes:
                    print(f"  {name}")
                print('\033[33mРёбра (u → v: расстояние, время, стоимость):\033[0m')
                for (u, v), weights in collector.graph.edges.items():
                    print(f'  {u} → {v}: {weights['distance']:.2f} км, '
                          f'{weights["time"]:.2f} ч, {weights["cost"]:.2f} руб.')
                print()

        elif choice == '7':
            collector.update_graph(speed_kmh=60.0, cost_per_km=15.0)
            collector.plot_network()

        elif choice == '8':
            collector.update_graph(speed_kmh=60.0, cost_per_km=15.0)
            type_list = ['distance', 'time', 'cost']
            start = input('Начальный пункт: ').strip()
            end = input('Конечный пункт: ').strip()
            print('Если "Enter" — "distance"')
            weight_type = input('Параметр для оптимизации (1 - distance), (2 - time), (3 - cost): ').strip().lower()
            if not weight_type or int(weight_type) > 3:
                weight_type = 1
            weight_type = type_list[int(weight_type) - 1]
            result = collector.find_shortest_path(start, end, weight_type)
            if result:
                path, total = result
                print('\033[32m=\033[0m' * 30)
                print(f'\033[32mКратчайший путь: {" → ".join(path)}\033[0m')
                print(f'\033[32mОбщая {weight_type}: {total:.2f}\033[0m\n')

        elif choice == '9':
            print(f'Если "Enter" — сохранить в {defoliate_base_csv} и {defoliate_base_json}')
            inp_format = input('1 — CSV, 2 — JSON, 3 — оба: ').strip()
            print('=' * 25)
            if not inp_format:
                collector.save_to_csv(defoliate_base_csv)
                collector.save_to_json(defoliate_base_json)
            elif inp_format == '1':
                filepath = input('Имя CSV‑файла: ').strip()
                if not filepath:
                    filepath = defoliate_base_csv
                else:
                    filepath = base_dir + filepath + format_scv
                collector.save_to_csv(filepath)
            elif inp_format == '2':
                filepath = input('Имя JSON‑файла: ').strip()
                if not filepath:
                    filepath = defoliate_base_json
                else:
                    filepath = base_dir + filepath + format_json
                collector.save_to_json(filepath)
            elif inp_format == '3':
                filepath = input('Имя файла: ').strip()
                if not filepath:
                    collector.save_to_csv(defoliate_base_csv)
                    collector.save_to_json(defoliate_base_json)
                else:
                    filepath_c = base_dir + filepath + format_scv
                    filepath_j = base_dir + filepath + format_json
                    collector.save_to_csv(filepath_c)
                    collector.save_to_json(filepath_j)
            else:
                print('\033[31mНеверный выбор!\033[0m\n')
        elif choice == '0':
            print('\033[33mДо свидания!\033[0m')
            break
        else:
            print('\033[31mНеверное действие!\nПопробуйте ещё раз.\033[0m\n')


if __name__ == '__main__':
    clear_screen()
    get_file_dir()
    info('Итоговый практикум 4', 'Оптимизация маршрута доставки')
    main()
