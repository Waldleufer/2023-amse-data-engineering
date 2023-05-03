# Project Plan

## Summary

<!-- Describe your data science project in max. 5 sentences. -->
This projects analyzes the hourly correlation between amount of measured bikers at a stationary counter in Constance, the measured weather at the given counter and the hourly border crossings. Is there less border crossings on sunny days? Is there less border crossings on days where many bikers ar on the roads in Constance? Or is there no meaningful correlation at all?

## Rationale

<!-- Outline the impact of the analysis, e.g. which pains it solves. -->
The analysis will correlate the measured amount of bike users in Constance with the weather at the given date and the pkw boarder crossings between Germany and Swiss at the same given date over the course of one year, to find out if there are any meaningful correlations. As the three measured border crossings do all lead through Constance this should give a good idea about the amount of vehicles on the road. The hourly counting of vehicles since 2020 at these border crossings will improve the precision of the generated result.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Border crossings motor vehicles Germany and Switzerland
* Metadata URL: https://mobilithek.info/offers/-6759756997530398389
* Data URLs: 
  - https://offenedaten-konstanz.de/sites/default/files/GZ_Grenzverkehr_Jul.%202020-Dez.2021.csv
  - https://offenedaten-konstanz.de/sites/default/files/TPZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv
  - https://offenedaten-konstanz.de/sites/default/files/EmZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv
  - https://offenedaten-konstanz.de/sites/default/files/DTV-Grenzverkehr%20KN-Kreuzlingen%202013-2020_0.csv
* Data Type: CSV
<details>
  <summary> Data Details </summary>

  
<p><strong>Die Koordinaten der Zollstellen:</strong></p>
<ul>
<li>Emmishofer Zoll: UMT = 512'684, 5'278'078; lat/lon = 47°39′21.517″N 9°10′08.096″E</li>
<li>GZA Kreuzlingen/Tägerwilen: UMT = 513'022, 5'277'985; lat/lon = 47°39′18.458″N 9°10′24.273″E</li>
<li>Tägerwilen-Paradieser Tor: UMT = 511'992, 5'278'865; lat/lon = 47°39′47.045″N 9°09′34.995″E </li>
</ul>
<p><strong>Spaltenerklärung:</strong></p>
<ul>
<li>EmZD = Anzahl der Kraftfahrzeuge nach Deutschland am Emmishofer Zoll</li>
<li>EmZCH = Anzahl der Kraftfahrzeuge in die Schweiz am Emmishofer Zoll</li>
<li>GZAD = Anzahl der Kraftfahrzeuge nach Deutschland an der Gemeinschaftszollanlage Kreuzlingen/Tägerwilen</li>
<li>GZACH = Anzahl der Kraftfahrzeuge in die Schweiz an der Gemeinschaftszollanlage Kreuzlingen/Tägerwilen</li>
<li>TPZD = Anzahl der Kraftfahrzeuge nach Deutschland an der Zollstelle Tägerwilen-Paradieser Tor</li>
<li>TPZCH= Anzahl der Kraftfahrzeuge in die Schweiz an der Zollstelle Tägerwilen-Paradieser Tor </li>
</ul>
</details>

<details>
<summary>The Swiss cantonal authority of Thurgau and the Swiss Federal Roads Office (ASTRA) collect the average daily traffic volume (DTV) of motor vehicles crossing the border at the three customs posts "Tägerwilen-Paradieser Tor", "Emmishofer Zoll" and the "Gemeinschaftszollanlage Kreuzlingen/Tägerwilen (GZA for short)".
</summary>
  
