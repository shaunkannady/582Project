#!/bin/bash

SAMPLING_FREQUENCY=10

nvidia-smi --query-gpu=timestamp,power.draw --format=csv -lms $SAMPLING_FREQUENCY > gpu_draw.csv & LOGGER_PID=$!

nsys profile ./build/debug/test/physics_unittest -i $SAMPLING_FREQUENCY

kill $LOGGER_PID
