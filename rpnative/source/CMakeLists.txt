set(P3RPLIGHT_HEADERS
  config_rplight.h
  gpuCommand.h gpuCommand.I
  gpuCommandList.h
  iesDataset.h
  internalLightManager.h internalLightManager.I
  pointerSlotStorage.h
  pssmCameraRig.h pssmCameraRig.I
  rpLight.h rpLight.I
  rpPointLight.h rpPointLight.I
  rpSpotLight.h rpSpotLight.I
  shadowAtlas.h shadowAtlas.I
  shadowManager.h shadowManager.I
  shadowSource.h shadowSource.I
  tagStateManager.h tagStateManager.I
)

set(P3RPLIGHT_SOURCES
  config_rplight.cxx
  gpuCommand.cxx
  gpuCommandList.cxx
  iesDataset.cxx
  internalLightManager.cxx
  pssmCameraRig.cxx
  rpLight.cxx
  rpPointLight.cxx
  rpSpotLight.cxx
  shadowAtlas.cxx
  shadowManager.cxx
  shadowSource.cxx
  tagStateManager.cxx
)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/rplight_igate.cpp ${CMAKE_CURRENT_BINARY_DIR}/rplight.in
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND interrogate -DCPPPARSER -D__STDC__=1 -D__cplusplus=201103L
  -I${PANDA_INCLUDE_DIR}/panda3d
  -S${PANDA_INCLUDE_DIR}/panda3d/parser-inc
  -oc ${CMAKE_CURRENT_BINARY_DIR}/rplight_igate.cpp
  -od ${CMAKE_CURRENT_BINARY_DIR}/rplight.in
  -fnames -string -refcount -assert -python-native -nomangle
  -module rplight -library rplight
  ${P3RPLIGHT_HEADERS}
  DEPENDS ${P3RPLIGHT_HEADERS}
)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/rplight_module.cpp
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMAND interrogate_module
  -oc ${CMAKE_CURRENT_BINARY_DIR}/rplight_module.cpp
  -module rplight -library rplight
  -python-native
  -import panda3d.core
  ${CMAKE_CURRENT_BINARY_DIR}/rplight.in
  DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/rplight_igate.cpp ${CMAKE_CURRENT_BINARY_DIR}/rplight.in
)

add_library(
  rplight SHARED
  ${P3RPLIGHT_HEADERS}
  ${P3RPLIGHT_SOURCES}
  ${CMAKE_CURRENT_BINARY_DIR}/rplight_igate.cpp
  ${CMAKE_CURRENT_BINARY_DIR}/rplight_module.cpp
)

set_target_properties(rplight PROPERTIES PREFIX "")
if(WIN32)
  set_target_properties(rplight PROPERTIES SUFFIX ".pyd")
endif()

if(WIN32)
  set(PANDA_LIBS
    # PRIMARY
    libp3framework
    # COMMON_PANDA_LIBS
    libpanda
    libpandaexpress
    # COMMON_DTOOL_LIBS
    libp3dtool
    libp3dtoolconfig
    # EXTRA
    libp3direct
    libp3interrogatedb
  )
else()
  set(PANDA_LIBS
    # PRIMARY
    p3framework
    # COMMON_PANDA_LIBS
    panda
    pandaexpress
    # COMMON_DTOOL_LIBS
    p3dtool
    p3dtoolconfig
    # EXTRA
    p3direct
    p3interrogatedb
  )
endif()

target_link_libraries(rplight
  ${PANDA_LIBS}
  # PYTHON
  ${PYTHON_LIBRARY}
)

# if(MODULE_TYPE STREQUAL "MODULE")
#   set_target_properties(rplight PROPERTIES POSITION_INDEPENDENT_CODE ON)
# endif()

install(TARGETS rplight DESTINATION ${CMAKE_INSTALL_PREFIX})
