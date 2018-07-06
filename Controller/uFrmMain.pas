unit uFrmMain;

interface

uses
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls, IdHttp, Vcl.ExtCtrls, System.DateUtils,
  cxEdit, Vcl.ComCtrls, dxCore, cxDateUtils, cxTextEdit, cxMaskEdit, cxDropDownEdit,
  cxCalendar, cxGraphics, cxControls, cxLookAndFeels, cxLookAndFeelPainters, cxContainer;

type
  TFrmMain = class(TForm)
    Panel1: TPanel;
    RadioGroup1: TRadioGroup;
    GroupBox1: TGroupBox;
    Panel2: TPanel;
    btnExec: TButton;
    btnExit: TButton;
    deBegin: TcxDateEdit;
    deEnd: TcxDateEdit;
    Label1: TLabel;
    Label2: TLabel;
    edtUrl: TEdit;
    Label3: TLabel;
    GroupBox2: TGroupBox;
    Memo1: TMemo;
    GroupBox3: TGroupBox;
    chkOp: TCheckBox;
    chkYp: TCheckBox;
    chkDx: TCheckBox;
    chkRq: TCheckBox;
    chkBf: TCheckBox;
    chkAll: TCheckBox;
    procedure btnExecClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure RadioGroup1Click(Sender: TObject);
    procedure btnExitClick(Sender: TObject);
    procedure chkAllClick(Sender: TObject);
  private
    { Private declarations }
    FUrl: string;
    procedure AddLog(AMsg: string);
  public
    { Public declarations }
  end;

var
  FrmMain: TFrmMain;

implementation

{$R *.dfm}

procedure WorkThread(AParam: Pointer);
var
  vForm: TFrmMain;
  vHttp: TIdHttp;
  sRet: string;
begin
  vForm := TFrmMain(AParam);
  if vForm = nil then Exit;
  vForm.btnExec.Enabled := False;
  vForm.btnExit.Enabled := False;
  vForm.AddLog('正在执行任务, 请稍等...');
  vHttp := TIdHttp.Create(vForm);
  try
    try
      sRet := vHttp.Get(vForm.FUrl);
      vForm.AddLog(sRet);
      vHttp.Disconnect;
    except on E: Exception do
      vForm.AddLog(E.Message);
    end;
  finally
    vForm.btnExec.Enabled := True;
    vForm.btnExit.Enabled := True;
    FreeAndNil(vHttp);
    vForm.AddLog('任务执行完成...');
  end;
end;

procedure TFrmMain.AddLog(AMsg: string);
var
  sMsg: string;
begin
  sMsg := FormatDateTime('[yyyy-MM-dd HH:MM:SS]', Now);
  sMsg := Format('%s%s', [sMsg, AMsg]);
  Self.Memo1.Lines.Add(sMsg);
end;

procedure TFrmMain.btnExecClick(Sender: TObject);
var
  sRet, sbDate, seDate: string;
  vHttp: TIdHttp;
  url: string;
  dwTid: DWORD;
  iTmp: Integer;
begin
  url := Trim(Self.edtUrl.Text);
  case Self.RadioGroup1.ItemIndex of
    0: url := url + 'imm';
    1: url := url + 'ls';
    2:
    begin
      url := Format('%shistory?startdate=%s&enddate=%s&ou=%d&ya=%d&dx=%d&rq=%d&bf=%d',
          [
            url,
            Self.deBegin.Text,
            Self.deEnd.Text,
            chkOp.Checked.ToInteger,
            chkYp.Checked.ToInteger,
            chkDx.Checked.ToInteger,
            chkRq.Checked.ToInteger,
            chkBf.Checked.ToInteger
          ]);
    end;
    3: url := url + 'og';
    4: url := url + 'oc';
    5: url := url + 'wc';
  end;
  Self.FUrl := url;
  BeginThread(nil, 0, @WorkThread, Self, 0, dwTid);
end;

procedure TFrmMain.btnExitClick(Sender: TObject);
begin
  Self.Close;
end;

procedure TFrmMain.chkAllClick(Sender: TObject);
begin
  chkOp.Checked := chkAll.Checked;
  chkYp.Checked := chkAll.Checked;
  chkDx.Checked := chkAll.Checked;
  chkRq.Checked := chkAll.Checked;
  chkBf.Checked := chkAll.Checked;
end;

procedure TFrmMain.FormCreate(Sender: TObject);
begin
  Self.Memo1.Lines.Clear;
  Self.deBegin.Date := IncMonth(Now, -1);
  Self.deEnd.Date := Now;
end;

procedure TFrmMain.RadioGroup1Click(Sender: TObject);
begin
  case TRadioGroup(Sender).ItemIndex of
    2:
    begin
      deBegin.Enabled := True;
      deEnd.Enabled := True;
      deBegin.Date := IncMonth(Now, -1);
      deEnd.Date := Now;
    end;
    else
    begin
      deBegin.Enabled := False;
      deEnd.Enabled := False;
      //deBegin.Date := System.DateUtils.IncDay(Now, -1);
      //deEnd.Date := Now;
    end;
  end;
end;

end.
