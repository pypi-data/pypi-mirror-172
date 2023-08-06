# numpy_array_buffer

Library for buffers used in real-time computation:

- RingBuffer: when full overwrites oldest row
- DownsamplingBuffer: when full downsamples full buffer

## Example

    ring_buffer = RingBuffer(3,2, column_names=["x", "y"])
    for i in range(6):
        ring_buffer.append([i, i + 10])
        print(f"{i=}, y: {ring_buffer.get_col('x')}")

output:

    i=0, y: [0.]
    i=1, y: [0. 1.]
    i=2, y: [0. 1. 2.]
    i=3, y: [1. 2. 3.]
    i=4, y: [2. 3. 4.]
    i=5, y: [3. 4. 5.]

Downsampled array

    downsampling_buffer = DownsamplingBuffer(4, 2)
    for i in range(9):
        data_object = [i, i + 10]
        downsampling_buffer.append(data_object)
        print(f"{i=}, Arr: {downsampling_buffer.get_array()[:,0]}")

output:

    i=0, Arr: [0.]
    i=1, Arr: [0. 1.]
    i=2, Arr: [0. 1. 2.]
    i=3, Arr: [0. 2.]
    i=4, Arr: [0. 2. 4.]
    i=5, Arr: [0. 4.]
    i=6, Arr: [0. 4.]
    i=7, Arr: [0. 4.]
    i=8, Arr: [0. 4. 8.]

## Similar packages:

Look at if functionality is the same, or compare benchmark:

- https://github.com/eric-wieser/numpy_ringbuffer/blob/master/numpy_ringbuffer/__init__.py
- https://stackoverflow.com/questions/8908998/ring-buffer-with-numpy-ctypes

## Develop:

    pip install -e .
