# DLR_ICF  
This tutorial will introduce how to run DLR_ICF to analyze DLR and ICF.

### DLR_ICF can be used to analyze DLR and ICF based on normlazed Hi-C contact matrix.  
DLR: distal-to-local ratio  
ICF: inter-chromosomal fraction  

#### calculate the DIR and ICF for individual Hi-C contact matrix
#### usage: 
DLR_ICF_main [-h] [-b] -I INPUTPATH -f FILENAME -d DISTANCE -r RESOLUTION -O OUTPATH -c CHRSIZE -o OUTFILE 

optional arguments:  
|  |   |    |   |   |
|:----:|:-----:|:----:|:------:|:------:|  
| -h | --help |   || show this help message and exit |
| -b | --balanced |             |   | type of contact matrix (iced or balanced) |
| -I | INPUTPATH  | --inputpath | INPUTPATH |path of input file  |  
| -f | FILENAME   | --filename    | FILENAME |name of input file |
| -d | DISTANCE  | --distance |DISTANCE|the distance of distal chromation interactions|
| -r    |   RESOLUTION| --resolution | RESOLUTION| resolution of contact matrix  | 
| -O | OUTPATH    | --outpath |  OUTPATH |path of output file  |  
| -c | CHRSIZE    | --chrsize |  CHRSIZE |chromosome size file  |
| -o | OUTFILE    | --outfile |  OUTFILE |name of output file  |


#### compare the difference in the DIR and ICF for 2 Hi-C contact matrices.  
#### usage: 
DLR_ICF_comparison [-h] -i INPUTPATH -t TREATMENT -c CONTROL -r RESOLUTION -O OUTPATH -o OUTFILE  
 
optional arguments:  
|  |   |    |   |   |
|:----:|:-----:|:----:|:------:|:------:|  
|  -h    |   --help    |              |           | show this help message and exit         |
|  -i    |   INPUTPATH | --inputpath  | INPUTPATH | path of input file             |
|  -t    |   TREATMENT | --treatment  | TREATMENT | name of treatment file         |
|  -c    |   CONTROL   | --control    | CONTROL   | name of control file             |
|  -r    |   RESOLUTION| --resolution | RESOLUTION| resolution of contact matrix  | 
|  -O    |   OUTPATH   | --outpath    | OUTPATH   | path of output file              |
|  -o   |    OUTFILE   | --outfile    | OUTFILE   | name of output file              |

### Installation 
#### requirement for installation
python>=3.8  
numpy
pandas
argparse
cooler
import h5py

#### pip install DLR_ICF==1.0.0
https://pypi.org/project/DLR-ICF/1.0.0/

#### reference
Transcription Elongation Can Affect Genome 3D Structure (https://doi.org/10.1016/j.cell.2018.07.047)
