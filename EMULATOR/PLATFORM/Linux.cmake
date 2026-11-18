if(UNIX AND NOT(ANDROID) AND NOT(EMSCRIPTEN))

#Find libs
find_package(SDL2 REQUIRED)

# Le build 64 bits est Vulkan-only (RMIG-012) : OpenGL/GLEW ne sont plus
# requis ni lies. Le build 32 bits conserve le chemin OpenGL de reference.
if(NOT (CMAKE_SIZEOF_VOID_P EQUAL 8) OR PORT_ALLOW_GL)
    find_package(OpenGL REQUIRED)
    #We want to link GLEW statically
    set(GLEW_USE_STATIC_LIBS ON)
    find_package(GLEW REQUIRED)

    #Setup project include directories
    include_directories(${GLEW_INCLUDE_DIR})
endif()
include_directories(${SDL2_INCLUDE_DIR})

set(PSX_LIB libPSX.a)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-narrowing")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -Wno-narrowing")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -Wno-narrowing")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-narrowing")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -Wno-narrowing")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Wno-narrowing")

endif()
