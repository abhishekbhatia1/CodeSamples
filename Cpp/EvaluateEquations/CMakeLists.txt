cmake_minimum_required(VERSION 2.8)

project( T_C_C )

include_directories(include)

set(SOURCES src/TCC.cpp src/main.cpp)

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

add_executable(../main ${SOURCES})

add_compile_options(-std=c++11)

set(CMAKE_BUILD_TYPE Debug)
