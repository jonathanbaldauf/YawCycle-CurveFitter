# YawCycle-CurveFitter

### PURPOSE:
An optimization script to fit yaw cycles and depth-of-penetration equations to a set of data.

<!-- Yaw Cycle -->
## Yaw Cycle

### Background:
Observing the flight and therefore the yaw cycle of a K.E. penetrator via instrumentation (such as high-speed cameras) can be immensely difficult for large caliber rounds and targets featuring learge explosions upon impact. Hence, more rudimentary means of tracking the penetrator's yaw cycle throughout the flight are used. Cardboard sheets are set up at various intervals between muzzle and target to capture the shape of the fins and rod of the penetrator as it pierces through the cardboard. Due to the destructive nature of the tests, the occasional yaw card may be too severely burned or destroyed thus producing no data. The program will provide the best fit given the yaw cards that produce readable data for each experiment.

### Instructions:
The magnitude and orientation of the yaw readings are recorded in an excel sheet like the sample workbook provided in this repository. (Note: This sample workbook contains manufactured data, not representative of real numbers obtained from experimentation). Fill out columns C, E, and F, highlighted in yellow with each yaw card's magnitude and orientation as well as the distance it is located downrange from the muzzle. Column G contains a user defined function (UDF) I wrote in VBA to convert mm of yaw into degrees of yaw however I removed that functionality and the conversion tables for security concerns. As a result, you will need to fill column G (instead of column E) - any number between 0 and 7 degrees of yaw is typical. Save the workbook and run "Solver.py" or the executable version "Solver.exe". You should now see the following app open up:

<img width="377" alt="yaw fit solver example" src="https://github.com/jonathanbaldauf/YawCycle-CurveFitter/assets/12901076/35459897-070d-4b09-b726-3c4c3abdc384">

Once the app is open...
*  Click "Load File" and navigate to "Yaw Fit Program Sample_Shot.xlsm"
*  From the drop-down menu, select the tab with the data you'd like to curve fit
*  Click "Select Equation" and verify that "Yaw Fit Equations" is selected
*  Hit "Solve" to run the program
*  You can click "Show Parameters" to see the optimized variables of the Yaw Fit Equations
*  Or click "Show Graphs" to cycle between different curve-fitted graphs overlaying the original data
*  A red dot is also mapped on the graphs to visually represent the yaw fit at the target distance

Alternatively, the optimized parameters are copied to your clipboard automatically. You can paste the results back into the Excel sheet in cells Y5:Y10. The Excel sheet should update with all the same graphs as were displayed in the python app.

<!-- Penetration Equations -->
## Penetration Equations

### Background:
A common metric for evaluating the efficiency of a penetrator is its P/L, or in other words, its depth of penetration over the penetrator length. Various expressions for determining P/L have been derived over the years, both theoretically and empiracally, but the most common formulas for penetration depth of monobloc penetrators were derived by two engineers Lanz and Odermatt. Army Research Lab published a brief unclassified report titled [An Overview of Novel Penetrator Technology](https://apps.dtic.mil/sti/pdfs/ADA387329.pdf) which outlines the derivations for some of the Lanz-Odermatt equations.

### Instructions:

<!-- Notes -->
## Notes
* I revamped the already existing yaw-fit Excel sheet by adding conversion tables for various penetrators and I wrote a small User Defined Function (UDF) in Excel VBA to automatically convert the mm of yaw (how the yaw cards are read) into degrees of yaw (a more understandable and workable metric). The UDF can be accessed via the Developer tab in the Excel workbook or a text copy is included in this repository.
* I must reiterate the data and values in the example spreadsheets are fake numbers that I made up to produce a realistic fit. They are not representative or to be interpreted as actual data from any particular shot or experiment.
