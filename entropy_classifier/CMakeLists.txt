cmake_minimum_required(VERSION 3.12)
project(aes_software_analyzer)

set(CMAKE_CXX_STANDARD 14)

add_executable(aes_software_analyzer main.cpp Counter.cpp Counter.h Directory.cpp Directory.h Timer.cpp Timer.h EncryptionChecker.cpp EncryptionChecker.h SettingsReader.cpp SettingsReader.h)