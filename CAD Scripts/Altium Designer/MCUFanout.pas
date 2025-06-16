var
  DebugModeEnabled : Boolean;
  MCUType : String;                   // the prefix of the 'comment' property of the MCU component
  FanOutLength : Integer;             // length of fan out wires, in mils
  PinOutFilePath : String;            // path to pinout.csv
  PinDictionary : TStringList;        // list of name-value pairs that storage pin designators and functions

// read pinout.csv into PinDictionary
procedure LoadPinoutCSV;
var
  CSVLine: String;
  CSVFile: TStringList;
  LineComponents: TStringList;
  i: Integer;
begin
  PinDictionary := TStringList.Create;

  if not FileExists(PinOutFilePath) then
  begin
    ShowMessage('Cannot found pinout.csv under' + PinOutFilePath);
    Exit;
  end;

  CSVFile := TStringList.Create;
  LineComponents := TStringList.Create;
  try
    CSVFile.LoadFromFile(PinOutFilePath);

    for i := 1 to CSVFile.Count - 1 do
    begin
      CSVLine := CSVFile[i];
      LineComponents.StrictDelimiter := True;
      LineComponents.Delimiter := ','; 
      LineComponents.DelimitedText := CSVLine;
      if LineComponents[3] <> '' then
        PinDictionary.Add(LineComponents[0] + '=' + LineComponents[3]);
    end;

    if DebugModeEnabled then
      ShowMessage('pinout.csv Loaded, with ' + IntToStr(PinDictionary.Count) + ' items');

  finally
    CSVFile.Free;
    LineComponents.Free;
  end;
end;

// the main procedure
procedure FanOutMCUPins;
var
  CurrentSchDoc: ISch_Document;                   // from which the "Run Script" command is executed

  CompIterator: ISch_Iterator;                     // used to iterate components on CurrentSchDoc
  Component: ISch_Component;                      // component iterated by CompIterator
  PinIterator: ISch_Iterator;                     // used to iterate pin within Component
  Pin: ISch_Pin;                                  // pin iterated by PinIterator
  PinDesignator: String;                          // designator of Pin
  PinFullDesignator: String;                      // full designator with part id (i.e. U1A-A4), used to check whether the iterated pin belongs to the current part of Component
  PinFunction: String;                            // function of Pin, read from PinDictionary

  Wire: ISch_Wire;                                // the fanout wire to be created
  StartX, StartY, EndX, EndY: Integer;            // the absolute location of Wire
  NetLabel: ISch_Netlabel;                        // labeling the function of the pin connected to Wire
  NetLabelJustification: TTestJustification;      // justification of NetLabel

  IsFound: Boolean;                               // flag indicating whether an MCU component is found
  i: Integer;

