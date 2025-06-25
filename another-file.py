import psutil
import GPUtil

try:
except ImportError:
    GPUtil = None

try:
    import wmi  # For Windows
except ImportError:
    wmi = None

def get_cpu_temp():
    temps = psutil.sensors_temperatures()
    cpu_temps = temps.get('coretemp') or temps.get('cpu-thermal') or temps.get('acpitz')
    if cpu_temps:
        return [entry.current for entry in cpu_temps]
    return None

def get_gpu_temp():
    if GPUtil:
        gpus = GPUtil.getGPUs()
        return [gpu.temperature for gpu in gpus]
    return None

def get_windows_temps():
    if wmi:
        w = wmi.WMI(namespace="root\\wmi")
        temperature_info = w.MSAcpi_ThermalZoneTemperature()
        temps = []
        for sensor in temperature_info:
            # Temperature is reported in tenths of Kelvin
            temp_c = (sensor.CurrentTemperature / 10.0) - 273.15
            temps.append(temp_c)
        return temps
    return None

def main():
    print("CPU Temperatures:", get_cpu_temp())
    print("GPU Temperatures:", get_gpu_temp())
    if wmi:
        print("Windows Hardware Temperatures:", get_windows_temps())

if __name__ == "__main__":
    main()