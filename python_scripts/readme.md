# FEMM / LTspice Automation for WPT FEM simulations

This folder contains the final scrpit versions and utilities used for generating results and functional data analisys tools for the research of "Wireless Power Transfer Through Low Frequency Ressonating Coils".

Essa pasta contém as versões finais e utilitários usados para conseguir resultados e ferramentas funcionais para análises de dados para a pesquisa "Transmissão de Energia Sem Fio Através de Bobinas Ressonantes em Baixas Frequências".

For doubts and futher information, e-mail me on: <dantepedrosa@gmail.com>!

## Contents

This file explains the purposes of each of the other files in this folder, including:

- ``cleanup.py`` - A cleanup tool used to clear junk files from current folder, gererated in the simulations.  
[Go to section...](##``cleanup.py``) | [Open file...](cleanup.py)

- ``efficiency_calculation.py`` - Calculates the efficiency of a sigle FEMM file (*.fem) in the folder it's located and prints on result on terminal.   
[Go to section...](#``efficiency_calculation.py``) | [Open file...](efficiency_calculation.py)

- ``efficiency_calculation_lib.py`` - A library version of ``efficiency_calculation.py`` to be used by other main scripts.   
[Go to section...](#``efficiency_calculation_lib.py``) | [Open file...](efficiency_calculation_lib.py)

- ``efficiency_v_diameter.py`` - A script for calculating the best combination of wire diameter and number of turns in a coil with a static cross section area that yields in the highest efficiency.  
[Go to section...](#efficiency_v_diameterpy) | [Open file...](efficiency_v_diameter.py)

- ``general_simulations.py`` - The gereral simulations file, used for creating simulations such as efficiency as a function of geometry cacacteristcs (area, lenght, distance and wire diameter) and circuit caracteristcs (current, frequency, wire type and load resistance) in one go.  
[Go to section...](#general_simulationspy) | [Open file...](general_simulations.py)



## ``cleanup.py``

A cleanup tool used to clear junk files from current folder, gererated in the simulations.  
[Open file...](cleanup.py)


## ``efficiency_calculation.py``

Calculates the efficiency of a sigle FEMM file (*.fem) in the folder it's located and prints on result on terminal.   
[Open file...](efficiency_calculation.py)


## ``efficiency_calculation_lib.py``

A library version of ``efficiency_calculation.py`` to be used by other main scripts.   
[Open file...](efficiency_calculation_lib.py)


## ``efficiency_v_diameter.py``

A script for calculating the best combination of wire diameter and number of turns in a coil with a static cross section area that yields in the highest efficiency.   
[Open file...](efficiency_v_diameter.py)

The logic of the script is as follows:

![Alt text](<Diagram - Diameter vs Current.png>)

## ``general_simulations.py``

The gereral simulations file, used for creating simulations such as efficiency as a function of geometry cacacteristcs (area, lenght, distance and wire diameter) and circuit caracteristcs (current, frequency, wire type and load resistance) in one go.  
[Open file...](general_simulations.py)