# WPT-Automation
Arquivos utilizados para a pesquisa Transmissão de Energia Sem Fio Através de Bobinas Ressonantes em Baixas Frequências.

## Description

This folder contains the final scrpit versions and utilities used for generating results and functional data analisys tools for the research of "Wireless Power Transfer Through Low Frequency Ressonating Coils".

Essa pasta contém as versões finais e utilitários usados para conseguir resultados e ferramentas funcionais para análises de dados para a pesquisa "Transmissão de Energia Sem Fio Através de Bobinas Ressonantes em Baixas Frequências".

For doubts and futher information, e-mail me on: <dantepedrosa@gmail.com>!

## Contents

The [`readme.md`](python_scripts/readme.md) file inside the folder explains the purposes of each of the other files inside, including:

- ``cleanup.py`` - A cleanup tool used to clear junk files from current folder, gererated in the simulations.  
[Go to section...](python_scripts/readme.md#cleanuppy) | [Open file...](python_scripts/cleanup.py)

- ``efficiency_calculation.py`` - Calculates the efficiency of a sigle FEMM file (*.fem) in the folder it's located and prints on result on terminal.   
[Go to section...](python_scripts/readme.md#efficiency_calculationpy) | [Open file...](python_scripts/efficiency_calculation.py)

- ``efficiency_calculation_lib.py`` - A library version of ``efficiency_calculation.py`` to be used by other main scripts.   
[Go to section...](python_scripts/readme.md#efficiency_calculation_libpy) | [Open file...](python_scripts/efficiency_calculation_lib.py)

- ``efficiency_v_diameter.py`` - A script for calculating the best combination of wire diameter and number of turns in a coil with a static cross section area that yields in the highest efficiency.  
[Go to section...](python_scripts/readme.md#efficiency_v_diameterpy) | [Open file...](python_scripts/efficiency_v_diameter.py)

- ``general_simulations.py`` - The gereral simulations file, used for creating simulations such as efficiency as a function of geometry cacacteristcs (area, lenght, distance and wire diameter) and circuit caracteristcs (current, frequency, wire type and load resistance) in one go.  
[Go to section...](python_scripts/readme.md#general_simulationspy) | [Open file...](python_scripts/general_simulations.py)
