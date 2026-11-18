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

        # Overlay de debug ImGui (RMIG-013), compile uniquement sur le chemin
        # Vulkan et active par F12.
        set(IMGUI_DIR ${ROOT_DIR}/external/imgui)
        add_library(imgui_overlay STATIC
            ${IMGUI_DIR}/imgui.cpp
            ${IMGUI_DIR}/imgui_draw.cpp
            ${IMGUI_DIR}/imgui_tables.cpp
            ${IMGUI_DIR}/imgui_widgets.cpp
            ${IMGUI_DIR}/backends/imgui_impl_sdl2.cpp
            ${IMGUI_DIR}/backends/imgui_impl_vulkan.cpp
        )
        target_include_directories(imgui_overlay PUBLIC
            ${IMGUI_DIR}
            ${IMGUI_DIR}/backends
        )
        target_link_libraries(imgui_overlay PUBLIC ${SDL2_LIBRARY} Vulkan::Vulkan)
        target_compile_definitions(imgui_overlay PUBLIC HAVE_IMGUI=1)

        target_compile_definitions(${PROJECT_NAME} PUBLIC HAVE_IMGUI=1)
        target_include_directories(${PROJECT_NAME} PUBLIC
            ${IMGUI_DIR}
            ${IMGUI_DIR}/backends
        )
        target_link_libraries(${PROJECT_NAME} PUBLIC imgui_overlay)
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
