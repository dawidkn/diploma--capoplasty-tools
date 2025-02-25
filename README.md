# 📌 Femoral Head Axis Approximation Macro

**Author:** Dawid K.  
**Repository:** [diploma--capoplasty-tools](https://github.com/dawidkn/diploma--capoplasty-tools)  
**Code location:** `axis_aproximation-program/`  
**Software:** Siemens NX 12 (Macro)  
**Language:** Python (likely using NX Open API)  

---

## 📖 Program Description  

This macro automates the **approximation of the femoral head axis** using a section-based method in **Siemens NX 12**. The algorithm iteratively adjusts the direction of the axis by analyzing cross-sections and optimizing for minimal cross-sectional area.  

---

## 🔧 How It Works  

1. **Load the 3D model** – The macro reads the femoral head geometry.  
2. **Calculate the center of mass** – The object's center of gravity is determined, and the model is translated to `(0,0,0)`.  
3. **Initial cross-sections** – The script generates slices in the following planes:  
   - XY  
   - YZ  
   - ZX  
4. **Surface area measurement** – Each section’s surface area is calculated.  
5. **Optimal orientation search** – The slicing plane rotates iteratively around **X, Y, and Z axes** to find the smallest cross-section.  
6. **Axis correction iteration** – After determining the minimum cross-section, the macro moves along the perpendicular direction to refine the axis.  
7. **Re-optimization** – The correction step repeats, with further rotations and adjustments to the optimal plane direction.  
8. **Final output** – The femoral head axis is determined and can be used for further analysis.  

---

## 📂 Code Structure  


---

## 🛠 Installation & Usage  

### **Requirements**  
- Siemens NX 12 (with macro support)  
- Python API (NX Open, if applicable)  

### **Installation**  
1. Copy the `axis_aproximation-program` folder into your NX environment.  
2. Open **NX 12** and go to the **Macro** section.  
3. Load `main.py` as a macro script.  

### **Running the Macro**  
1. Open **NX 12**.  
2. Navigate to **Tools > Macros**.  
3. Select `main.py` and execute it.  
4. The results will be displayed in the NX console or exported to a file.  

---

## 📌 Planned Improvements  

✅ **Current Features:**  
- Center of mass calculation  
- Initial cross-section creation in primary planes  
- Iterative axis optimization  

🔜 **Future Enhancements:**  
- 📌 Improve axis optimization algorithm  
- 📌 Export results to CSV/STL format  
- 📌 Interactive axis visualization in NX  
- 📌 GUI for user-friendly operation  

---

## 📄 License  
This project is released under the **MIT License**, meaning it is free to modify and use without restrictions.  

---

## 🚀 How to Add This Documentation  

1. Open **Visual Studio Code**.  
2. Navigate to the `axis_aproximation-program/` folder.  
3. Create a new file named `README.md`.  
4. Copy and paste this documentation into the file.  
5. Save the file.  
6. Commit and push it to GitHub:  

## Changes History
