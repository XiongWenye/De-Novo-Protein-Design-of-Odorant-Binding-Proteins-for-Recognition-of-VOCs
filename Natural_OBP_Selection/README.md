# OBP-Selecting

This repository contains a Python script to analyze the binding affinities of various compounds to different OBP (Odorant Binding Proteins) and identify the best OBP combinations for specified target molecules based on a new scoring method.

## Requirements
- Python 3.6 or higher
- pandas library

## Usage
- Ensure you have the Compound_OBP_binding.csv file in the directory.
- Run the script
```sh
python OBP_Selecting.py
```

## Input Data Format
- The input CSV file Compound_OBP_binding.csv should have the following structure:
```
CAS-number,Compound name,AaegOBP22,AbamOBP28,AcerASP1,...
<value1>,<compound name1>,<binding value1>,<binding value2>,...
...
```

## Output 
The script will generate a CSV file Best_OBP_Combination.csv containing the best OBP combinations for the specified target molecules.
