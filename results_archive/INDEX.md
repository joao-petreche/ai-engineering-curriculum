# Results Archive Index

## Overview
Central archive for all experimental results, outputs, and artifacts across the training curriculum. This folder preserves all outputs while keeping them organized and easily recoverable.

## Organization Structure

```
results_archive/
├── INDEX.md (este arquivo)
├── LOCATIONS_MAP.md (mapa de localizações originais)
└── por_categoria/
    ├── federated_learning/
    ├── optimization/
    ├── piml/
    └── outros/
```

## Mapping to Original Locations

See [LOCATIONS_MAP.md](LOCATIONS_MAP.md) for a complete map showing where each file was originally located and when it can be moved back.

## File Categories

### Federated Learning Results (Mes 10)
- Convergence plots and metrics
- Training results and outputs
- Located in: `Science AI Engineering/mes10_federated_learning/`
- Archived files: `federated_convergence_*.png`, `federated_results_*.csv`, `demo_output.txt`, `hybrid_demo.txt`

### Optimization Results (Mes 8)
- NSGA-II results (Pareto frontiers, convergence)
- Sensitivity analysis (Morris, Sobol)
- Constrained optimization solutions
- Located in: `Science AI Engineering/mes8_optimization/results/`

### Physics-Informed ML (Mes 4)
- Surrogate models (XGBoost, neural networks)
- Model training artifacts
- Located in: `Science AI Engineering/mes4_piml/`

## How to Use This Archive

1. **Finding a result**: Check `LOCATIONS_MAP.md` for the original location
2. **Recovering original location**: See recovery date in map
3. **Adding new results**: 
   - Create subdirectory in `results_archive/por_categoria/`
   - Update `LOCATIONS_MAP.md` with origin path and date
   - Optionally delete from original location once archived

## Batch Recovery Procedure

To move files back to their original locations:

```powershell
# Example: Restore federated learning results
$archiveRoot = "C:\Users\joaop\Downloads\FAPESP\Training_12Meses\results_archive"
$originPath = "C:\Users\joaop\Downloads\FAPESP\Training_12Meses\Science AI Engineering\mes10_federated_learning"

# Move files
Move-Item "$archiveRoot\federated_learning\*.png" $originPath
Move-Item "$archiveRoot\federated_learning\*.csv" $originPath
Move-Item "$archiveRoot\federated_learning\*.txt" $originPath
```

## Last Updated
Initial creation: 2026-01-17
