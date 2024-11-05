
---

# HARMONIE Dataset Description

## Abstract

HARMONIE information in gridded form (regular lat-lon) of near surface and boundary layer (up to 300 m) parameters from the UWC-West HARMONIE-AROME Cy43 model. For this weather forecast model, KNMI works closely with Iceland, Denmark, and Ireland on local short-term weather forecasts under the name "United Weather Centres-West" (UWC-West). An international project team is working on a joint Numerical Weather Prediction model (NWP), procurement, and management of the HPC (supercomputer) and infrastructure. The output frequency is 1 hour.

## Documentatie Harmonie

Het KNMI beschikt over een eigen weermodel HARMONIE (HIRLAM ALADIN Research on Mesoscale Operational NWP in Euromed) dat sinds 2012 beschikbaar is. Ontstaan uit samenwerking tussen ALADIN en HIRLAM consortia binnen grote Europese samenwerkingsprojecten, is HARMONIE ontworpen speciaal voor de korte termijn weersverwachtingen. Gebruikmakend van het AROME-model van Météo-France voor resoluties tot 2,5 km, versterkt het KNMI zijn voorspellingscapaciteiten.

Het KNMI is op 1 maart 2013 na een testperiode van een jaar begonnen met operationele prognoseruns met het niet-hydrostatische convectie-toelaatbare HARMONIE-model. In 2024 wordt er een flinke update van HARMONIE verwacht. Houdt de nieuwsbrieven in de gaten voor meer informatie.

Voor weersverwachtingen kunt u de numerieke modeluitvoer HARMONIE-AROME gebruiken. Hierbij worden de verwachte parameters voor 48 uur vooruit gegeven. Deze dataset is niet voor alleen de Bilt, maar een generieke uitvoer. Gezien ons wettelijk kader bieden wij een specifieke verwachting, op locatie, niet aan.

## Technische gegevens

- **Rekenrooster:** Lambertprojectie
- **Product resolutie:** 0,037° west-oost en 0,023° noord-zuid (300x300 punten)
- **Grid representatie:** Regulier Lat/Lon
- **Gebiedsdefinitie:** noord 55,877° N.B. zuid 49,0° N.B. / oost 11,063° O.L. en west 0,0° W.L.
- **Tijdstappen:** +00u (+1u) +48u

## Parameters

| Afkorting | Parameter beschrijving                | Code | Leveltype | Level  | TRI | Units |
|-----------|--------------------------------------|------|-----------|--------|-----|-------|
| PMSL      | Luchtdruk herleid tot zeeniveau       | 1    | 103       | 0      | 0   | Pa    |
| PSRF      | Luchtdruk aan het modeloppervlak      | 1    | 105       | 0      | 0   | Pa    |
| GEOP      | Oppervlakte geopotentiaal             | 6    | 105       | 10     | 0   | m²/s² |
| 2T        | Luchttemperatuur 2 m                  | 11   | 105       | 2      | 0   | K     |
| TSRF      | Oppervlakte temperatuur               | 11   | 105       | 10     | 0   | K     |
| 2TD       | Dauwpuntstemperatuur 2 m              | 17   | 105       | 2      | 0   | K     |
| VIS       | Zicht aan het oppervlak               | 20   | 105       | 0      | 0   | m     |
| U10       | U-wind component 10 m                 | 33   | 105       | 10     | 0   | m/s   |
| V10       | V-wind component 10 m                 | 34   | 105       | 10     | 0   | m/s   |
| 2RH       | Relatieve luchtvochtigheid            | 52   | 105       | 2      | 0   | %     |
| SC        | Snowcover                             | 66   | 105       | 0      | 0   | kg/m² |
| BLH       | Boundary layer height                 | 67   | 105       | 0      | 0   | m     |
| TCC       | Totale hoeveelheid bewolking          | 71   | 105       | 0      | 0   | %     |
| LCC       | Low Cloud Cover (surface to 748 hPa)  | 73   | 105       | 0      | 0   | %     |
| MCC       | Medium Cloud Cover (748 to 424 hPa)   | 74   | 105       | 0      | 0   | %     |
| HCC       | High Cloud Cover (above 424 hPa)      | 75   | 105       | 0      | 0   | %     |
| SWR       | Net shortwave radiation               | 111  | 105       | 0      | 4   | J/m²  |
| LWR       | Net long wave radiation               | 112  | 105       | 0      | 4   | J/m²  |
| GR        | Global Radiation                      | 117  | 105       | 0      | 4   | J/m²  |
| SH        | Sensible heat flux                    | 122  | 105       | 0      | 4   | J/m²  |
| LH        | Latent heatflux                       | 132  | 105       | 0      | 4   | J/m²  |
| UWG       | U-component max windstoot             | 162  | 105       | 10     | 2   | m/s   |
| VWG       | V-component max windstoot             | 163  | 105       | 10     | 2   | m/s   |
| INR       | Intensiteit regen                     | 181  | 105       | 0      | 0   | kg/m²s|
| CR        | Cumulatieve som regen                 | 181  | 105       | 0      | 4   | kg/m² |
| INS       | Intensiteit sneeuw                    | 184  | 105       | 0      | 0   | kg/m²s|
| CS        | Cumulatieve som sneeuw                | 184  | 105       | 0      | 4   | kg/m² |
| CLB       | Wolkenbasis                           | 186  | 200       | 0      | 0   | m     |
| ING       | Intensiteit graupel                   | 201  | 105       | 0      | 0   | kg/m²s|
| CG        | Cumulatieve som graupel               | 201  | 105       | 0      | 4   | kg/m² |
| CIG       | Column integrated graupel             | 201  | 200       | 0      | 0   | kg/m² |
| U         | U-wind op hoogte                      | 33   | 105       | 50,100,200,300 | 0 | m/s|
| V         | V-wind op hoogte                      | 34   | 105       | 50,100,200,300 | 0 | m/s|
| T         | Temperatuur op hoogte                 | 11   | 105       | 50,100,200,300 | 0 | K  |

