cmake_minimum_required(VERSION 3.5)
set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
project(rplight)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_INSTALL_RPATH ".")

find_package(PythonInterp 3.2 REQUIRED)
find_package(PythonLibs 3.2 REQUIRED)
include_directories(${PYTHON_INCLUDE_DIR})

find_path(PANDA_INCLUDE_DIR NAMES panda3d/pandatoolbase.h)
include_directories(${PANDA_INCLUDE_DIR}/panda3d)

find_library(PANDAGL_LIBRARY_PATH NAMES libpandagl.so libpandagl.dll)
get_filename_component(PANDA_LIBRARY_DIR ${PANDAGL_LIBRARY_PATH} DIRECTORY)
link_directories(${PANDA_LIBRARY_DIR})

include_directories(source)
add_subdirectory(source)
