import numpy as np
import matplotlib.pyplot as plt

def generate_sinusoid(frequency, fs=100, amplitude=1, phase=0, periods=30):
    if frequency == 0:
        num_points = periods * fs
        t = np.linspace(0, periods, num_points)
        y = np.ones_like(t)
    else:
        T = 1 / frequency
        total_time = periods * T
        num_points = int(fs * total_time)
        num_points = num_points if num_points % 2 == 0 else num_points + 1
        t = np.linspace(0, total_time, num_points, endpoint=False)
        y = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    return t, y

def decimate_signal(t, y):
    return t[::2], y[::2]

def interpolate_signal(t_dec, y_dec):
    t_interp = np.linspace(t_dec[0], t_dec[-1], 2*len(t_dec))
    y_interp = np.interp(t_interp, t_dec, y_dec)
    return t_interp, y_interp

def calculate_mse(y_orig, y_restored):
    return np.mean((y_orig - y_restored)**2)

def process_signal(frequency):
    t_orig, y_orig = generate_sinusoid(frequency)
    t_dec, y_dec = decimate_signal(t_orig, y_orig)
    t_interp, y_interp = interpolate_signal(t_dec, y_dec)
    
    y_restored = np.interp(t_orig, t_interp, y_interp)
    return t_orig, y_orig, y_restored, calculate_mse(y_orig, y_restored)

def main():
    frequency = float(input("Введите частоту (0-50 Гц): "))
    
    if not 0 <= frequency <= 50:
        print("Неверная частота!")
        return

    t, y_orig, y_restored, mse = process_signal(frequency)
    
    # Визуализация
    plt.figure(figsize=(12, 6))
    plt.plot(t, y_orig, 'b-', label='Исходный сигнал', linewidth=2)
    plt.plot(t, y_restored, 'r--', label='Восстановленный сигнал', alpha=0.8)
    plt.title(f"Сравнение сигналов ({frequency} Гц)\nMSE: {mse:.2e}")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.legend()
    plt.grid()
    plt.show()

    frequencies = np.arange(0, 51)
    mse_values = []
    
    for freq in frequencies:
        *_, mse = process_signal(freq)
        mse_values.append(mse)
    
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, mse_values, 'bo-')  # Обычная шкала
    plt.title("Зависимость MSE от частоты")
    plt.xlabel("Частота, Гц")
    plt.ylabel("MSE")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()