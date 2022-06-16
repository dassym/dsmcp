; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Dsmcp"
#define MyAppVersion "0.5.0"
#define MyAppPublisher "Dassym SA"
#define MyAppURL "https://www.dassym.com"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{30C7D693-6D2C-46ED-9DA9-EF7642A5AC2C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; Remove the following line to run in administrative install mode (install for all users.)
;PrivilegesRequired=lowest
;PrivilegesRequiredOverridesAllowed=dialog
OutputDir=G:\deploy\build\
OutputBaseFilename=dsmcp-setup
SetupIconFile=G:\src\app\gui\img\dcp.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "G:\src\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "G:\src\app\gui\img\dcp.ico"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

[UninstallDelete]
Type: files; Name: "{userdesktop}/dcpserial.lnk"
Type: files; Name: "{userdesktop}/dcphost.lnk"

[Code]
var
  Pass: Boolean;
  PythonExe: String;
const
  PY_MAJOR = 3;
  PY_MINOR = 8;

procedure createDesktopIcon(filename: string; description: string; shortcutTo: string; parameters:  string; workingDir: string; iconFilename: string);
begin
  Log(parameters)
  CreateShellLink(filename, description, shortcutTo, parameters, workingDir, iconFilename, 0, SW_SHOWNORMAL)
end;

procedure createDesktopSerialIcon();
begin
  createDesktopIcon(
    ExpandConstant('{userdesktop}\dcpserial.lnk'),
    'An application for debuging Dassym board by serial communication',
    'python.exe',
    ExpandConstant(' "{app}\dcpbasic.py" -c "dsmcp.ini" -S'),
    ExpandConstant('{app}'),
    ExpandConstant('{app}\dcp.ico')
  );
end;

procedure createDesktopHostIcon();
begin
  createDesktopIcon(
    ExpandConstant('{userdesktop}\dcphost.lnk'),
    'An application for debuging Dassym board by remote communication',
    'python.exe',
    ExpandConstant(' "{app}\dcpbasic.py" -c "dsmcp.ini" -H'),
    ExpandConstant('{app}'),
    ExpandConstant('{app}\dcp.ico')
  );
end;

function checkPython(): Boolean;
var
  PythonInstalled: Boolean;
  ReturnString: AnsiString;
  Version: String;
  ReturnCode: Integer;
  tmpFileName: String;
  PythonVersionGood: Boolean;
begin
  // python install
  TmpFileName := ExpandConstant('{tmp}') + '\pythonversion.txt';

  Exec('cmd.exe', '/C python --version > "' + TmpFileName + '"', '', SW_HIDE,
      ewWaitUntilTerminated, ReturnCode);
  if ReturnCode = 0 then begin
    if LoadStringFromFile(TmpFileName, ReturnString) then begin
      { do something with contents of file... }
      if StrToInt(ReturnString[8]) = PY_MAJOR then begin
        if StrToInt(ReturnString[10]) >= PY_MINOR then begin
          PythonVersionGood := True
          PythonExe := 'python'
        end else begin
          PythonVersionGood := False
        end;
      end else begin
        Exec('cmd.exe', '/C python3 --version > "' + TmpFileName + '"', '', SW_HIDE,
        ewWaitUntilTerminated, ReturnCode);
        if ReturnCode = 0 then begin
          if LoadStringFromFile(TmpFileName, ReturnString) then begin
            if StrToInt(ReturnString[8]) = PY_MAJOR then begin
              if StrToInt(ReturnString[10]) >= PY_MINOR then begin
                PythonVersionGood := True
                PythonExe := 'python3'
              end else begin
                PythonVersionGood := False
              end;
            end else begin
              PythonVersionGood := False
            end;
          end;
        end else begin
          PythonVersionGood := False
        end;
      end;
    end;
  end else begin
    PythonVersionGood := False
  end;
  
  Result := PythonVersionGood
end;

function InitializeSetup: Boolean;
begin
  Result := True
  if not checkPython then begin
    Result := False
    MsgBox('Dsmcp installation impossible. Please install python version ' + IntToStr(PY_MAJOR) + '.' + IntToStr(PY_MINOR) + '.x or greather.', mbInformation, MB_OK)
  end;
end;

procedure pipDependenciesInstall();
var
  ReturnCode: Integer;
begin
  Exec('python.exe', ExpandConstant('-m pip install -r "{app}\requirements.txt"'), '', SW_HIDE, ewWaitUntilTerminated, ReturnCode)

  Pass := True
  if ReturnCode <> 0 then begin
    Pass := False
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ReturnCode: Integer;             
begin   
  if CurStep=ssPostInstall then begin
    pipDependenciesInstall
    if Pass = False then begin
      Exec(ExpandConstant('{uninstallexe}'), ' /VERYSILENT /SUPPRESSMSGBOXES', '', SW_SHOW, ewWaitUntilTerminated, ReturnCode)
      MsgBox('Dsmcp installation failed', mbInformation, MB_OK)
      Abort()
    end else begin
      createDesktopSerialIcon
      //createDesktopHostIcon
    end;
  end;
end;

