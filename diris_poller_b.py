# -*- coding: utf-8 -*- 

import time, sys
import datetime
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.payload import BinaryPayloadDecoder



diris_slave_id = 1

data_file_prefix = 'diris_data_'
time_lapse = 3
diris_port='COM3'



def write_data(datastr):
	now = datetime.datetime.now()
	data_file_name = data_file_prefix + now.strftime("%Y-%m") + ".log"
	OF = open(data_file_name,"a")
	OF.write(datastr + "\n")
	print datastr
	OF.close()


	
if __name__  == "__main__":


	now = datetime.datetime.now()
	write_data("Starting data logger "+ now.strftime("%Y-%m-%d %H:%M")+"\n\n")
	
	diris_modbus = ModbusClient(method='rtu', port=diris_port, timeout=1, baudrate=9600, parity='E')
	
	if (not diris_modbus.connect()):
		print "Connection Failed"
		sys.exit()
	
	



	while True:


		rk = diris_modbus.read_holding_registers(50536,2,unit=diris_slave_id)
		active_p = BinaryPayloadDecoder.fromRegisters(rk.registers,endian=Endian.Big).decode_32bit_uint()
		active_p = float(active_p)/100

		rk = diris_modbus.read_holding_registers(50538,2,unit=diris_slave_id)
		reactive_p = BinaryPayloadDecoder.fromRegisters(rk.registers,endian=Endian.Big).decode_32bit_uint()

		rk = diris_modbus.read_holding_registers(50540,2,unit=diris_slave_id)
		apparent_p = BinaryPayloadDecoder.fromRegisters(rk.registers,endian=Endian.Big).decode_32bit_int()

		now = datetime.datetime.now()
		result_string = '%s = (Kw, Var, KVA),%s,%s,%s' % (now.strftime("%H:%M:%S "),active_p,reactive_p,apparent_p)

		write_data(result_string) 
		
		time.sleep(time_lapse)
