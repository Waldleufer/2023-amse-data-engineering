# Project Plan

## Summary

<!-- Describe your data science project in max. 5 sentences. -->
This projects analyzes XY.

## Rationale

<!-- Outline the impact of the analysis, e.g. which pains it solves. -->
The analysis will correlate the measured amount of bike users in Konstanz with the weather at the given date and the pkw boarder crossings between Germany and Swiss at the same given date over the course of one year (tbt, possibly not 2021 bc of a technical defect in one of the counters), to find out if there are any meaningful correlations.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Border crossings motor vehicles Germany and Switzerland
* Metadata URL: https://mobilithek.info/offers/-6759756997530398389
* Data URL: [todo]
* Data Type: CSV

<details>
<summary>The Swiss cantonal authority of Thurgau and the Swiss Federal Roads Office (ASTRA) collect the average daily traffic volume (DTV) of motor vehicles crossing the border at the three customs posts "Tägerwilen-Paradieser Tor", "Emmishofer Zoll" and the "Gemeinschaftszollanlage Kreuzlingen/Tägerwilen (GZA for short)".
</summary>
  
#### Further information
Since 2013, this data has been collected and is now also made available as open data. These data are also available in the [Open Data Portal of the Canton of Thurgau](https://map.geo.tg.ch/apps/mf-geoadmin3/?lang=de&topic=ech&catalogNodes=10000,20000,30000,15100,34000&layers=richtplankt50k_hauptverkehrstrassen,richtplankt200k_motorfahrzeugverkehr,strassenverkehrszaehlung_messdaten&layers_opacity=0.9,1,1&E=2728994.19&N=1280640.14&zoom=6&layers_timestamp=,,20130101&layers_visibility=true).

Note: The city of Constance explicitly did not collect the data.

#### Data source:

[Open Data Constance](https://offenedaten-konstanz.de/dataset/grenz-berg-nge-kraftfahrzeuge-deutschland-schweiz) under CC-BY 4.0

</details>


### Datasource2: ExampleSource
* Metadata URL: https://mobilithek.info/offers/-7161835583190029268
* Data URL: [todo]
* Data Type: CSV

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

1. Example Issue [#1][i1]
2. ...

[i1]: https://github.com/jvalue/2023-amse-template/issues/1
