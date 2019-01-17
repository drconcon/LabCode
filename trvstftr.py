# Semi-Automatisierung mit dem DSO
# Messung der Einschaltzeit mit dem MSO 6 der Serie 6
import visa
import time
rm = visa.ResourceManager()
RudisNGL = rm.open_resource('ASRL/dev/ttyACM0::INSTR')
RudisMSO6 = rm.open_resource('TCPIP::172.16.32.128::INSTR')
print(RudisNGL.query('*IDN?'))
print(RudisMSO6.query('*IDN?'))
print(RudisMSO6.write('*RST'))
#FTR-Modus an oder aus
print("ftr")
ftr = float(raw_input())
f = open('tr_U.txt', 'wb')
UQ = 1
while UQ!=0:
# Ausgang aus
	RudisNGL.write('OUTP:GEN 0')
# Quellspannung setzen
	print("UQ")
	UQ = float(raw_input())
# MSO6 AKQ
# Einfaches Sampling
	RudisMSO6.write('ACQ:MOD SAM')
# Anzahl der aufgenommenen Sequenzen 
	RudisMSO6.write('ACQ:SEQ:NUMSEQ 1')
# Single Shot
	RudisMSO6.write('ACQ:STOPA SEQ')
# Aufzeichnung an 
	RudisMSO6.write('ACQ:STATE 1')
# Horizontale und vertikale Skala
	RudisMSO6.write('HOR:SCA 100e-6')
	RudisMSO6.write('CH1:SCA %s' % str(0.5*UQ))
# Triggerung
# Flankentrigger
	RudisMSO6.write('TRIG:A:EDGE:SOU CH1')
	RudisMSO6.write('TRIG:A:LEVEL:CH1 %s' % str(0.1*UQ))
	RudisMSO6.write('TRIG:TYPE EDGE')
	time.sleep(1)
# Messung parametrieren
# Risetime
	RudisMSO6.write('MEASU:ADDN MEAS1')
	RudisMSO6.write('MEASU:MEAS1:TYPE RISETIME')
	RudisMSO6.write('MEASU:MEAS1:SOU CH1')
# Parametriert die Quelle mit Strombegrenzung
	RudisNGL.write('INST:SEL 1') 
	RudisNGL.write('VOLT:AMPL %s' % str(UQ))
	RudisNGL.write('CURR:AMPL 3')
# FTR an aus
	RudisNGL.write('OUTP:FTR %s' % str(ftr))
	RudisNGL.write('OUTP 1')
# Ausgang an
	RudisNGL.write('OUTP:GEN 1')
	time.sleep(1)
# Ergebnisse anfordern
	RudisMSO6.write('SAVE:IMG')
	tr = RudisMSO6.query_ascii_values('MEASU:MEAS1:RESU:CURR:MAX?')
	print(tr)
	f.write('%s	%s\n' % (UQ,tr))
else:
# Ausgang aus
	RudisNGL.write('OUTP:GEN 0')
	f.close()
	print "Ende"
