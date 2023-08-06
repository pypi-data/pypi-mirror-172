project(sponge_pyplugin)
cmake_minimum_required(VERSION 3.10)
set(Python3_USE_STATIC_LIBS FALSE)
find_package(Python3 COMPONENTS Interpreter Development)

set(SOURCES "")
set(INCLUDES "")
set(LIBRARIES "")

list(APPEND SOURCES main.cpp)
list(APPEND INCLUDES ${Python3_INCLUDE_DIRS})
list(APPEND LIBRARIES ${Python3_LIBRARIES})

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE  ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

include_directories(${INCLUDES})
add_library(sponge_pyplugin SHARED ${SOURCES})
target_link_libraries(sponge_pyplugin PUBLIC ${LIBRARIES})

set_target_properties(sponge_pyplugin PROPERTIES OUTPUT_NAME "pyplugin" PREFIX "")
