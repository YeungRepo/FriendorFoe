#! /bin/bash


python3 DynamicFeatureAnalytics.py "/FoFData/20220224/P1_A549ErkFra1/"  >> 20220224P1_A549ErkFra.txt & 

python3 DynamicFeatureAnalytics.py "/FoFData/20220224/P2_A549ErkFra1/"  >> 20220224P2_A549ErkFra.txt & 

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220224/P1_HCT116ErkFra1/"  >> 20220224P1_HCT116ErkFra.txt & 

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/20220224/P2_HCT116ErkFra1/"  >> 20220224P2_HCT116ErkFra.txt & 


