#! /bin/bash


python3 DynamicFeatureAnalytics.py "/FoFData/20220518_ERDC/P1_A549ERKFRA1/"  >> 20220518_P1_A549ERKFRA1.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/20220518_ERDC/P2_A549ERKFRA1/"  >> 20220518_P2_A549ERKFRA1.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/20220518_ERDC/P3_A549ERKFRA1/"  >> 20220518_P3_A549ERKFRA1.txt &


python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220518_ERDC/P1_HCT116ERKFRA1/"  >> 20220518_P1_HCT116ERKFRA1.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220518_ERDC/P2_HCT116ERKFRA1/"  >> 20220518_P2_HCT116ERKFRA1.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220518_ERDC/P3_HCT116ERKFRA1/"  >> 20220518_P3_HCT116ERKFRA1.txt &









