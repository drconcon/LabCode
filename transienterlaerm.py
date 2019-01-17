# Semi-Automatisierung mit dem MSO der Serie 6
# Messung von Restwelligkeit und Netzgeräterauschen 
# UL = 0 mV, 100 mV, 200 mV, 300 mV, 500 mV, 700 mV, 900 mV, 1 V
import visa
import time
rm = visa.ResourceManager()
RudisNGL = rm.open_resource('ASRL/dev/ttyACM0::INSTR')
RudisMSO6 = rm.open_resource('TCPIP::172.16.32.138::INSTR')
print(RudisNGL.query('*IDN?'))
print(RudisMSO6.query('*IDN?'))
print(RudisMSO6.write('*RST'))
print("ftr")
ftr = float(raw_input())
f = open('ripple_pk2pk.txt', 'wb')
UQ = 1
while UQ!=0:
# 
# Ausgang aus
	RudisNGL.write('OUTP:GEN 0')
# Parameter setzen
	print("UQ")
	UQ = float(raw_input())
# 
# MSO6 AKQ
# Einfaches Sampling
	RudisMSO6.write('ACQ:MOD SAM')
#
# Anzahl der aufgenommenen Sequenzen 
	RudisMSO6.write('ACQ:SEQ:NUMSEQ 1')
#
# Single Shot
	RudisMSO6.write('ACQ:STOPA SEQ')
#
# Aufzeichnung an 
	RudisMSO6.write('ACQ:STATE 1')
#
# Horizontale und vertikale Skala
	RudisMSO6.write('HOR:SCA 20e-3')
	RudisMSO6.write('CH1:SCA %s' % str(0.5*UQ))
#
#Bandbreitenbegrenzung 20 MHz
	RudisMSO6.write('CH1:BAN 20')
#
#Eingangsbereich 50 Ohm
	RudisMSO6.write('CH1:TER 50')
#
# Triggerung
# Flankentrigger
	RudisMSO6.write('TRIG:A:EDGE:SOU CH1')
	RudisMSO6.write('TRIG:A:LEVEL:CH1 %s' % str(0.1*UQ))
	RudisMSO6.write('TRIG:TYPE EDGE')
	time.sleep(1)
# Pulsetrigger
# 	RudisMSO6.write('TRIG:A:PULSEW:SOU CH1')
# 	RudisMSO6.write('TRIG:A:PULSEW:LOWL 0.5e-3')
# 	RudisMSO6.write('TRIG:A:PULSEW:WHE LESS')
# 	RudisMSO6.write('TRIG:TYPE WIDTH')
# Messungen parametrieren
# RMS
	RudisMSO6.write('MEASU:ADDN MEAS1')
	RudisMSO6.write('MEASU:MEAS1:TYPE ACRMS')
	RudisMSO6.write('MEASU:MEAS1:SOU CH1')
# V_PK2PK
	RudisMSO6.write('MEASU:ADDN MEAS2')
	RudisMSO6.write('MEASU:MEAS2:TYPE PK2PK')
	RudisMSO6.write('MEASU:MEAS2:SOU CH1')
# Parametriert die Quelle mit Strombegrenzung auf kritischen Lastwert
	RudisNGL.write('INST:SEL 1')
	RudisNGL.write('VOLT:ALIM 1') 
	RudisNGL.write('ALIM 1') 
	RudisNGL.write('VOLT:AMPL %s' % str(UQ))
	RudisNGL.write('CURR:AMPL 2e-2')
# FTR an aus
	RudisNGL.write('OUTP:FTR %s' % str(ftr))
	RudisNGL.write('OUTP 1')
# Ausgang an
	RudisNGL.write('OUTP:GEN 1')
# Warten
	time.sleep(1)
# Ergebnisse anfordern
	RudisMSO6.write('SAVE:IMG')
	rms = RudisMSO6.query_ascii_values('MEASU:MEAS1:RESU:CURR:MAX?')
	print(rms)
	pk2pk = RudisMSO6.query_ascii_values('MEASU:MEAS2:RESU:CURR:MAX?')
	print(pk2pk)
	f.write('%s	%s	%s\n' % (UQ, rms, pk2pk))
else:
# Ausgang aus
	RudisNGL.write('OUTP:GEN 0')
	f.close()
	print "Ende"
