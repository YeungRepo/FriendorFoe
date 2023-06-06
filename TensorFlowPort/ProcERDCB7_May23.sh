#! /bin/bash


python3 DynamicFeatureAnalytics.py "/FoFData/ERDCBatch7/A549P1/" >> ERDCB3A549P1.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/ERDCBatch7/A549P2/" >> ERDCB3A549P2.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/ERDCBatch7/A549P3/" >> ERDCB3A549P3.txt &

python3 DynamicFeatureAnalytics.py "/FoFData/ERDCBatch7/A549P4/" >> ERDCB3A549P4.txt &


python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/ERDCBatch7/HCT116P1" >> ERDCB3HCT116P1.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/ERDCBatch7/HCT116P2" >> ERDCB3HCT116P2.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/ERDCBatch7/HCT116P3" >> ERDCB3HCT116P3.txt &

python3 DynamicFeatureAnalytics_HCT116.py "/FoFData/ERDCBatch7/HCT116P4" >> ERDCB3HCT116P4.txt &




