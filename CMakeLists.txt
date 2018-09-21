set (CMAKE_CXX_STANDARD 11)
cmake_minimum_required(VERSION 2.8.12)
project(cubicalRipser)
# Set source directory
set(SOURCE_DIR "src/")
# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/cubicalripser_2dim.cpp" "${SOURCE_DIR}/dense_cubical_grids.cpp" "${SOURCE_DIR}/birthday_index.cpp" "${SOURCE_DIR}/columns_to_reduce.cpp" "${SOURCE_DIR}/simplex_coboundary_enumerator.cpp" "${SOURCE_DIR}/union_find.cpp" "${SOURCE_DIR}/write_pairs.cpp" "${SOURCE_DIR}/compute_pairs.cpp")
include_directories("${SOURCE_DIR}/include") 

# Generate Python module
add_subdirectory(lib/pybind11)
pybind11_add_module(cubicalRipser ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
