#Ion Propulsion system comparison tool
import tkinter as tk
root = tk.Tk()
root.title("Ion Propulsion Systems comparison")
root.configure(background='white')
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
frame1 = tk.Frame(root,bg='white',width=200, height =600)
frame1.grid(row=0,column=0 )
frame2 = tk.Frame(root,bg='#b2bec3',width=576, height =720)
frame2.grid(row=0,column=1)
frame3 = tk.Frame(root,bg='#636e72',width=576, height =720)
frame3.grid(row=0,column=2)
#DefineVariables
BM=tk.DoubleVar() #Base Mass = Structure + Payload + misc (essentially (Total - propulsion and Power)
DV=tk.DoubleVar() #Delta V
RT=tk.DoubleVar() #Watt/kg of RTG System
EL=tk.StringVar() #Engines information elsx file
OT=tk.DoubleVar() #Operating Temperature
MD=tk.DoubleVar() #Tank Material Density
YS=tk.DoubleVar() #Yield Strength of tank material
CP=tk.DoubleVar() #Critical Pressure of gas
CT=tk.DoubleVar() #Critical Temperature of gas
MM=tk.DoubleVar() #Molecular mass of gas
FS=tk.DoubleVar() #Factor of safety (tank)
#Hoping to add more in the future like Voltage, Current,etc

def basicdata():
      #Labels
      tk.Label(frame1,bg='white', text='Base Mass (Payload + Structure)').grid(row=0,column=0)
      tk.Label(frame1,bg='white', text='Delta V (km/s)').grid(row=2,column=0)
      tk.Label(frame1,bg='white', text='RTG Power (W) per Kg').grid(row=4,column=0)
      #DataEntry
      tk.Entry(frame1,textvariable=BM,width=30).grid(row=1, padx=2, pady=2)
      tk.Entry(frame1,textvariable=DV,width=30).grid(row=3, padx=2, pady=2)
      tk.Entry(frame1,textvariable=RT,width=30).grid(row=5, padx=2, pady=2)

#Engine List
tk.Label(frame1, text='EngineList.xlsx').grid(row=6,column=0)
tk.Entry(frame1,textvariable=EL,width=30).grid(row=7, padx=2, pady=2)

def tanksize():
      #Labels
      frame3 = tk.Frame(frame1, bg="white")
      frame3.grid(row=10,column=0)
      tk.Label(frame3,bg='white', text='Tank Sizing (spherical)___________ ').grid(row=0,column=0)
      tk.Label(frame3,bg='white', text='Operating Temperature').grid(row=1,column=0)
      tk.Label(frame3,bg='white', text='Material density kg/m3 (Ti = 4850)').grid(row=3,column=0)
      tk.Label(frame3,bg='white', text='Yield Strength Mpa (Ti = 140)').grid(row=5,column=0)
      tk.Label(frame3,bg='white', text='Critical Pressure of gas (kPa)\n (Xenon = 5838)').grid(row=7,column=0)
      tk.Label(frame3,bg='white', text='Critical Temperature of gas (K)\n (Xenon = 289.74)').grid(row=9,column=0)
      tk.Label(frame3,bg='white', text='Molecular Mass (Xenon = 132)').grid(row=11,column=0)
      tk.Label(frame3,bg='white', text='Factor of Safety').grid(row=13,column=0)
      #Data Entry
      tk.Entry(frame3,textvariable=OT).grid(row=2,column=0)
      tk.Entry(frame3,textvariable=MD).grid(row=4,column=0)
      tk.Entry(frame3,textvariable=YS).grid(row=6,column=0)
      tk.Entry(frame3,textvariable=CP).grid(row=8,column=0)
      tk.Entry(frame3,textvariable=CT).grid(row=10,column=0)
      tk.Entry(frame3,textvariable=MM).grid(row=12,column=0)
      tk.Entry(frame3,textvariable=FS).grid(row=14,column=0)

