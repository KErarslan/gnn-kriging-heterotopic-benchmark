Raw data used in the GNN vs kriging benchmark (local copy; may be redistributed under GPL >= 2, see below).

jura/         Goovaerts (1997) Jura data, as served by the Python package geostats-datasets (v1.0.0):
              prediction.csv (259 calibration points) + validation.csv (100 points). Coordinates in km; metals in mg/kg.
walker_lake/  Isaaks & Srivastava (1989) Walker Lake data, via geostats-datasets (v1.0.0):
              sample.csv (470 points) and exhaustive.csv (78 000 grid nodes, 260 x 300 m).
meuse/        Meuse topsoil data (Rikken & Van Rijn 1993) from the R package sp (GPL >= 2):
              meuse.rda / meuse.grid.rda (original R files) and CSV conversions. Coordinates in m (RD New);
              the notebook divides them by 1000 (km).
Note: at 6 Walker Lake sample points the V value in sample.csv differs from exhaustive.csv; the notebook uses the exhaustive values.

Licence: Jura and Walker Lake are taken by geostats-datasets from the R package gstat and shared under GPL (>= 2);
Meuse comes from the R package sp, also GPL (>= 2). Redistribution is allowed under the same licence with attribution.

SHA256SUMS lists the checksums of these files; notebook CELL 1 verifies the Jura and Walker Lake files against them.
geostats-datasets is no longer installable from PyPI (checked October 2026); these copies are the reference.
