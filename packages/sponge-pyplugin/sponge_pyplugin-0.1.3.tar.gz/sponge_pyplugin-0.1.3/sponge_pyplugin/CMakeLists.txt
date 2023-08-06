set(PROJECT_NAME sponge_pyplugin)
project(${PROJECT_NAME} LANGUAGES CXX CUDA)
cmake_minimum_required(VERSION 3.18)


set(SOURCES "")
set(INCLUDES "")
set(LIBRARIES "")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE  ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

list(APPEND SOURCES main.cu control.cuh common.cuh)

if (CUDA_VERSION VERSION_GREATER "11.0")
set(CMAKE_CUDA_ARCHITECTURES 70)
else()
set(CMAKE_CUDA_ARCHITECTURES 50)
endif()

add_library(${PROJECT_NAME} SHARED ${SOURCES})
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pyplugin" PREFIX "")
set_target_properties(${PROJECT_NAME} PROPERTIES CUDA_SEPARABLE_COMPILATION ON)


list(APPEND INCLUDES ${CUDA_INCLUDE_DIRS})
list(APPEND LIBRARIES ${CUDA_LIBRARIES})

include_directories(${INCLUDES})
target_link_libraries(${PROJECT_NAME} PUBLIC ${LIBRARIES})


