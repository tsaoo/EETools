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

def CalculateVout(R1, R2, R3, vfb):
    if R2 == math.inf:
        R23 = R3
    elif R3 == math.inf:
        R23 = R2
    else:
        R23 = (R2*R3)/(R2+R3)
    vout = vfb*(R1+R23)/(R23)
    return vout

def main():
    if len(sys.argv) != 4:
        print('\n\nUsage: python ./FeedbackDivider.py [output voltage] [feedback voltage] [resistance series (E12/E24/E48)]\n\n')
        sys.exit(1)
    
    try:
        vtarget = float(sys.argv[1])
        vfb = float(sys.argv[2])
        series = sys.argv[3]
    except ValueError:
        print("Wrong input format")
        sys.exit(1)

    print(' ===============================================================')
    print(f'|   {vtarget:.2f}V ---------( R1 )--\t---+-----( R2 )-----+--- Gnd\t|')
    print('|                           \t   |                |      \t|')
    print('|                           \t   +-----( R3 )-----+      \t|')
    print('|                           \t   |                       \t|')
    print(f'|                           \t   +----- {vfb:.2f}V           \t|')
    print(' ===============================================================')

    configs = []
    for i in range(len(options[series])):
        for j in range(i,len(options[series])):
            R2 = options[series][i]
            R3 = options[series][j]
            vout = CalculateVout(R1def, R2, R3, vfb)
            err = abs((vout-vtarget)/vtarget)
            configs.append([R2,R3,vout,err])
    configs.sort(key=lambda x:x[3])
    configs = configs[:10]

    extraConfigs = []
    for R2 in options[series]:
        vout = CalculateVout(R1def, R2, math.inf, vfb)
        err = abs((vout-vtarget)/vtarget)
        extraConfigs.append([R2,math.inf,vout,err])
    extraConfigs.sort(key=lambda x:x[3])
    configs = [extraConfigs[0]]+configs

    for config in configs:
        print(f"R1={tools.Notation(R1def)}Ohms,\
              R2={tools.Notation(config[0])}Ohms,\
              R3={tools.Notation(config[1])}Ohms,\
              Vout={config[2]:.3f}V,\
              Error={round(config[3]*100,2)}%")

if __name__ == "__main__":
    main()