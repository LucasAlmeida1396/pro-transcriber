[Setup]
; Configurações Gerais do Aplicativo
AppName=ProTranscriber
AppVersion=1.0.0
AppPublisher=Lucas Pacheco de Almeida
AppPublisherURL=https://github.com/LucasAlmeida1396
DefaultDirName={autopf}\ProTranscriber
DefaultGroupName=ProTranscriber
OutputBaseFilename=ProTranscriber_Setup
SetupIconFile=assets\logo.ico
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64os

; AQUI VOCÊ COLOCA O CAMINHO COMPLETO ATÉ A SUA PASTA "dist/ProTranscriber"
SourceDir=C:\SistemasFeitos\audio_transcription\dist\ProTranscriber

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Copia o executável principal e o ffmpeg para a raiz do programa
Source: "ProTranscriber.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion

; Copia a pasta _internal inteira
Source: "_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

; Copia a pasta assets (para o ícone)
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Cria os atalhos no Menu Iniciar e na Área de Trabalho com o seu ícone
Name: "{group}\ProTranscriber"; Filename: "{app}\ProTranscriber.exe"; IconFilename: "{app}\assets\logo.ico"
Name: "{autodesktop}\ProTranscriber"; Filename: "{app}\ProTranscriber.exe"; IconFilename: "{app}\assets\logo.ico"; Tasks: desktopicon

[Run]
; Oferece a opção de iniciar o programa assim que a instalação terminar
Filename: "{app}\ProTranscriber.exe"; Description: "{cm:LaunchProgram,ProTranscriber}"; Flags: nowait postinstall skipifsilent