object Form1: TForm1
  Left = 0
  Top = 0
  BorderStyle = bsDialog
  Caption = 'FindSTM32pins'
  ClientHeight = 360
  ClientWidth = 500
  Color = clBtnFace
  DefaultMonitor = dmMainForm
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -19
  Font.Name = 'Tahoma'
  Font.Style = []
  KeyPreview = True
  OldCreateOrder = False
  Position = poMainFormCenter
  OnCreate = Form_Create
  OnKeyUp = Form1KeyUp
  PixelsPerInch = 168
  TextHeight = 23
  object Label_Path: TLabel
    Left = 10
    Top = 10
    Width = 93
    Height = 23
    Caption = 'Pinout File:'
  end
  object Label_FanOutLength: TLabel
    Left = 10
    Top = 43
    Width = 129
    Height = 23
    Caption = 'Fanout Length:'
  end
  object Label_MCUType: TLabel
    Left = 10
    Top = 76
    Width = 92
    Height = 23
    Caption = 'MCU Type:'
  end
  object Label_DebugMode: TLabel
    Left = 10
    Top = 109
    Width = 115
    Height = 23
    Caption = 'Debug Mode:'
  end
  object Box_Path: TEdit
    Left = 170
    Top = 10
    Width = 320
    Height = 31
    TabOrder = 1
  end
  object Box_FanOutLength: TEdit
    Left = 170
    Top = 43
    Width = 320
    Height = 31
    TabOrder = 2
    Text = '1000'
  end
  object Box_MCUType: TEdit
    Left = 170
    Top = 76
    Width = 320
    Height = 31
    TabOrder = 4
    Text = 'STM32'
  end
  object CheckBox_DebugMode: TCheckBox
    Left = 170
    Top = 109
    Width = 23
    Height = 23
    TabOrder = 3
  end
  object Button_RunClick: TButton
    Left = 10
    Top = 230
    Width = 480
    Height = 100
    Margins.Left = 5
    Margins.Top = 5
    Margins.Right = 5
    Margins.Bottom = 5
    Caption = 'Run'
    Default = True
    ModalResult = 1
    TabOrder = 0
    OnClick = Button_RunClick
  end
end
