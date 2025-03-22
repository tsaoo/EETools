# MCUFanout
Automatically fans out MCUs (STM32 only for now) according to external pin-out file.

## Usage
1. Starting from a CubeMX project, do Pinout->Export pinout without Alt. Functions

![](assets/MCUFanout_1.png)

2. Load EETools.PrjScr to your workspace.

![](assets/MCUFanout_2.png)

3. Run MCUFanout.pas, fill in pinout file path, fanout length and MCU type, click Run.

![](assets/MCUFanout_3.png)

4. Finished.
   
![](assets/MCUFanout_4.png)

