# Evaluate four indivdual tools and RDS

## Evaluate the four indivadual tools 

1. Download modified benchmark from our GitHub repository.

```
    git clone https://github.com/RaceDetectionService/dataracebench.git
```
2. Run DataRaceBen for each indivdual tools with command:

```
    cd dataracebench
    ./check-data-races.sh --archer
    ./check-data-races.sh --tsanclang
    ./check-data-races.sh --romp
    ./check-data-races.sh --inspector-max-resource
    or
    ./check-data-races.sh --newbench
```
Before you run this dataracebench, make sure you have correct tools installed on your computer. The instruction for install four tools can be found at [here](InstallTool.md).

3.Run DataRaceBen for RDS with command:
```
    cd dataracebench
    ./RDS.sh
```
Before you run this dataracebench, make sure you have correct RDS serve running somewhere. The instruction for deploy RDS can be found at [here](MetaserviceSetup.md).

4. Evaluate the result

After you run this dataracebench, you can find the result at results floder. There will be generated CSV files. You can manually put all result into one CSV file. In this project we put all results in to f-1.csv. Then run the metric.py to caculate the result. You can also use excel to caculate the result.
```
    cd dataracebench/result
    Python3 metric.py
```
Notice, you need change the file name to your CSV filename in line 5. You also need to change the column number in line 18 for your tools name and RDS with different policy. 
