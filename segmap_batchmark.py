import os
import subprocess
import datetime
import itertools
import configparser

result_dir = '/home/dongwonshin/Desktop/SLAM_eval/Experiment_Results'

target_kitti_data_list = [0,1,2,4,5,6,7,8,9,10]
icp_configs = ['semantic_icp', 'ordinary_icp']
odom_configs = ['with_odom', 'without_odom']

# TODO: benchmark start mark
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
start_dir = os.path.join(result_dir, timestamp)
os.mkdir(start_dir + ' [Batch Start]')

try:
    for target_kitti_data, icp_config, odom_config in itertools.product(target_kitti_data_list, icp_configs, odom_configs):
        # TODO: if the process not work well, then what should I do?
        subprocess.check_output('python segmap_benchmark.py \
                                --target_kitti_data %d \
                                --icp_config %s \
                                --odom_config %s ' % (target_kitti_data , icp_config, odom_config), shell=True)
except KeyboardInterrupt:
    print('----------------------KeyboardInterrupt----------------------')

# TODO: benchmark end mark
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
end_dir = os.path.join(result_dir, timestamp)
os.mkdir(end_dir + ' [Batch End]')