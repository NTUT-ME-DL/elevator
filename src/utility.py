def getCurrentMemoryUsage():
    # Memory usage in kB
    try:
        with open('/proc/self/status') as f:
            memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]

        return int(memusage.strip()) / 1024
    except:
        return "The function that get Current memory usage of the current process only support on Linux"