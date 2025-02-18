# The Manufactoring facility

## Requirements
```ps
pip install -r requirements.txt
```

## Run the simulation
To run a simulation use the following command
```ps
python simulation/app.py
```

it will print the results of the simulation: ProductionLineId, items acepted, items, rejected, WorkstationId, avg fixing time, avg supply time, avg ws production time, and avg pl production time


## Generate a report
run the following command
```ps
./simulation/summary.bat
```
and it will generate an output file `output.csv`
