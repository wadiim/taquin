import matplotlib.pyplot as plt
import pandas as pd
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)
    
    stats_filename = sys.argv[1]

    # Read the stats file into a pandas DataFrame
    df = pd.read_csv(stats_filename, sep=' ', names=[
        'min_moves',
        'id',
        'algorithm',
        'params',
        'solution_length',
        'visited_states',
        'processed_states',
        'max_depth',
        'execution_time'
    ])

    # Calculate the arithmetic mean values for each algorithm and each heuristic (if applicable)
    grouped = df.groupby(['algorithm', 'params', 'min_moves']).mean()
    grouped_without_params = df.groupby(['algorithm', 'min_moves']).mean()

    criteria = ['solution_length', 'visited_states', 'processed_states', 'max_depth', 'execution_time']
    orders = ['drlu', 'drul', 'ludr', 'lurd', 'rdlu', 'rdul', 'uldr', 'ulrd']
    algorithms = ['bfs', 'dfs', 'astr']
    heuristics = ['hamm', 'manh']

    field_to_label_map = {
        'min_moves': 'Depth',
        'bfs': 'BFS',
        'dfs': 'DFS',
        'astr': 'A*',
        'hamm': 'Hamming',
        'manh': 'Manhattan',
        'solution_length': 'Average solution length',
        'visited_states': 'Average number of visited states',
        'processed_states': 'Average number of processed states',
        'max_depth': 'Average maximum recursion depth',
        'execution_time': 'Average execution time (ms)'
    }

    SMALL_SIZE = 10
    MEDIUM_SIZE = 12
    BIGGER_SIZE = 14

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    for c in criteria:
        # BFS, DFS, and A* combined
        plt.figure()
        plt.title('Total')
        plt.subplots_adjust(right=0.78)
        bar_width = 1 / 4
        for i, a in enumerate(algorithms):
            data = grouped_without_params.loc[(a, slice(None), slice(None)), c]
            plt.bar(data.index.get_level_values('min_moves') + i * bar_width - bar_width, data.values,
                    label=field_to_label_map[a], width=bar_width)
        plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left", borderaxespad=0)
        plt.xlabel(field_to_label_map['min_moves'])
        plt.ylabel(field_to_label_map[c])
        if c in ['visited_states', 'processed_states', 'execution_time']:
            plt.yscale('log')
            top_limit = 10 ** 4 if c == 'execution_time' else 10 ** 6
            plt.ylim(top=top_limit)
        if c in ['solution_length', 'max_depth']:
            plt.yticks([i for i in range(0, 22, 2)])

        # A*
        bar_width = 1 / 3
        plt.figure()
        plt.title('A*')
        plt.subplots_adjust(right=0.78)
        for i, heuristic in enumerate(heuristics):
            data = grouped.loc[('astr', heuristic, slice(None)), c]
            plt.bar(data.index.get_level_values('min_moves') + i * bar_width - 0.5 * bar_width, data.values,
                    label=field_to_label_map[heuristic], width=bar_width)
        plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left", borderaxespad=0)
        plt.xlabel(field_to_label_map['min_moves'])
        plt.ylabel(field_to_label_map[c])
        if c == 'visited_states':
            plt.yticks([i for i in range(0, 25, 2)])
        elif c == 'processed_states':
            plt.yticks([i for i in range(0, 10)])

        # BFS
        bar_width = 1 / 9
        plt.figure()
        plt.title('BFS')
        plt.subplots_adjust(right=0.78)
        for i, order in enumerate(orders):
            data = grouped.loc[('bfs', order, slice(None)), c]
            plt.bar(data.index.get_level_values('min_moves') + i * bar_width - 3.5 * bar_width, data.values,
                    label=order.upper(), width=bar_width)
        plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left", borderaxespad=0)
        plt.xlabel(field_to_label_map['min_moves'])
        plt.ylabel(field_to_label_map[c])
        if c in ['visited_states', 'processed_states', 'execution_time']:
            plt.yscale('log')
            if c != 'execution_time':
                plt.ylim(top=((10 ** 3) + 100))
        else:
            plt.yticks([i for i in range(0, 8)])
        
        # DFS
        bar_width = 1 / 9
        plt.figure()
        plt.title('DFS')
        plt.subplots_adjust(right=0.78)
        for i, order in enumerate(orders):
            data = grouped.loc[('dfs', order, slice(None)), c]
            plt.bar(data.index.get_level_values('min_moves') + i * bar_width - 3.5 * bar_width, data.values,
                    label=order.upper(), width=bar_width)
        plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left", borderaxespad=0)
        plt.xlabel(field_to_label_map['min_moves'])
        plt.ylabel(field_to_label_map[c])
        if c in ['visited_states', 'processed_states', 'execution_time']:
            plt.yscale('log')
            if c != 'execution_time':
                plt.ylim(top=((10 ** 6) + 100))
        else:
            plt.yticks([i for i in range(0, 22, 2)])

    plt.show()