begin
  LoadPinoutCSV;

  if SchServer = nil then
  begin
    ShowMessage('SchServer not found, aborted!');
    Exit;
  end;

  CurrentSchDoc := SchServer.GetCurrentSchDocument;
  if CurrentSchDoc = nil then
  begin
    ShowMessage('Current document is not SchDoc, aborted!');
    Exit;
  end;

  CompIterator := CurrentSchDoc.SchIterator_Create;
  CompIterator.AddFilter_ObjectSet(MkSet(eSchComponent));      // let CompIterator read the component objects only

  IsFound := False;
  Component := CompIterator.FirstSchObject;                    // iterate the components
  while Component <> nil do
  begin
    if (Component.Comment <> nil) and (Copy(Component.Comment.Text, 1, Length(MCUType)) = MCUType) then
    begin
      IsFound := True;
      if DebugModeEnabled then
        ShowMessage('Found: ' + Component.Designator.Text + ', part count: ' + IntToStr(Component.PartCount) + ' current part: ' + IntToStr(Component.CurrentPartID));

      PinIterator := Component.SchIterator_Create;
      PinIterator.AddFilter_ObjectSet(MkSet(ePin));
      Pin := PinIterator.FirstSchObject;                      // iterate the pins
      while Pin <> nil do
      begin
        if (DebugModeEnabled) then
          ShowMessage('Found pin:' + Pin.Designator + ' part:' + IntToStr(Pin.OwnerSchComponent.GetState_CurrentPartID) + ' ishidden: ' + IntToStr(Pin.IsHidden));

        // AD's API SUCKS !!!!
        // for a multi-part component, every part will be iterated once by CompIterator
        // and for every part, EVERY pin of the component will be iterated by PinIterator, no matter the pin belongs to the current part or not.
        // For those pins not belonged to the current part, its Location will be read as the topleft pin of this part, which means overlapping.
        // The current solution is to check the full designator of every pin,
        // and see if the part id (e.g. A/B/C...) meets with CurrentPartID of Component.
        
        PinFullDesignator := Pin.FullDesignator;
        if (Component.IsMultiPartComponent) and ( Ord(Copy(PinFullDesignator, Pos('-',PinFullDesignator) - 1, 1)) - 64 <> Component.CurrentPartID) then      // 'A'=64, part A = part 1
        begin
          if DebugModeEnabled then
            ShowMessage('Skipped ' + PinFullDesignator + ' when iterates to part' + IntToStr(Component.CurrentPartID));
          Pin := PinIterator.NextSchObject;
          continue
        end;
          
        PinDesignator := Pin.Designator;
        PinFunction := PinDictionary.Values[PinDesignator];   // read function of the pin
        if PinFunction = '' then                              // filter out pins with no function
        begin
          Pin := PinIterator.NextSchObject;
          continue
        end;

        StartX := Pin.Location.X;                             // location of the root of the pin
        StartY := Pin.Location.Y;
        if Pin.Orientation = eRight then                      // eRight actually means the pin is pointing to the left (CRAZY)
        begin
          StartX := StartX - Pin.PinLength;                   // find the end of the pin
          EndX := StartX - MilsToCoord(FanOutLength);         // calculate the vertex of funout wire
          EndY := StartY;
          NetLabelJustification := eJustify_BottomLeft;
        end
        else if Pin.Orientation = eLeft then
        begin
          StartX := StartX + Pin.PinLength;
          EndX := StartX + MilsToCoord(FanOutLength);
          EndY := StartY;
          NetLabelJustification := eJustify_BottomRight;
        end;

        if (DebugModeEnabled) then
          ShowMessage('pin ' + PinDesignator + ' as ' + PinFunction + ' starts from (' + IntToStr(CoordToMILs(StartX)) + ',' + IntToStr(CoordToMILs(StartY)) + ')' + ' ends at (' + IntToStr(CoordToMILs(EndX)) + ',' + IntToStr(CoordToMILs(EndY)) + ')');

        Wire := SchServer.SchObjectFactory(eWire, eCreate_GlobalCopy);        // create and configure the wire
        Wire.Location := Point(StartX, StartY);
        Wire.InsertVertex := 1;
        Wire.SetState_Vertex(1, Point(StartX, StartY));
        Wire.InsertVertex := 2;
        Wire.SetState_Vertex(2, Point(EndX, EndY));
        CurrentSchDoc.RegisterSchObjectInContainer(Wire);

        NetLabel := SchServer.SchObjectFactory(eNetlabel,eCreate_GlobalCopy);   // create and configure the net label
        NetLabel.Location := Point(EndX, EndY);
        NetLabel.Text := PinFunction;
        NetLabel.SetState_Justification(NetLabelJustification);
        CurrentSchDoc.RegisterSchObjectInContainer(NetLabel);

        Pin := PinIterator.NextSchObject;
      end;

      //break;
    end;
    Component := CompIterator.NextSchObject;
  end;

  if not IsFound then
  begin
    ShowMessage('Not Found!');
  end;

  PinDictionary.Free;
end;

procedure TForm1.Button_RunClick(Sender: TObject);
begin
  PinOutFilePath := Box_Path.Text;
  FanOutLength := StrToInt(Box_FanOutLength.Text);
  MCUType := Box_MCUType.Text;
  if CheckBox_DebugMode.State = cbChecked then          // not sure if it is the only way to do an if-else
  begin                                                 // Delphi is fucking nonsense to me
    DebugModeEnabled := True;
  end
  else
  begin
    DebugModeEnabled := False;
  end;

  FanOutMCUPins;
  Close;
end;

procedure TForm1.Form_Create(Sender: TObject);
var
  ProjectDir : String;
begin
  ProjectDir := ExtractFilePath(GetWorkspace.DM_FocusedProject.DM_ProjectFullPath);
  Box_Path.Text := ProjectDir + 'pinout.csv';
end;