*TRI = Time Range Indicator, 0=instantaneous, 2=sum/max over past hour, 4=accumulated during forecast.*

---

## GRIB Codes for Harmonie Cy43 P1

| Code | Afkorting | Parameter beschrijving                             | Units      | Leveltype | Level                  | TRI |
|------|----------|----------------------------------------------------|------------|-----------|------------------------|-----|
| 1    | PMSL     | Pressure altitude above mean sea level             | Pa         | 103       | 0                      | 0   |
| 1    | PSRF     | Pressure height above ground                       | Pa         | 105       | 0                      | 0   |
| 6    | GP       | Geopotential                                       | m² s⁻²      | 105       | 0                      | 0   |
| 11   | TMP      | Temperature                                        | K          | 105       | 0, 2, 50, 100, 200, 300 | 0   |
| 11   | TMP      | Temperature                                        | K          | 100       | 100, 200, 300          | 0   |
| 17   | DPT      | Dew-point temperature                              | K          | 105       | 2                      | 0   |
| 20   | VIS      | Visibility                                         | m          | 105       | 0                      | 0   |
| 33   | UGRD     | u-component of wind                                | m s⁻¹       | 100       | 100, 200, 300          | 0   |
| 33   | UGRD     | u-component of wind                                | m s⁻¹       | 105       | 10, 50, 100, 200, 300  | 0   |
| 34   | VGRD     | v-component of wind                                | m s⁻¹       | 100       | 100, 200, 300          | 0   |
| 34   | VGRD     | v-component of wind                                | m s⁻¹       | 105       | 10, 50, 100, 200, 300  | 0   |
| 52   | RH       | Relative humidity                                  | %          | 105       | 2                      | 0   |
| 61   | APCP     | Total precipitation                                | kg m⁻²     | 105       | 0                      | 4   |
| 65   | WEASD    | Water equivalent of accumulated snow depth         | kg m⁻²     | 105       | 0                      | 0   |
| 67   | MIXHT    | Mixed layer depth                                  | m          | 105       | 0                      | 0   |
| 71   | TCDC     | Total cloud cover                                  | %          | 105       | 0                      | 0   |
| 73   | LCDC     | Low cloud cover                                    | %          | 105       | 0                      | 0   |
| 74   | MCDC     | Medium cloud cover                                 | %          | 105       | 0                      | 0   |
| 75   | HCDC     | High cloud cover                                   | %          | 105       | 0                      | 0   |
| 81   | LAND     | Landcover                                          | Proportion | 105       | 0                      | 0   |
| 111  | NSWRS    | Net short-wave radiation flux (surface)            | W m⁻²      | 105       | 0                      | 4   |
| 112  | NLWRS    | Net long-wave radiation flux (surface)             | W m⁻²      | 105       | 0                      | 4   |
| 117  | GRAD     | Global radiation flux                               | W m⁻²      | 105       | 0                      | 4   |
| 122  | SHTFL    | Sensible heat flux                                  | W m⁻²      | 105       | 0                      | 4   |
| 132  | LHTFL    | Latent heat flux through evaporation                | W m⁻²      | 105       | 0                      | 4   |
| 162  | CSULF    | U-momentum of gusts out of the model                | m s⁻¹       | 105       | 10                     | 2   |
| 163  | CSDLF    | V-momentum of gusts out of the model                | m s⁻¹       | 105       | 10                     | 2   |
| 181  | LPSX     | (Cumulative sum) Rain                               | kg m⁻²     | 105       | 0                      | 4   |
| 181  | LPSX     | Rain                                               | kg m⁻²     | 105       | 0                      | 0   |
| 184  | HGTY     | (Cumulative sum) Snow                               | kg m⁻²     | 105       | 0                      | 4   |
| 184  | HGTY     | Snow                                               | kg m⁻²     | 105       | 0                      | 0   |
| 186  | ICNG     | Cloud base                                         | m          | 200       | 0                      | 0   |
| 201  | ICWAT    | (Cumulative sum) Graupel                            | kg m⁻²     | 105       | 0                      | 4   |
| 201  | ICWAT    | Graupel                                             | kg m⁻²     | 105       | 0                      | 0   |
| 201  | ICWAT    | (Column integrated) Graupel                        | kg m⁻²     | 200       | 0                      | 0   |

Hier is een overzicht van de GRIB codes voor HARMONIE Cy43 P1. Code is de indicatorOfParameter variabele, LevelType is terug te vinden als indicatorOfTypeOfLevel, en TRI staat voor timeRangeIndicator. Voor LevelType en TRI is onderaan de pagina uitleg wat ze betekenen.

LevelType

| Level type | WMO/HIRLAM type definition | Units |
|------------|---------------------------|--------|
| 100 | Isobaric level | hPa |
| 103 | Specified altitude above mean sea level | Altitude in m |
| 105 | Specified height above ground | Altitude in m |
| 109 | Hybrid level | |
| 200 | Entire atmosphere (considered as a single layer) | |


TRI (TimeRangeIndicator)

| Time Range Indicator | Range |
|---------------------|-------|
| 0 | Instantaan |
| 2 | Geaccumuleerd over beperkte periode |
| 4 | Geaccumuleerd over hele forecast periode |