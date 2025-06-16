import sys
import math
from EEToolsLib import EETools as tools

R1def = 10000
E12base = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

E24base = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
           3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

E48base = [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69,
           1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01,
           3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36,
           5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53]
options = {
    'E12': [round(base * (10 ** i),1) for i in range(7) for base in E12base]+[math.inf],
    'E24': [round(base * (10 ** i),1) for i in range(7) for base in E24base]+[math.inf],
    'E48': [round(base * (10 ** i),2) for i in range(7) for base in E48base]+[math.inf]
}

def main():
    if len(sys.argv) != 3:
        print('\n\nUsage: python ./RatioCalculator.py [ratio] [resistance series (E12/E24/E48)]\n\n')
        sys.exit(1)
    
    try:
        ratioTarget = float(sys.argv[1])
        series = sys.argv[2]
    except ValueError:
        print("Wrong input format")
        sys.exit(1)

    configs = []
    for i in range(len(options[series])):
        for j in range(len(options[series])):
            R1 = options[series][i]
            R2 = options[series][j]
            calRatio = R1/R2
            err = abs((calRatio-ratioTarget)/ratioTarget)
            configs.append([R1,R2,calRatio,err])
    configs.sort(key=lambda x:x[3])
    configs = configs[:10]

    for config in configs:
        print(f"R1={tools.Notation(config[0])}Ohms,\
              R2={tools.Notation(config[1])}Ohms,\
              Ratio={config[2]:.3f},\
              Error={round(config[3]*100,2)}%")

if __name__ == "__main__":
    main()