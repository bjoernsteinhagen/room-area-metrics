# Speckle Automate: Automated Room and Area KPI Calculation 🏢📊

## Automate for Area/Room Metrics Check 📐: 
Exploring how [Speckle Automate](https://www.speckle.systems/product/automate) can plug in to the architectural design process.

The function automates the process of checking Key Performance Indicators (KPIs) related to **Net Internal Area (NIA)** and **Gross Floor Area (GFA)**. It retrieves Revit model data, including `Objects.BuiltElements.Area` and `Objects.BuiltElements.Room`, and compares them against a given threshold.

- **Gross Floor Area (GFA)** = Taken from `Objects.BuiltElements.Area` where the string `Gross` is included
- **Net Internal Area (NIA)** = Taken from the remaining `Objects.BuiltElements.Area` but excluding usage designations from the `rooms_to_exclude`
- **KPI** = NIA/GFA

---

## **Code Overview** 🖥️

### **Functionality**
This Python script defines an automated function that computes and evaluates a **KPI** (Net Internal Area / Gross Floor Area) for rooms and areas within a model. Based on the results, it provides visual feedback to the user indicating whether the KPI meets the required threshold.

### **Key Components** 🏗️:
1. **FunctionInputs Class**:
   - `threshold`: A float representing the KPI threshold (default 0.8). Determines the minimum acceptable ratio of **NIA** to **GFA**.
   - `rooms_to_exclude`: A comma-separated string of room names that should be excluded from the NIA calculation. Default is `"Corridor, Elevator, Stair, Storage"`.

2. **automate_function**:
   - **Room Exclusion**: Derives a list of rooms to exclude from computation based on user input.
   - **Model Data Extraction**: Uses the `ModelDataExtractor` to extract **rooms** and **areas** from the model version.
   - **DataFrames**: Creates dataframes (`room_df`, `area_df`) for rooms and areas using `RoomData` and `AreaData` classes.
   - **Area Calculations**: Sums the **gross areas** and computes the percentage of **NIA** to **GFA**.
   - **Filtering and Mapping**: Filters and adjusts level names in the data (hacky section).
   - **Results Evaluation**: Classifies rooms as `skipped`, `failed`, or `passed` based on the KPI.

3. **Post-Processing**:
   - The rooms are visualized using **Speckle Automate's** context functions to attach colored feedback:
     - **Skipped**: Rooms excluded from the calculation.
     - **Failed**: Rooms with a KPI less than the threshold.
     - **Passed**: Rooms with a KPI greater than or equal to the threshold.

### **Post-Processing Actions**:
- For each category (skipped, failed, passed), relevant messages are attached to the model objects with visual overrides (e.g., color changes for easy identification).

---

### **Usage** 🚀:
1. Define the threshold and rooms to exclude in the **FunctionInputs**.
2. Assign the automation to a Speckle model. The automation is triggered by each new model version and the KPI for rooms and areas in your model are calculated.
3. Visual feedback is provided in the 3D model, showing color-coded rooms based on the KPI results:
   - **🟢 Green**: Passed KPI
   - **🔴 Red**: Failed KPI
   - **⚪ Gray**: Skipped rooms

---

### **Points to Consider** 💡:
1. **Temporary Code**: The filtering and mapping section is temporary (labeled as "hacky") and should be refactored in future releases.
   
2. **Visual Feedback**: The results are visualized in the 3D model using Speckle's `attach_info_to_objects` and `attach_error_to_objects`, making it easy to interpret the results.

3. **Refactoring**: While the logic works, further refactoring is needed to clean up temporary code and ensure modularity and maintainability.

---

### **Conclusion** 🎉:
This automation function simplifies the process of checking room and area KPIs for architectural models, reducing the need for manual calculations and enabling real-time feedback within the model. By integrating with **Speckle Automate**, this solution enhances collaboration and ensures design criteria are met without manual intervention.

