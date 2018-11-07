import os 
import fileinput
import datetime
import shutil
import argparse
import subprocess
import configparser

icp_config_file_list = {
    'semantic_icp':'/home/dongwonshin/segmap_ws/src/segmap/segmapper/launch/kitti/icp_dynamic_outdoor_labeled.yaml',
    'ordinary_icp':'/home/dongwonshin/segmap_ws/src/segmap/segmapper/launch/kitti/icp_dynamic_outdoor.yaml'
}

odom_config_file_list = {
    'with_odom':'/home/dongwonshin/segmap_ws/src/segmap/segmapper/launch/kitti/cnn_kitti_loop_closure_labeled_odom.yaml',
    'without_odom':'/home/dongwonshin/segmap_ws/src/segmap/segmapper/launch/kitti/cnn_kitti_loop_closure_labeled.yaml'
}

parser = argparse.ArgumentParser()
parser.add_argument("--target_kitti_data", type=int)
parser.add_argument("--icp_config", type=str)
parser.add_argument("--odom_config", type=str)
args = parser.parse_args()

target_kitti_data = args.target_kitti_data
icp_config_file = icp_config_file_list[args.icp_config]
odom_config_file = odom_config_file_list[args.odom_config]

# fixed
kitti_odom_bag = [
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_10_03_drive_0027.bag",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_10_03_drive_0042.bag", 
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_10_03_drive_0034.bag",
    "not_exist",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_09_30_drive_0016.bag",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_09_30_drive_0018.bag",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_09_30_drive_0020.bag",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_09_30_drive_0027.bag",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_09_30_drive_0028.bag",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_09_30_drive_0033.bag",
    "/home/dongwonshin/Desktop/KITTI_odometry_dataset/2011_09_30_drive_0034.bag",
]
template_launch_filename = '/home/dongwonshin/segmap_ws/src/segmap/segmapper/launch/kitti/kitti_odometry_test_template.launch'
generated_launch_filename = '/home/dongwonshin/segmap_ws/src/segmap/segmapper/launch/kitti/kitti_odometry_test.launch'
text_bag_file = kitti_odom_bag[target_kitti_data]

# launch file generation
with fileinput.FileInput(template_launch_filename, inplace=False, backup='.bak') as file:
    with open(generated_launch_filename,'wt') as outfile:
        for line in file:
            if (line.find('$bag_file$')>=0):
                outfile.write(line.replace('$bag_file$', text_bag_file))
                continue
            if (line.find('$icp_config$')>=0):
                outfile.write(line.replace('$icp_config$', icp_config_file))
                continue
            if (line.find('$odom_config$')>=0):
                outfile.write(line.replace('$odom_config$', odom_config_file))
                continue
            
            outfile.write(line)
            
# run experiments
# TODO: if the process not work well, then what should I do?
# os.system('catkin build segmapper && roslaunch segmapper kitti_odometry_test.launch')
try:
    subprocess.check_output('roslaunch segmapper kitti_odometry_test.launch', shell=True)
except KeyboardInterrupt:
    print('----------------------KeyboardInterrupt----------------------')
    exit()


# run eval
traj_file = '/tmp/trajectory.csv'
result_dir = '/home/dongwonshin/Desktop/SLAM_eval/Experiment_Results'
gt_file = '/home/dongwonshin/Desktop/KITTI_odometry_dataset/poses/%02d_time.txt' % target_kitti_data

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
result_dir = os.path.join(result_dir, timestamp)
os.mkdir(result_dir)
os.mkdir(os.path.join(result_dir,'ape_eval'))
os.mkdir(os.path.join(result_dir,'rpe_eval'))

print(timestamp)

shutil.copy(generated_launch_filename, result_dir)
shutil.copy(traj_file, result_dir)
shutil.copy(odom_config_file, result_dir)
shutil.copy(icp_config_file, result_dir)

os.system('evo_ape tum "%s" "%s/trajectory.csv" -va --plot_mode xz \
            --save_results %s/ape_eval/ape_results.zip \
            --save_plot %s/ape_eval/ape_plot.pdf > %s/ape_eval/ape_log.txt' \
            % (gt_file, result_dir, result_dir, result_dir, result_dir))
os.system('evo_rpe tum "%s" "%s/trajectory.csv" -va --plot_mode xz \
            --save_results %s/rpe_eval/rpe_results.zip --save_plot \
            %s/rpe_eval/rpe_plot.pdf > %s/rpe_eval/rpe_log.txt' \
            % (gt_file, result_dir, result_dir, result_dir, result_dir))

# Parameter of Ineterests
POI = configparser.ConfigParser()

POI['PARAMETERS'] = {}
POI['PARAMETERS']['target_kitti_data'] = str(args.target_kitti_data)
POI['PARAMETERS']['icp_config'] = str(args.icp_config)
POI['PARAMETERS']['odom_config'] = str(args.odom_config)

POI_file = os.path.join(result_dir,'POI.ini')
with open(POI_file,'w') as configfile:  # Parameters of Interests
    POI.write(configfile)