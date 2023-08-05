#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "vivid::vivid" for configuration "Release"
set_property(TARGET vivid::vivid APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(vivid::vivid PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libvivid.so"
  IMPORTED_SONAME_RELEASE "libvivid.so"
  )

list(APPEND _cmake_import_check_targets vivid::vivid )
list(APPEND _cmake_import_check_files_for_vivid::vivid "${_IMPORT_PREFIX}/lib/libvivid.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
