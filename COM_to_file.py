import serial

ard=serial.Serial('COM5',115200)
ard.timeout = 1 # in seconds

logfile=open("logfile.log","w")

cnt = 0
while (cnt<1000):
    x = ard.readline()
    if len(x) == 0:
        break
    s = str(x)
    s=s[2:]
    i=1
    stemp=s[:i]
    while stemp.isdigit():
        i=i+1
        stemp=s[:i]
    if (i>1):
        s=stemp[:i-1]
        logfile.write(s+'\n')
        print(s)
    cnt=cnt+1
logfile.close

print("stop")