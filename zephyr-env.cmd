@echo off
set ZEPHYR_BASE=C:\Users\dmara\zephyrproject\zephyr

if exist "%userprofile%\zephyrrc.cmd" (
	call "%userprofile%\zephyrrc.cmd"
)
