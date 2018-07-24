import cpuinfo
import os

def cpu_info():
   """Get CPU info by cpuinfo lib: [Brand, Version, Hardware, Hz_actual]"""
   p = cpuinfo.get_cpu_info()
   return [p['brand'], p['cpuinfo_version'], p['hardware'], p['hz_actual']]

def cpu_info_comp():
   """Get Complementary infos on CPU: [Revision, Serial]"""
   res = ["", ""]
   with open('/proc/cpuinfo') as cpuinfo:
      for line in cpuinfo:
          if 'Revision' in line:
              res[0] = line.rsplit(None, 1)[-1]
          elif 'Serial' in line:
              res[1] = line.rsplit(None, 1)[-1]
   return res

def cpu_temperature():
   """Get CPU Temperature. Return a Float"""
   res = os.popen("vcgencmd measure_temp").readline()
   return float(res.replace("temp=","").replace("'C\n",""))

def cpu_use():
   """Get CPU Usage. Return a Float pourcentage"""
   return float(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()) * 100

def ram_info():
   """Get Ram info. Return: [Total, Used, Free]"""
   p = os.popen('free')
   count = 0
   while True:
       count += 1
       line = p.readline()
       if count == 2: return line.split()[1:4]

def diskspace_info():
   """Get Disk Space Info. Return [Total Size, Used, Available, Use %]"""
   p = os.popen("df -h /")
   count = 0
   while True:
      count += 1
      line = p.readline()
      if count == 2: return line.split()[1:5]
