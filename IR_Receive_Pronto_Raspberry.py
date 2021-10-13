import os , shlex
import subprocess as sp
import time
#getting the spaces and pulses from terminal shell
command = "sudo mode2 -d/dev/lirc0"
p=sp.Popen(command.split(),preexec_fn=os.setpgrp,stdout=sp.PIPE,universal_newlines=True)
time.sleep(3)
pgid=os.getpgid(p.pid)
p_kill=sp.Popen(['sudo','kill',format(pgid)])
mess = p.communicate()
p.wait()

#splitting the list of on and off times 
temp_list = (mess[0])
space_pulse = temp_list.split("\n")
space_pulse.pop(0)

RAW=[]
for i in range (len(space_pulse)-1):
    b=space_pulse[i].split(" ")
    RAW.append(int(b[1]))
    
print(RAW)                                                   #raw on and off cycles

frequency = 38000                                            #you can change frequency as you wish 
time_period = (1/frequency)*1000000
burst_pairs_count = int(len(RAW)/2)


def int_to_hex(num):
    temp_hex=hex(num)
    if (len(str(temp_hex[2:]))==4):                          #making the 4 digit hex
        return temp_hex[2:]
    elif (len(str(temp_hex[2:]))==3):                        #making the 4 digit hex
        return '0'+ temp_hex[2:]
    elif (len(str(temp_hex[2:]))==2):                        #making the 4 digit hex
        return '00'+ temp_hex[2:]
    elif (len(str(temp_hex[2:]))==1):                        #making the 4 digit hex
        return '000'+ temp_hex[2:]


def make_pronto():
    if(len(RAW)==0):
        return []
    pronto_hex=[]
    #making the preamable part
    pronto_hex.append('0000')                                 #lead in
    freq = int(1000000/(frequency*0.241246))
    pronto_hex.append(int_to_hex(freq))                       #frequency
    pronto_hex.append(int_to_hex(burst_pairs_count))
    pronto_hex.append('0000')                                 #lead out
    for c in RAW:
        pronto_hex.append(int_to_hex(int(c/time_period)))     #convert spaces and pulses to 4 digit hex
    return pronto_hex

print(make_pronto())