import matplotlib.pyplot as plt
import numpy.typing as npt
import numpy as np
from typing import Annotated
import pandas as pd

def nsToS(time_result : int) -> float:
  return time_result / 1_000_000_000

cube_sizes : Annotated[npt.NDArray[np.int8], (5, 1)] = np.array([(n + 1) * 5 for n in range(5)], dtype=np.int8)
timing_values : Annotated[npt.NDArray[np.int8], (3000, 1)] = np.array([0.01 * n for n in range(1, 3001)], dtype=np.float32)
power_usages : Annotated[npt.NDArray[np.float32], (5, 3000)] = np.zeros((5, 3000), dtype=np.float32)

for index, cube_size in enumerate(cube_sizes):
  current_csv : pd.core.frame.DataFrame = pd.read_csv(f"gpu_draw_{cube_size}.csv")
  power_measurements : pd.core.series.Series = current_csv[" power.draw [W]"]
  power_measurements : pd.core.series.Series = power_measurements.str[1:-1]
  power_measurements : npt.NDArray[np.float32] = power_measurements.astype(np.float32).to_numpy()
  power_measurements = np.pad(power_measurements, (0, power_usages.shape[1] - power_measurements.shape[0]), 'constant')
  power_usages[index, :] = power_measurements

for index, cube_size in enumerate(cube_sizes):
  plt.plot(timing_values, power_usages[index], label= f'{cube_size}')


plt.title("Power Draw by Cube Size, System 2")
plt.xlabel("Time (s)")
plt.ylabel("Power Draw (W)")
plt.legend()
plt.show()

cube_sizes : Annotated[npt.NDArray[np.str_], (5, )] = np.array([str((n + 1) * 5) for n in range(5)], dtype=np.str_)
kernel_launch_times : Annotated[npt.NDArray[np.uint64], (5, )]  = np.array([176103085, 176129486, 184158652, 238190028, 206072427], dtype = np.uint64)
spring_kernel_times : Annotated[npt.NDArray[np.uint64], (5, )] = np.array([870423590, 1566915923, 4113670528, 8436511981, 16097389725], dtype = np.uint64)
mass_kernel_times : Annotated[npt.NDArray[np.uint64], (5, )] = np.array([533172719, 548243898, 754525147, 1331753887, 2560509260], dtype = np.uint64)
malloc_times : Annotated[npt.NDArray[np.uint64], (5, )] = np.array([67966894, 69926815, 135963777, 336473615, 588625545], dtype = np.uint64)

kernel_launch_times : Annotated[npt.NDArray[np.float64], (5, )] = np.vectorize(nsToS)(kernel_launch_times)
spring_kernel_times : Annotated[npt.NDArray[np.float64], (5, )] = np.vectorize(nsToS)(spring_kernel_times)
mass_kernel_times : Annotated[npt.NDArray[np.float64], (5, )] = np.vectorize(nsToS)(mass_kernel_times)
malloc_times : Annotated[npt.NDArray[np.float64], (5, )] = np.vectorize(nsToS)(malloc_times)

plt.barh(cube_sizes, spring_kernel_times, label="Spring")
plt.barh(cube_sizes, mass_kernel_times, left = spring_kernel_times, label="Mass")
plt.barh(cube_sizes, malloc_times, left = spring_kernel_times + mass_kernel_times, label="Malloc")
plt.barh(cube_sizes, kernel_launch_times, left = spring_kernel_times + mass_kernel_times + malloc_times, label="Launch")

plt.title("Timing Analysis by Cube Size, System 2")
plt.xlabel("Time (s)")
plt.ylabel("Cube Size")
plt.legend()
plt.show()