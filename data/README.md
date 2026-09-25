# Data

The data are not tracked in git. They are available from the authors on request.

## Folder layout expected by the notebooks

```
data/
├── raw/
│   ├── eta_daily/*.tif                   daily 30 m ETa, date (YYYY-MM-DD) in the file name
│   ├── sm_daily/SM<depth>/*.tif          soil moisture maps, depth = 30 ... 180 cm
│   ├── climate/Daily_AWS_data.xlsx       CoAgMet Akron station, one sheet per year (TIMESTAMP, PrecipTotal)
│   ├── yield/<YYYY>/<Field>_<YYYY>_Wheat.tif    kriged 5 m yield, bu/ac
│   ├── soil_rasters/<Property> (<a-b> cm).tif   e.g. "Clay (0-15 cm).tif", "pH (15-30 cm).tif"
│   ├── topography/DEM.tif, Aspect.tif, Curvature.tif, Slope.tif, TPI.tif
│   └── nitrogen/Nitrogen_<YYYY>.tif      nitrogen zone raster per year
├── processed/                            written by notebooks 01-02
└── model_input/
    ├── ASP/<Field>_<YYYY>_Wheat.csv      one table per field-year (notebook 03)
    └── BAU/<Field>_<YYYY>_Wheat.csv
```

Notebooks 04-06 only need `model_input/`. The file name gives the field and the year.

## Field-year tables

One row per 5 m yield pixel.

| Column | Description | Unit |
|---|---|---|
| `latitude`, `longitude` | pixel centre (projected coordinates of the yield raster) | m |
| `yield` | winter wheat yield (multiplied by 62.77 in the models to get kg/ha) | bu/ac |
| `Carbon`, `OM`, `pH (0-15 / 15-30 cm)` | soil carbon, organic matter, pH | g/kg, %, - |
| `Clay`, `Sand`, `Silt (0-15 ... 90-120 cm)` | soil texture in five layers | % |
| `Elevation`, `Aspect`, `Curvature`, `Slope`, `TPI` | topography from the RTK-GPS DEM | m, degree, -, degree, m |
| `Nitrogen` | nitrogen zone / applied rate | - |
| `ETa` | mean of the monthly ETa, October to April | mm/day |
| `SM 30 cm` ... `SM 180 cm` | mean of the monthly soil moisture, October to April | m³/m³ |
| `Precipitation` | accumulated precipitation, 1 October to 15 April (same for all pixels of a year) | mm |

ASP fields: S2, S4, S5, S6, SB1, SB4, SB5, SB7, SCD2, SCD3, SCD5, SCD6.
BAU fields: S3, S7, SB3, SB6, SCD4, SCD7.
