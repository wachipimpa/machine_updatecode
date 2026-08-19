
import time
class Write_file:


    def start_write(self, relay_8, plc_status, temperature, ph, orp, pressure, plc_in, plc_all_in):
        print("writefile open")
        with open('/home/pi/txt_file/status_relay_8.txt','w') as relay_file:
            relay_file.write(str(relay_8))

        with open('/home/pi/txt_file/status_plc.txt','w') as plc_file:
            plc_file.write(str(plc_status))

        with open('/home/pi/txt_file/status_plc_in.txt','w') as plc_file_in:
            plc_file_in.write(str(plc_in))

        with open('/home/pi/txt_file/temperature.txt','w') as temperature_file:
            temperature_file.write(str(temperature))


        with open('/home/pi/txt_file/ph.txt','w') as ph_file:
            ph_file.write(str(ph))
        
        with open('/home/pi/txt_file/orp.txt','w') as orp_file:
            orp_file.write(str(orp))

        with open('/home/pi/txt_file/pressure.txt','w') as pressure_file:
            pressure_file.write(str(pressure))
        
        with open('/home/pi/txt_file/status_plc_in_16.txt','w') as write_all_in:
            write_all_in.write(str(plc_all_in))
            write_all_in.close()

        print("writefile close")

    def write_over_presssure(self,pressure):
        print("writefile pressure open")
        with open('/home/pi/txt_file/count_down_close_system.txt','w') as pressure_file:
            pressure_file.write(str(pressure))
        print("writefile pressure close")

    def clear_pressure_time(self):
        with open('/home/pi/txt_file/count_down_close_system.txt','w') as count_down_read:
            count_down_read.write('')

    def counter_locking(self, data_setting):
        try:
            read_counter_lock = open('/home/pi/txt_file/couter_lock_machine.txt','r')
            if read_counter_lock.read() != "":
                counter_lock_machine = int(read_counter_lock.read())
                sum_counter_lock = counter_lock_machine + 1
                print("-----xxx---"+str(sum_counter_lock))
                with open('/home/pi/txt_file/couter_lock_machine.txt', 'w') as write_lock_machine:
                    write_lock_machine.write(str(sum_counter_lock))
           
                if sum_counter_lock >= ((int(data_setting[0]['setting_frequence']) * 60) * 60):
                        self.clear_pressure_time()
                        time.sleep(0.5)
                       
                        with open('/home/pi/txt_file/couter_lock_machine.txt', 'w') as f:
                            f.write("0")
            else:
                with open('/home/pi/txt_file/couter_lock_machine.txt', 'w') as f:
                    f.write("0")
        except:
             pass
    def set_zero_locking_counter(self):
        self.clear_pressure_time()
        time.sleep(0.5)
        with open('/home/pi/txt_file/couter_lock_machine.txt', 'w') as f:
             f.write("0")
        # write_lock_machine = open('/home/pi/txt_file/couter_lock_machine.txt','w')
        # write_lock_machine.write("0")
             
    def write_speed_vmc(self, vmc_speed):
        data = vmc_speed[0]['vmc_filtration']+','+vmc_speed[0]['vmc_choc']+','+vmc_speed[0]['vmc_backwash']
        with open('/home/pi/txt_file/vmc_set_speed.txt','w') as write_speed:
            write_speed.write(data)



