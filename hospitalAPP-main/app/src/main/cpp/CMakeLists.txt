cmake_minimum_required(VERSION 3.4.1)

add_library(
        rootcheck
        SHARED
        rootcheck.c
)

find_library(
        log-lib
        log
)

target_link_libraries(
        rootcheck
        ${log-lib}
)