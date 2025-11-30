cmake_minimum_required(VERSION 3.10)

project(sliding_window_benchmark)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(benchmark
  benchmark.cpp
  ../algorithms/naive.cpp
  ../algorithms/sliding.cpp
  ../algorithms/generate.cpp
)
