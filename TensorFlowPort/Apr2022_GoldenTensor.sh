#! /bin/bash


python3 DynamicFeatureAnalytics.py "/FoFData/20220414_Handoff/P1_A549ERKFRA1/"  >> 20220414_P1_A549ERKFRA1.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/20220414_Handoff/P2_A549ERKFRA1/"  >> 20220414_P2_A549ERKFRA1.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/20220414_Handoff/P3_A549ERKFRA1/"  >> 20220414_P2_A549ERKFRA1.txt & 

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220414_Handoff/P1_HCT116ERKFRA1/"  >> 20220414_P1_HCT116ERKFRA1.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220414_Handoff/P2_HCT116ERKFRA1/"  >> 20220414_P2_HCT116ERKFRA1.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220414_Handoff/P3_HCT116ERKFRA1/"  >> 20220414_P3_HCT116ERKFRA1.txt & 





