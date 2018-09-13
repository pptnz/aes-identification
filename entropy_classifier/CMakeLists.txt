cmake_minimum_required(VERSION 3.12)
project(entropy_classifier)

set(CMAKE_CXX_STANDARD 14)

add_executable(entropy_classifier main.cpp Counter.cpp Counter.h Directory.cpp Directory.h Timer.cpp Timer.h EncryptionChecker.cpp EncryptionChecker.h SettingsReader.cpp SettingsReader.h)