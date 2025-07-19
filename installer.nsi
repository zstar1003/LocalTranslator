; LocalTranslator Installer Script
; Using NSIS (Nullsoft Scriptable Install System)

;--------------------------------
; Include Modern UI
!include "MUI2.nsh"

;--------------------------------
; Constants
!define APP_NAME "LocalTranslator"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "LocalTranslator"
!define APP_URL "https://github.com/zstar1003/LocalTranslator"
!define APP_EXECUTABLE "LocalTranslator.exe"

;--------------------------------
; Installer Properties
Name "${APP_NAME}"
OutFile "LocalTranslator_Setup.exe"
Unicode True

; Default installation directory
InstallDir "$PROGRAMFILES64\${APP_NAME}"

; Get installation directory from registry
InstallDirRegKey HKLM "Software\${APP_PUBLISHER}\${APP_NAME}" "InstallDir"

; Request administrator privileges
RequestExecutionLevel admin

;--------------------------------
; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "ui\logo.ico"
!define MUI_UNICON "ui\logo.ico"

; Welcome page
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${APP_NAME} Setup"
!define MUI_WELCOMEPAGE_TEXT "This will install ${APP_NAME} on your computer.$\r$\n$\r$\n${APP_NAME} is an AI-based local translation tool that supports Chinese, English, and Russian translation.$\r$\n$\r$\nClick Next to continue."

; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXECUTABLE}"
!define MUI_FINISHPAGE_RUN_TEXT "Run ${APP_NAME}"

;--------------------------------
; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
; Languages
!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Version Information
VIProductVersion "1.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "${APP_NAME}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "Comments" "AI-based Local Translation Tool"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "© 2024 ${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "${APP_NAME} Setup"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${APP_VERSION}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductVersion" "${APP_VERSION}"

;--------------------------------
; Installation Section
Section "Main Program" SecMain

  SectionIn RO

  ; Set output path
  SetOutPath "$INSTDIR"

  ; Copy files
  File /r "dist\LocalTranslator\*.*"

  ; Write registry
  WriteRegStr HKLM "Software\${APP_PUBLISHER}\${APP_NAME}" "InstallDir" "$INSTDIR"
  WriteRegStr HKLM "Software\${APP_PUBLISHER}\${APP_NAME}" "Version" "${APP_VERSION}"

  ; Write uninstall information
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\${APP_EXECUTABLE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1

  ; Create uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"

SectionEnd

; Optional: Desktop Shortcut
Section "Desktop Shortcut" SecDesktop

  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_EXECUTABLE}" 0

SectionEnd

; Optional: Start Menu Shortcut
Section "Start Menu Shortcut" SecStartMenu

  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_EXECUTABLE}" 0
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk" "$INSTDIR\uninstall.exe"

SectionEnd

;--------------------------------
; Component Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} "Install ${APP_NAME} main program files (required)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Create ${APP_NAME} shortcut on desktop"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Create ${APP_NAME} shortcut in Start Menu"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
; Uninstaller Section
Section "Uninstall"

  ; Delete files and directories
  RMDir /r "$INSTDIR"

  ; Delete shortcuts
  Delete "$DESKTOP\${APP_NAME}.lnk"
  RMDir /r "$SMPROGRAMS\${APP_NAME}"

  ; Delete registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "Software\${APP_PUBLISHER}\${APP_NAME}"

  ; Delete publisher key if empty
  DeleteRegKey /ifempty HKLM "Software\${APP_PUBLISHER}"

SectionEnd
