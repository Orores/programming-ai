In FreeCAD, you can automate repetitive tasks such as inserting specific text into the formula field using the built-in macro functionality. Below is a step-by-step guide on how to create a macro that inserts `<<Spreadsheet>>.B` and allows you to type a number afterward. Additionally, you can assign a hotkey to this macro for easy access.

### Step 1: Create the Macro

1. **Open FreeCAD**.
2. Go to the **Macro** menu and select **Macros...**.
3. In the dialog that appears, click on **Create**.
4. Give your macro a name, such as `InsertSpreadsheetFormula`, and click **Save**.
5. The macro editor will open. Replace any existing code with the following:

   ```python
   import FreeCAD
   import FreeCADGui

   def insertSpreadsheetFormula():
       # Get the active document
       doc = FreeCAD.ActiveDocument
       if doc is None:
           return

       # Get the active object
       selection = FreeCADGui.Selection.getSelection()
       if not selection:
           return

       # Get the active object's properties
       obj = selection[0]
       
       # Check if the object has a property that can accept a formula
       prop_name = FreeCADGui.ActiveDocument.ActiveObject.PropertyName
       
       # Insert the formula
       if prop_name:
           new_formula = "<<Spreadsheet>>.B"
           # Insert the formula into the property
           obj.setProperty(prop_name, new_formula)
           FreeCAD.ActiveDocument.recompute()

   insertSpreadsheetFormula()
   ```

6. **Save** the macro and close the editor.

### Step 2: Assign a Hotkey

1. Go to the **Tools** menu and select **Customize...**.
2. In the Customize dialog, go to the **Macro** tab.
3. Find your newly created macro (`InsertSpreadsheetFormula`) in the list.
4. Select it and then click on the **Add** button next to the **Shortcuts** section.
5. Press the desired hotkey combination you want to assign (for example, `Ctrl+M`).
6. Click **OK** to close the Customize dialog.

### Step 3: Use the Macro

1. Select the object in FreeCAD where you want to input the formula.
2. Press the hotkey you assigned to your macro.
3. After the macro runs, you can manually edit the formula to include the specific number by editing the property in the property editor.

### Note

This macro will insert `<<Spreadsheet>>.B` into the property of the selected object. You may need to manually edit the property value afterward to add the specific number you want. 

Make sure to adjust the macro if you want to target a specific property or behavior according to your needs.
