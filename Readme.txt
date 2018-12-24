# Ion-Propulsion-system-comparison-tool

The python code has the following dependencies - 
1) tkinter
2) pandas
3) matplotlib
Note: Make sure you have the Engine list in the same folder as the code. The Log and the graphs would be saved in the same folder. 
Please run through a compiler like 'spyder'

The "Ion Propulsion system comparison tool" takes in the following user inputs -

1)  Base Mass ( = Structure+Payload i.e. everything besides the power and the propulsion
subsystem (= Propellant mass + Tank mass)
2)  Delta-V
3)  Specific power of RTG (Radioisotope thermoelectric generator) in W/kg
4)  List of Engines in .elsx format (Sample included (sourced from manufacturer websites) in the repository) 
    Engine List should have the following information (in the same order as in the sample)
    4.1) Engine Name
    4.2) Engine Mass
    4.2) ISP
    4.3) Thrust
    4.4) Power Requirement
5)  Operating Temperature of propellant 
6)  Tank Material Density
7)  Yield Strength of tank material
8)  Critical Pressure of gas
9)  Critical Temperature of gas
10) Molecular mass of gas
11) Factor of safety (tank)
Note: The code does not take voltage and current into account

And then calculates - 
1) Total Mass of spacecraft
2) Propellant Volume
3) Propellant Density
4) Tank wall thickness
5) Tank Pressure

Apart from display in the UI (made using Tkinter) a 'Log' is also generated
Sample 'Log' output - 
Engine:............|Qinetiq T6 (1kw)
ISP:...............|4500.0s
Thrust:............|0.039N
Total Mass:........|1482.206kg
--Base Mass:.......|450kg
--Propellant Mass:.|623.906kg
--Power Mass:......|400.0kg
--Tank Mass:.......|476.423kg
Propellant Volume:.|0.465m^3
Propellant Density:|1342.098kg/m^3
Power Requirement:.|1000.0W
Tank Thickness:....|35.093mm
Tank Pressure:.....|8.179MPa
