import os
from glob import glob
from pandas import DataFrame
import configparser
import subprocess as sp

bench_start = '2018-11-07_12:05:48'
bench_end = '2018-11-07_12:14:30'

all_benchmarks = sorted(glob('/home/dongwonshin/Desktop/SLAM_eval/Experiment_Results/*'))

# benchmark filtereing
filtered_benchmarks = []
for benchmark in all_benchmarks:
    if (bench_start <= benchmark.split('/')[-1] and benchmark.split('/')[-1] <= bench_end):
        filtered_benchmarks.append(benchmark)

df = DataFrame()
for benchmark in filtered_benchmarks:
    config = configparser.ConfigParser()
    config.read(os.path.join(benchmark, 'POI.ini'))
    target_kitti_data = config.get('PARAMETERS','target_kitti_data')
    icp_config = config.get('PARAMETERS','icp_config')
    odom_config = config.get('PARAMETERS','odom_config')

    df = df.append({"benchmark_path": benchmark.split('/')[-1],
                    "target_kitti_data": target_kitti_data, 
                    "icp_config": icp_config, 
                    "odom_config" : odom_config}, ignore_index = True)

target_benchmarks = df.loc[df['target_kitti_data']==str(4)]
print(target_benchmarks)

result_files = ""
for index, row in target_benchmarks.iterrows():
    result_files += os.path.join('\"Experiment_Results',row['benchmark_path'],'rpe_eval/rpe_results.zip\"') + " "

for eval_type in ['ape', 'rpe']:
    os.system('evo_res %s --save_table %s_table.csv --save_plot %s_plot.pdf --use_filenames --no_warnings --silent' % (result_files, eval_type, eval_type))

