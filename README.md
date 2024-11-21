# Speckle Automate: Automated Room and Area KPI Calculation 🏢📊

> ⚠️ **Important Notice: Proof of Concept** ⚠️  
> 
> This repository contains **proof-of-concept code** designed specifically for a demo example. While the current implementation demonstrates the core functionality, **it is not production-ready**. Key areas such as **exception handling** and **mismatched floor handling** require improvements for future developments.  
> 
> We welcome contributions and ideas from the community! If you're interested in enhancing or building upon this example, feel free to join the discussion on the [Speckle Community Forum](https://speckle.community/).

## Prerequisites 📋:

- The model is assumed to be sent from **Revit**
- The Speckle model must contain the following types: `Objects.BuiltElements.Area` and `Objects.BuiltElements.Room`
  - `Objects.BuiltElements.Area` is used for the numeric evaluation of the KPIs. Ensure that each level has an `Area` with the substring `Gross` in its name, which represents the gross area of that level.
  - `Objects.BuiltElements.Room` is used for visualizations of the results. This does not affect the calculations, however, serve as a mode to view and interrogate results. Mapping between the two types is done on a `level` and `name` basis.
 
<img width="1200" alt="image" src="https://github.com/user-attachments/assets/5c197a7a-f2cf-4046-b872-fbea892e07a3">

- Using the automation resuts, we can interrogate which levels passed (first screenshot) or which rooms were ignored as per user input (second screenshot).

<img width="1200" alt="image" src="https://github.com/user-attachments/assets/7a857a05-4e27-44cd-a990-cfa4a82872ef">
<img width="1200" alt="image" src="https://github.com/user-attachments/assets/483a2f5a-6c18-4775-9b61-1b13e060ad10">


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
   - `levels_to_exclude`: A comma-separated string of levels that should be excluded from the entire calculation. 

2. **automate_function**:
   - **Room Exclusion**: Derives a list of rooms to exclude from computation based on user input.
   - **Model Data Extraction**: Uses the `ModelDataExtractor` to extract **rooms** and **areas** from the model version.
   - **DataFrames**: Creates dataframes (`room_df`, `area_df`) for rooms and areas using `RoomData` and `AreaData` classes.
   - **Area Calculations**: Sums the **gross areas** and computes the percentage of **NIA** to **GFA**.
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
1. Define the threshold and rooms and levels to exclude in the **FunctionInputs**.
2. Assign the automation to a Speckle model (ensure the model has all required object types and inputs). The automation is triggered by each new model version and the KPI for rooms and areas in your model are calculated.
3. Visual feedback is provided in the 3D model, showing color-coded rooms based on the KPI results:

---

### **Conclusion** 🎉:
This automation function simplifies the process of checking room and area KPIs for architectural models, reducing the need for manual calculations and enabling real-time feedback within the model. By integrating with **Speckle Automate**, this solution enhances collaboration and ensures design criteria are met without manual intervention.

