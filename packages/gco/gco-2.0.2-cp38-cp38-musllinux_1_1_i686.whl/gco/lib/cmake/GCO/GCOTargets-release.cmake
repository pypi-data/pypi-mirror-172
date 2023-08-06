#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "GCO::gco" for configuration "Release"
set_property(TARGET GCO::gco APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(GCO::gco PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgco.a"
  )

list(APPEND _cmake_import_check_targets GCO::gco )
list(APPEND _cmake_import_check_files_for_GCO::gco "${_IMPORT_PREFIX}/lib/libgco.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