import pandas as pd
import math as m
class iteration(object):
      def __init__(self,BM,DV,RT,EL,tank_details):
            self.output=[['Engine','Thrust','Total Mass','Propellant Volume','Pressurizer Volume', 'Power Reqd']]
            self.output1=[]
            engine_file=EL+'.xlsx'
            #propellantfile=PL+'.xlsx'
            self.engine_data=pd.read_excel(engine_file,header=0)
            self.n=len(self.engine_data['Type'])
            self.powerWperKG=RT #RTG
            self.DV=DV*1000
            self.tank=tank_details
            self.BM=BM
            iteration.itera(self)
      def data(self,IterationNumber):
            it=IterationNumber
            ed=self.engine_data
            #Excel Data O
            self.Engine=ed.iloc[it,0]
            self.Type=ed.iloc[it,1]
            self.Propellant=ed.iloc[it,2].split('/')
            self.OF=float(ed.iloc[it,3])
            self.EngineMass=float(ed.iloc[it,4])
            self.InletPressure=float(ed.iloc[it,5])
            self.SpecificImpulse=float(ed.iloc[it,6])
            self.TotalImpulse=float(ed.iloc[it,7])
            self.TotalPulses=float(ed.iloc[it,8])
            self.MinImpulseBit=float(ed.iloc[it,9])
            self.SteadyStateFiringTime=float(ed.iloc[it,10])
            self.Thrust=float(ed.iloc[it,11])
            self.Powerreqd=float(ed.iloc[it,12])
            self.PropellantDensity=[]

      def itera(self):
            n=self.n
            dv=self.DV #m/s
            for i in range(0,n):
                        iteration.data(self,i)
                        iteration.calculate(self,dv)
            iteration.plotISP_Thrust(self)
            iteration.plotTotalMassvsEngine(self)

      def calculate(self,dv):
            engine=self.Engine
            thrust=self.Thrust #in Newtons
            Powerreqd=self.Powerreqd
            powermass=self.Powerreqd/self.powerWperKG
            v_ex=self.SpecificImpulse*9.81
            TotalMass=0
            TotalPropellantVolume=0
            TotalPressurizerVolume=0
            #Mass contributions in kg
            Mass_payload_and_structure=self.BM
            Mass_Engine=self.EngineMass
            TotalMass=Mass_payload_and_structure+Mass_Engine
            TotalMass+=(Powerreqd/self.powerWperKG)
            k=m.exp(dv/v_ex)-1
            thrust=self.Thrust

            #special cases
            if self.Engine=='NEXT':
                  TotalPropellantVolume+=0.11775

            #End of Special cases

            #Tank sizing calculations -
            #[OT,MD,YS,CP,CT,MM,FS]
            tank=self.tank
            T=tank[0] #K Operating Temperature
            pt=tank[1] #kg/m3 Material Density
            ys=tank[2]*1e6 #Mpa Yield Strength
            Tcr=tank[4] #K Critical Temperature
            Pcr=tank[3]*1e3 #kPa Critical Pressure
            M=tank[5] #Molecular mass
            R=8314 #J/kg-mol K Gas Constant
            a=R**2*Tcr**2.5/(9*(2**(1/3)-1)*Pcr) #Redlich-Kwong Parameter
            b=(2**(1/3)-1)*R*Tcr/(3*Pcr) #Redlich-Kwong Parameter
            pp=((4*R*T**1.5*b*M**2*a)**0.5-R*T**1.5*b*M-a*M)/(R*T**1.5*b**2-a*b) #propellant Density
            P=pp*((R*T/(M-b*pp))-(a*pp)/(M*(M+b*pp)*T**0.5)) #Tank Pressure
            TankPressure=P/1e6
            FOS=tank[-1] #Factor of Safety
            Mfu=TotalMass*k / (1 - ((1.5*P*pt*FOS)/(ys*pp))) #propellant Mass
            import math
            tankageFraction=(1.5*P*pt*FOS)/(ys*pp)  #i.e tank mass/propellant Mass
            tankmass=tankageFraction*Mfu
            TotalPropellantVolume+=Mfu/pp
            Thickness=(P*1000*FOS/(2*ys))*((3*TotalPropellantVolume)/(4*math.pi))**(1/3) #Tank Thickness
            TotalMass+=Mfu
            self.output.append([engine,self.SpecificImpulse,thrust,TotalMass,self.BM,Mfu,powermass,TotalPropellantVolume,Powerreqd,tankmass,Thickness,TankPressure,pp])
            self.output1.append([engine, thrust, TotalMass, (TotalPropellantVolume+ TotalPressurizerVolume), (Powerreqd)])

      import matplotlib.backends.tkagg as tkagg
      from matplotlib.backends.backend_agg import FigureCanvasAgg
      def plotISP_Thrust(self):
            import matplotlib.pyplot as plt
            fig1,ax=plt.subplots(figsize=(8,10))
            plt.rcParams['font.size']=12
            ISP=[]
            Thrust=[]
            for i in range (0,self.n):
                  ISP.append(float(self.engine_data.iloc[i,6]))
                  Thrust.append(float(self.engine_data.iloc[i,11]))
                  plt.annotate(self.engine_data.iloc[i,0],xy=(float(self.engine_data.iloc[i,11])+0.01,float(self.engine_data.iloc[i,6])-50),)
            #plt.loglog(basex=10,basey=10)
            plt.xlabel('Thrust (N)')
            plt.ylabel('ISP (s)')
            plt.title('ISP vs Thrust')
            plt.grid(True)
            plt.scatter(Thrust,ISP,marker='o',cmap=plt.get_cmap('Spectral'))
            plt.savefig("ISP VS Thrust.png")
            ISP = tk.PhotoImage(file='ISP VS Thrust.png')
            ISP_label = tk.Label(frame2, image=ISP)
            ISP_label.image = ISP
            ISP_label.grid(row=0,column=0)
      def plotTotalMassvsEngine(self):
            IsNegative=False
            import matplotlib.pyplot as plt
            fig2,ax=plt.subplots(figsize=(8,10))
            Thrust=[]
            TotalMass=[]
            plt.rcParams['font.size']=12
            for i in range (0,self.n):
                  Thrust.append(float(self.engine_data.iloc[i,11]))
                  TotalMass.append(float(self.output1[i][2]))
                  plt.annotate(self.engine_data.iloc[i,0],xy=(float(self.engine_data.iloc[i,11])+0.004,float(self.output1[i][2])))
            plt.xlabel('Thrust (N)')
            plt.ylabel('Total Mass (kg)')
            plt.title('Total Mass (structure + power + fuel) VS Thrust')

            #_____Slight Digression _________LOG________________________________________________________
            #Make Log
            #[engine,self.SpecificImpulse,thrust,TotalMass,self.BM,Mfu,powermass,TotalPropellantVolume,Powerreqd,tankmass,Thickness,TankPressure, pp]
            log=[]
            for i in range(1,self.n+1):
                  #Check for Negative numbers (caused by very high input values)
                  if(self.output[i][1]<0 or self.output[i][2]<0 or self.output[i][3]<0 or self.output[i][4]<0 or self.output[i][5]<0 or self.output[i][6]<0 or self.output[i][7]<0 or self.output[i][-1]<0 or self.output[i][-5]<0 or self.output[i][-3]<0 or self.output[i][-2]<0 or self.output[i][9]<0):
                        IsNegative=True

                  if IsNegative==True:
                        plt.title("Wrong output. Some values negative.\n Reduce input values to a resonable number")
                        break
                  #___Check Complete
                  log.append("______________________________________\n")
                  log.append("Engine:............|"+str(self.output[i][0])+"\n")
                  log.append("ISP:...............|"+str(round(self.output[i][1],3))+"s\n")
                  log.append("Thrust:............|"+str(round(self.output[i][2],3))+"N\n")
                  log.append("Total Mass:........|"+str(round(self.output[i][3],3))+"kg\n")
                  log.append("--Base Mass:.......|"+str(round(self.output[i][4],3))+"kg\n")
                  log.append("--Propellant Mass:.|"+str(round(self.output[i][5],3))+"kg\n")
                  log.append("--Power Mass:......|"+str(round(self.output[i][6],3))+"kg\n")
                  log.append("--Tank Mass:.......|"+str(round(self.output[i][9],3))+"kg\n")
                  log.append("Propellant Volume:.|"+str(round(self.output[i][7],3))+"m^3\n")
                  log.append("Propellant Density:|"+str(round(self.output[i][-1],3))+"kg/m^3\n")
                  log.append("Power Requirement:.|"+str(round(self.output[i][-5],3))+"W\n")
                  log.append("Tank Thickness:....|"+str(round(self.output[i][-3],3))+"mm\n")
                  log.append("Tank Pressure:.....|"+str(round(self.output[i][-2],3))+"MPa\n")

            #Make Log File
            with open ("Log.txt",'w+') as file:
                  for i in log:
                        file.write(i)
                  file.close()
            #_________________________________________________________________________________
            plt.grid(True)
            plt.scatter(Thrust, TotalMass)
            plt.savefig("Total Mass (structure + power + fuel) VS Thrust.png")
            mass = tk.PhotoImage(file='Total Mass (structure + power + fuel) VS Thrust.png')
            mass_label = tk.Label(frame3, image=mass)
            mass_label.image = mass
            mass_label.grid(row=0,column=0)

def event(event):
      #Get values - BM,DV,RT,EL,PL,[OT,MD,YS,CP,CT,MM,FS]
      #iteration(BM.get(),DV.get(),RT.get(),EL.get(),[OT.get(),MD.get(),YS.get(),CP.get(),CT.get(),MM.get(),FS.get()])
      iteration(450,7,2.5,"ED",[300,4678,140,5768,289.74,132,2.5]) #testing purposes


button =tk.Button(frame1, text="Plot") #create button
button.grid(row=11,column=0)
button.bind("<Button-1>", event)  #bind button to mouse click

basicdata()
tanksize()
root.mainloop()