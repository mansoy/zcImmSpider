program Controller;

uses
  Vcl.Forms,
  uFrmMain in 'uFrmMain.pas' {FrmMain},
  Vcl.Themes,
  Vcl.Styles;

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.Title := '���������';
  TStyleManager.TrySetStyle('Turquoise Gray');
  Application.CreateForm(TFrmMain, FrmMain);
  Application.Run;
end.
