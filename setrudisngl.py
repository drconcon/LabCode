# Beispielmessung mit NGL202
# Kanal 1 = Quelle, Kanal 2 = Last
# Der Laststrom bleibt innerhalb einer Messreihe {UQ}, 
# durch geeignete Variation des Lastwiderstands RL, konstant. 

import visa
import time
rm = visa.ResourceManager()
RudisNGL = rm.open_resource('ASRL/dev/ttyACM0::INSTR')
print(RudisNGL.query('*IDN?'))
IL = float(raw_input())
while UQ!=0:
#Ausgang aus
	RudisNGL.write('OUTP:GEN 0')
#Parameter setzen
	UQ = float(raw_input())
	RL = UQ/IL
#Parametriert die Quelle mit Strombegrenzung auf kritischen Lastwert
	RudisNGL.write('INST:SEL 1') 
	RudisNGL.write('VOLT:ALIM 1')
	RudisNGL.write('VOLT:AMPL %s' % str(UQ))
	RudisNGL.write('CURR:AMPL 3')
#FTR an aus
#	RudisNGL.write('OUTP:FTR 1')
	RudisNGL.write('OUTP 1')
#Parametriert die Last
	RudisNGL.write('INST:SEL 2')
	RudisNGL.write('VOLT:ALIM 1')
	RudisNGL.write('VOLT:AMPL 0')
	RudisNGL.write('CURR:AMPL 3')
	RudisNGL.write('RES:AMPL %s' % str(RL))
	RudisNGL.write('RES:STAT 1')
	RudisNGL.write('OUTP 0')
#Ausgang an
	RudisNGL.write('OUTP:GEN 1')
#Nach 1 ms ist der lastfreie Ausgang sicher im Gleichgewicht
	time.sleep(0.001)
#Last an frei
	RudisNGL.write('INST:SEL 2')
	RudisNGL.write('OUTP 1')
	time.sleep(1)
else:
	print "Ende"

