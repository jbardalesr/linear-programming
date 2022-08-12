# Linear Programming


### Config
In file `/root/.vscode/setting.json # CTRL+ SHIFT + P and select  Open Workspace Setting ` add this for vscode autocompletion.
```
{
    "python.analysis.extraPaths": ["${workspaceFolder}/.."]
}
```
For import in files `.ipynb` add the next lines
```
import sys
sys.path.insert(0, "..")
from algorithms.util import *
from algorithms.network_flows import *
```


### References
[1] Sierksma, Gerard, and Yori Zwols. *Linear and integer optimization: theory and practice.* CRC Press, 2015.