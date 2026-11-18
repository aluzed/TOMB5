cmake_minimum_required (VERSION 3.0)

project (Emulator_${TARGET_ARCH})

set(OPT_DEFINITIONS "")

#Extract current source folder name.
get_filename_component(PLATFORM_SPECIFIC_FOLDER_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)

#Enable NTSC mode
OPTIONAL_DEFINE(NTSC_VERSION "Enable/Disable NTSC Mode" ON)

#Enable 32-bit address for tag
OPTIONAL_DEFINE(USE_32_BIT_ADDR "Enable/Disable 32-bit address for tag" ON)

#Setup platform specific / game code include folder
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${GAME_CODE_DIR})

#Recursively locate the source files for SPEC_PSX.
file(GLOB_RECURSE EMULATOR_SPECIFIC_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.C  ${CMAKE_CURRENT_SOURCE_DIR}/*.S ${CMAKE_CURRENT_SOURCE_DIR}/*.H ${CMAKE_CURRENT_SOURCE_DIR}/*.CUR ${CMAKE_CURRENT_SOURCE_DIR}/*.RC)

#Group solution source files to correct folders.
source_group(${PLATFORM_SPECIFIC_FOLDER_NAME} FILES ${EMULATOR_SPECIFIC_SRCS})

if(NOT ANDROID)
add_library(
${PROJECT_NAME}
STATIC
${EMULATOR_SPECIFIC_SRCS}
)
endif()

# Vulkan backend (64 bits uniquement pour l'instant ; le 32 bits garde le
# backend GL de reference).
if(NOT ANDROID AND CMAKE_SIZEOF_VOID_P EQUAL 8)
    find_package(Vulkan QUIET)
    if(Vulkan_FOUND)
        target_link_libraries(${PROJECT_NAME} PUBLIC Vulkan::Vulkan)
        target_compile_definitions(${PROJECT_NAME} PUBLIC HAVE_VULKAN=1)
    endif()
endif()

#Include all platform specific cmake files.
include("PLATFORM/Windows.cmake")
include("PLATFORM/Mingw.cmake")
include("PLATFORM/Linux.cmake")
include("PLATFORM/Emscripten.cmake")
include("PLATFORM/Android.cmake")

if (NOT ANDROID)
BuildPreProcessorDefinitions()
target_compile_definitions(${PROJECT_NAME} PRIVATE GLEW_STATIC)

set_target_properties(
${PROJECT_NAME} PROPERTIES OUTPUT_NAME "PSX"
${PROJECT_NAME} PROPERTIES FOLDER "Libs"
)
endif()
