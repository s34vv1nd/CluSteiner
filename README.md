# Shortest Path Genetic Algorithm (SPGA)

## Le Minh Hai Phong - 20170221

### School of Information and Communication Technology, Hanoi University of Science and Technology

#
This project is divided into two parts: the source code and result analysis code.

## 1. Source code (\src)
This folder contains code of the algorithms. Follows these steps to produce output files:
1. Download input files

    Download input files to folder "\input_data". These files can be found at: 

    [github-link](https://github.com/s34vv1nd/CluSteiner/tree/master/input_data)



2. Run tests

    Use following command in terminal to run all tests in input folder, with ALGORITHM being 0/1/2 corresponding to SPGA/RSPH/SPMST:
    > python src/tests.py ALGORITHM

## 2. Result Analysis (\result_analysis)
This folder contains code to analyse results.
1. Install requirements
    > pip install -r result_analysis\requirements.txt

2. Fetch result

    Run the [fetch_results.ipynb](\result_analysis\fetch_results.ipynb)

3. Analyse PI and RPD

    Run the [results_analysis.ipynb](\result_analysis\results_analysis.ipynb)

4. Analyse non-parametric statistics

    Read [instructions.pdf](\result_analysis\controlTest\instructions.pdf)

## The full project are at: [github](https://github.com/s34vv1nd/CluSteiner)