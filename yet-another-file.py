import subprocess
import time
import threading

def get_cpu_temp():
    try:
        # Use osx-cpu-temp if installed
        output = subprocess.check_output(["osx-cpu-temp"]).decode()
        temp = float(output.split("°")[0])
        return temp
    except Exception:
        return None

def get_cpu_freq():
    try:
        output = subprocess.check_output(
            ["sysctl", "-n", "hw.cpufrequency"]
        ).decode()
        freq_hz = int(output.strip())
        freq_ghz = freq_hz / 1_000_000_000
        return freq_ghz
    except Exception:
        return None

def stress_cpu(duration=30):

    def busy_loop():
        t_end = time.time() + duration
        while time.time() < t_end:
            pass

    threads = []
    for _ in range(4):  # Adjust for your CPU core count
        t = threading.Thread(target=busy_loop)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def main():
    print("Testing for CPU throttling...")
    print("Initial CPU frequency: {:.2f} GHz".format(get_cpu_freq() or 0))
    print("Initial CPU temperature: {}°C".format(get_cpu_temp() or "N/A"))

    print("Stressing CPU for 30 seconds...")
    stress_cpu(30)

    print("After stress:")
    print("CPU frequency: {:.2f} GHz".format(get_cpu_freq() or 0))
    print("CPU temperature: {}°C".format(get_cpu_temp() or "N/A"))

if __name__ == "__main__":
    main()