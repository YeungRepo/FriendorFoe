#! /bin/bash


python3 DynamicFeatureAnalytics.py "/FoFData/20220428_IVV/P1_A549ERKFRA1/"  >> 20220428_P1_A549ERKFRA1.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/20220428_IVV/P2_A549ERKFRA1/"  >> 20220428_P2_A549ERKFRA1.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220428_IVV/P1_HCT116ERKFRA1/"  >> 20220428_P1_HCT116ERKFRA1.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220428_IVV/P2_HCT116ERKFRA1/"  >> 20220428_P2_HCT116ERKFRA1.txt &







