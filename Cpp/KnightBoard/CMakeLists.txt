cmake_minimum_required(VERSION 2.8)

project( C_T_C )

include_directories(include)

set(SOURCES src/KnightBoard.cpp src/main.cpp)

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x	")

add_executable(../main ${SOURCES})

add_compile_options(-std=c++0x)

set(CMAKE_BUILD_TYPE Debug)
