object FrmMain: TFrmMain
  Left = 0
  Top = 0
  Anchors = [akLeft, akTop, akRight, akBottom]
  Caption = #29228#34411#25511#21046#22120
  ClientHeight = 452
  ClientWidth = 748
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  Position = poScreenCenter
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object Panel1: TPanel
    Left = 0
    Top = 0
    Width = 631
    Height = 452
    Align = alClient
    TabOrder = 0
    ExplicitWidth = 542
    ExplicitHeight = 361
    DesignSize = (
      631
      452)
    object RadioGroup1: TRadioGroup
      Left = 8
      Top = 8
      Width = 161
      Height = 193
      Caption = #29228#34411#31867#22411
      ItemIndex = 0
      Items.Strings = (
        #26102#26102#25968#25454
        #32852#36187#25968#25454
        #21382#21490#25968#25454
        #27431#20896
        #27431#27954#26479
        #19990#30028#26479)
      TabOrder = 0
      OnClick = RadioGroup1Click
    end
    object GroupBox1: TGroupBox
      Left = 175
      Top = 8
      Width = 450
      Height = 193
      Anchors = [akLeft, akTop, akRight]
      Caption = #37197#32622
      TabOrder = 1
      ExplicitWidth = 427
      object Label1: TLabel
        Left = 16
        Top = 134
        Width = 52
        Height = 13
        Caption = #24320#22987#26085#26399':'
      end
      object Label2: TLabel
        Left = 204
        Top = 134
        Width = 52
        Height = 13
        Caption = #25130#33267#26085#26399':'
      end
      object Label3: TLabel
        Left = 16
        Top = 19
        Width = 52
        Height = 13
        Caption = #26381#21153#22320#22336':'
      end
      object deBegin: TcxDateEdit
        Left = 74
        Top = 131
        Enabled = False
        Properties.DateButtons = [btnClear, btnToday]
        Properties.DisplayFormat = 'yyyy-MM-dd'
        Properties.EditFormat = 'yyyy-MM-dd'
        Properties.ShowTime = False
        TabOrder = 0
        Width = 121
      end
      object deEnd: TcxDateEdit
        Left = 262
        Top = 131
        Enabled = False
        Properties.DateButtons = [btnClear, btnToday]
        Properties.DisplayFormat = 'yyyy-MM-dd'
        Properties.EditFormat = 'yyyy-MM-dd'
        Properties.ShowTime = False
        TabOrder = 1
        Width = 121
      end
      object edtUrl: TEdit
        Left = 74
        Top = 16
        Width = 311
        Height = 21
        TabOrder = 2
        Text = 'http://127.0.0.1:8080/'
      end
      object GroupBox3: TGroupBox
        Left = 16
        Top = 53
        Width = 369
        Height = 68
        TabOrder = 3
        object chkOp: TCheckBox
          Left = 32
          Top = 15
          Width = 97
          Height = 17
          Caption = #27431#36180
          TabOrder = 0
        end
        object chkYp: TCheckBox
          Left = 113
          Top = 15
          Width = 97
          Height = 17
          Caption = #20122#36180
          TabOrder = 1
        end
        object chkDx: TCheckBox
          Left = 177
          Top = 15
          Width = 97
          Height = 17
          Caption = #22823#23567#25351#25968
          TabOrder = 2
        end
        object chkRq: TCheckBox
          Left = 32
          Top = 38
          Width = 97
          Height = 17
          Caption = #35753#29699#25351#25968
          TabOrder = 3
        end
        object chkBf: TCheckBox
          Left = 113
          Top = 38
          Width = 97
          Height = 17
          Caption = #27604#20998#25351#25968
          TabOrder = 4
        end
      end
      object chkAll: TCheckBox
        Left = 32
        Top = 48
        Width = 49
        Height = 17
        Caption = #20840#36873
        TabOrder = 4
        OnClick = chkAllClick
      end
    end
    object GroupBox2: TGroupBox
      Left = 8
      Top = 207
      Width = 617
      Height = 240
      Anchors = [akLeft, akTop, akRight, akBottom]
      Caption = #26085#24535
      TabOrder = 2
      ExplicitWidth = 594
      object Memo1: TMemo
        Left = 2
        Top = 15
        Width = 613
        Height = 223
        Align = alClient
        Lines.Strings = (
          'Memo1')
        ScrollBars = ssBoth
        TabOrder = 0
        ExplicitWidth = 524
        ExplicitHeight = 200
      end
    end
  end
  object Panel2: TPanel
    Left = 631
    Top = 0
    Width = 117
    Height = 452
    Align = alRight
    TabOrder = 1
    ExplicitLeft = 542
    ExplicitHeight = 361
    object btnExec: TButton
      Left = 24
      Top = 49
      Width = 75
      Height = 25
      Caption = #25191#34892
      TabOrder = 0
      OnClick = btnExecClick
    end
    object btnExit: TButton
      Left = 24
      Top = 400
      Width = 75
      Height = 25
      Caption = #36864#20986
      TabOrder = 1
      OnClick = btnExitClick
    end
  end
end
