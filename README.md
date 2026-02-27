# Set-up guide
You'll need to:
1. Download the [zip](https://github.com/GB-MD/bearingtool/archive/refs/heads/main.zip), unzip and put it in the desired working folder
2. Download anaconda prompt [here](https://www.anaconda.com/download/success) (skip if you already have it installed)

Steps to get it to work:
1. Open anaconda prompt
2. Go to the directory, copy its path (see below)
3. Type `cd` and copy paste the path into the terminal


# Inputs
There are two interfaces for inputting parameters.

1. `config.yml`
2. The excel file containing the data

Edit the parameters in `config.yml` by opening it in notepad (or any text editor) and filling in the desired inputs.





# Running the code
###
Paste the following instructions on the miniconda terminal:

```
conda create env -f environment.yml
```
```
conda activate bearingtool
```
```
python main.py
```

Your results will be generated in the same directory in `results.xlsx`.