import subprocess

def getTemp() :
    cmd = "cat /sys/class/thermal/thermal_zone0/temp"
    commande =  subprocess.run(cmd.split(),stdout = subprocess.PIPE)
    return(int(commande.stdout)/1000)