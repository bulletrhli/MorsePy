@echo off
set args=-w %1 -o %2
set file=%3
set par=%args% %file%
ebook2cw.exe %par%

