#!/bin/bash

iter_s=1
iter_e=5

for iter in $(seq $iter_s $iter_e); do

    # 1. create folders
    mkdir /glade/work/yifanc/course/ERT574/VIC_sample_data/image/FindleyLake/spinup/$iter

    # 2. update configuration files
    config="iteration/global_param.FindleyLake.spinup.iter.$iter.txt"
    
    iter_pre=$((iter - 1))

    sed "s#ITER1PH#$iter_pre#g" global_param.FindleyLake.spinup.iter.temp.txt > $config
    sed -i "s#ITER2PH#$iter#g" $config

    # 3. run hydrologic models and save the log files
    /glade/work/yifanc/code/VIC/vic/drivers/image/vic_image.exe -g $config

done
