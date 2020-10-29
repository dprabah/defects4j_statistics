import numpy as np
import matplotlib.pyplot as plt
import csv
from pyaml import print

from util import get_project_root, read_config

results_folder = '/Probabilistic_coupling/results'
project_config = read_config(['../project_details.properties'])


def visualize_as_box_plot():
    font = {'size': 20}

    plt.rc('font', **font)
    project_list = project_config.get('projects', 'project_list').split(",")

    # if len(project_list) > 1:
    #     print("reduce number of projects to 1")
    #     exit(0)
    project_list = project_list[0]

    statement_coverage_r = []
    checked_coverage_r = []

    file_name = "/point_biserial_correlation__full" + ".csv"
    path = str(get_project_root()) + results_folder + file_name

    try:
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                statement_coverage_r.append(float(row['adequacy_based_tests_statement']))
                checked_coverage_r.append(float(row['adequacy_based_tests_checked']))
    except FileNotFoundError:
        pass

    data_to_plot = [statement_coverage_r, checked_coverage_r]
    fig = plt.figure(1, figsize=(9, 6))

    ax = fig.add_subplot()

    ax.set_ylabel('Probabilistic coupling')
    # ax.set_xlabel('Indicates whether or not, a bug detecting test is included in generated test suite')
    # ax.set_title(project_list)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(tuple(['Statement coverage', 'Checked coverage']))

    bp = ax.violinplot(data_to_plot, showmeans=True, showmedians=True)

    # loop over the paths of the mean lines
    xy = [[l.vertices[:, 0].mean(), l.vertices[0, 1]] for l in bp['cmeans'].get_paths()]
    xy = np.array(xy)

    ax.scatter(xy[:, 0], xy[:, 1], s=121, c="crimson", marker="x", zorder=3)

    # make lines invisible
    bp['cmeans'].set_visible(False)

    bp['bodies'][0].set(color='#e69138', linewidth=2)
    bp['bodies'][1].set(color='#3d85c6', linewidth=2)

    ax.legend().remove()
    plt.show()
    save_path = str(get_project_root()) + results_folder + '/' + str(project_list) + '_violin-plot'
    fig.savefig(save_path, dpi=100)


visualize_as_box_plot()