#### Further information
Since 2013, this data has been collected and is now also made available as open data. These data are also available in the [Open Data Portal of the Canton of Thurgau](https://map.geo.tg.ch/apps/mf-geoadmin3/?lang=de&topic=ech&catalogNodes=10000,20000,30000,15100,34000&layers=richtplankt50k_hauptverkehrstrassen,richtplankt200k_motorfahrzeugverkehr,strassenverkehrszaehlung_messdaten&layers_opacity=0.9,1,1&E=2728994.19&N=1280640.14&zoom=6&layers_timestamp=,,20130101&layers_visibility=true).

Note: The city of Constance explicitly did not collect the data.

#### Data source:

[Open Data Constance](https://offenedaten-konstanz.de/dataset/grenz-berg-nge-kraftfahrzeuge-deutschland-schweiz) under CC-BY 4.0

</details>


### Datasource2: Bicycle permanent counting stations Constance
* Metadata URL: https://mobilithek.info/offers/-7161835583190029268
* Data URLs: 
  - https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2018_stuendlich_Wetter.csv
  - https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2019_stuendlich_Wetter.csv
  - https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2020_stuendlich_Wetter.csv
  - https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2021_stuendlich_Wetter.csv
* Handy visualisation URL: https://www.bicycle-data.de/city-analysis/
* Data Type: CSV

<details>
  <summary> Data Details </summary>

  
<p>Der Datensatz enthält die Messergebnisse der Fahrradzählungen aller städtischen Dauerzählstellen im Konstanzer Stadtgebiet. Mit diesen Daten kann genau festgestellt werden, wann wie viele Radfahrerinnen und Radfahrer an diesen Orten unterwegs gewesen sind. Die Messergebnisse sind im stündlichen Rhythmus erfasst. Da dieser Datensatz  die damaligen Wetterdaten enthält, können spannende Zusammenhänge zwischen Wetter und Fahrradnutzung aufgedeckt werden.</p>
<p>Die Daten der Fahrradzählstelle im Herosépark werden von der französischen Herstellerfirma Eco Counter erhoben. Die Wetterdaten stammen von <a href="http://www.worldweatheronline.com" target="_blank">www.worldweatheronline.com</a> </p>
<p>Der Spaltenaufbau dieser Ressource bestimmt sich nach dem folgenden Schema:</p>
<ul>
<li>Zeit: Datum (DD.MM.JJJJ)</li>
<li>Uhrzeit (HH:MM)</li>
<li>Fahrradbruecke: Anzahl RadverkehrsteilnehmerInnen gesamt (Zahl)</li>
<li>Fahrradbruecke stadteinwaerts: Anzahl RadverkehrsteilnehmerInnen stadteinwärts (Zahl) (linksrheinisches Gebiet)</li>
<li>Fahrradbruecke stadtauswaerts: Anzahl RadverkehrsteilnehmerInnen stadtauswärts (Zahl)</li>
<li>Symbol Wetter: Kategorisierung Wetter in Sonnig, Leicht bewölkt, Bewölkt, Bedeckt, Leichter Nebel, Stellenweiser Nieselregen, Nieselregen, Stellenweiser leichter Regenfall, Leichter Regenschauer, Stellenweiser Regenfall, Stellenweise Gewitter und Niederschläge, Mäßiger Regenfall, Teilweise mäßiger Regenfall, Mäßiger bis starker Regenschauer</li>
<li>Temperatur: Gemessene Temperatur zum gemessenen Zeitpunkt in Grad Celsius </li>
<li>Gefühlte Temperatur: Wahrgenommene Umgebungstemperatur, die sich aufgrund verschiedener Faktoren von der gemessenen Lufttemperatur unterscheiden kann. Es handelt sich um ein bioklimatisches Maß für das thermische Wohlbefinden. Die nach dem Hitzindex gemessene gefühlte Temperatur zum gemessenen Zeitpunkt in Grad Celsius   </li>
<li>Regen (mm): Niederschlag zum Zeitpunkt in Millimeter </li>
</ul>
</details>

<details>
<summary>The Swiss cantonal authority of Thurgau and the Swiss Federal Roads Office (ASTRA) collect the average daily traffic volume (DTV) of motor vehicles crossing the border at the three customs posts "Tägerwilen-Paradieser Tor", "Emmishofer Zoll" and the "Gemeinschaftszollanlage Kreuzlingen/Tägerwilen (GZA for short)".
</summary>
  
#### Further information
Since 2013, this data has been collected and is now also made available as open data. These data are also available in the [Open Data Portal of the Canton of Thurgau](https://map.geo.tg.ch/apps/mf-geoadmin3/?lang=de&topic=ech&catalogNodes=10000,20000,30000,15100,34000&layers=richtplankt50k_hauptverkehrstrassen,richtplankt200k_motorfahrzeugverkehr,strassenverkehrszaehlung_messdaten&layers_opacity=0.9,1,1&E=2728994.19&N=1280640.14&zoom=6&layers_timestamp=,,20130101&layers_visibility=true).

Note: The city of Constance explicitly did not collect the data.

#### Data source:

[Open Data Constance](https://offenedaten-konstanz.de/dataset/grenz-berg-nge-kraftfahrzeuge-deutschland-schweiz) under CC-BY 4.0

</details>

<details>
  <summary>
    The data set contains the measurement results of the bicycle counts of all municipal permanent counting points in the Constance urban area. With this data, it can be determined exactly when and how many cyclists were on the road at these locations. The measurement results are recorded in 15-minute intervals. The counting stations serve as an important data basis for the city's cycling policy.
  </summary>

#### Further information
Currently, the city of Constance operates one permanent counting station in the city area. The bicycle counting station is located at the end of the bicycle bridge near Herosépark (more info and pictures [here](http://www.konstanz.de/leben+in+konstanz/radstadt-konstanz/handlungsprogramm+radverkehr/daten+zum+radverkehr)).

Data from the bicycle counting station of the city of Constance: The statistics are provided annually on this portal in CSV format. More current data can be requested if needed. Access to the live API data can be granted on a case-by-case basis. Those who wish to access the Constance Bicycle Counter data for a particular day can do so on an interactive map provided by the vendor [Eco Counter](http://eco-public.com/ParcPublic/?id=4586).

The Bicycle-Data-Initiative has an interactive tool which offers the following functions: (Attention: currently only works for data until 08.11.2020)

* __1.__ [Download](https://www.bicycle-data.de/bicycles-data) of raw data based on the intervals you choose.

* __2.__ [create](https://www.bicycle-data.de/city-analysis) automated and standardized analyses from the data (e.g., averages for day, month, or weather conditions) 

* __3.__ [comparison](https://www.bicycle-data.de/city-comparison) of Constance with other cities. 

(Source: City of Constance, Office for Urban Planning and Environment)
</details>

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

In order to fully utilize the automated Linking that GitHub provides the coarse-grained list of work packages is proveded in the first issue of this Project and will constantly be updated there.

## [Work Packages → #1][Work Packages]

[Work Packages]: https://github.com/Waldleufer/2023-amse-data-engineering/issues/1
