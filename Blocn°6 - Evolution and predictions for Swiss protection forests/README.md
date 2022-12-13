Welcome to the Block n°6 of the Jedha's certification !...
 - Analysis, Evolution and predictions of Swiss Protective Forests - 

Name : DINE Aloïs Jesshuan
e-mail : jesshuan.dine@gmail.com

Lien vidéo de la présentation :
https://share.vidya

-------------------
ABOUT THE GLOBAL COLLABORATIVE PROJECT

Presentation :

An analysis of the state of protective forests in Switzerland : main factors of growth and health and first modelling approaches to predict the future of these forests...

-> Presentation of the project available on the Jedha Bootcamp youtube channel during the DemoDay (8min):
https://www.youtube.com/watch?v=Hbn9JkuRaWk&t=9036s
(our presentation start at 1h 22m 40s)

-> The presentation with slides is also added in this repository : Protective Forest CH.pptx

Team Main contribution :

- Dashboarding: Marjory Lamothe
- Satellite data gathering and aggregation: myself
- Climatic data analysis: Arnaud Barraquand ([Git](https://github.com/Ukratic/Protection-Forests) "Link to the git repo")
- Scientific expertise: Estelle Noyer ([Git](https://github.com/NoyE-R/JF_B6_ProtectiveForest/blob/main/README.md) "Link to the git repo")
- Modeling: all members.

Dataset :

The used dataset includes three kind of data:

- National Forest Inventory (NFI) data : field measurements of the typographical and structural variables from 1983 to 2017
- Historical climatic data (WSL): monthly temperature and precipitation records
- Satellite data (Google Earth Engine): satellite images of each forest plots from LANDSAT 5 and 7.
NB: due to the size of the data (large volume), requests to satellites were done by all members of the team using a automation script and a special env with Docker image.

Outputs Results take form through :

    Dashboard with EDA and modeling analysis of the forest, and a presentation of our model's performances :
    Availaible on [this link](https://ukratic-protection-forests-dashboard-home-fsgk56.streamlit.app/)

Analytical approach :

Three targets were selected in order to get different point of view defining the health of forests:
Basal Area: biomass production at time t (feature : SURF_TER_HA)
Wood volume increment: growth of the forest plot between two forest surveys (features : ACCR or ACCR_UNIT)
Regeneration cover rate: development ability of the forest in the future, i.e. stability of the forest. (feature : TAUX_COUV_RAJ)

Descriptive models :

All the "descriptive" models in Machine Learning and Deep Learning were been built to respond to two objectives :
- What are the main factors of the health of the protective forests ? (To describe the forest at time t by all the features at time t, and to make features extraction.)
- Can we correlate satellite and weather data with our health indicators ? (to add or substract theses features and to look performances)
Preprocessing were similar, but each target was the subject of a different technique.
Models tested : Simple Linear Regressor, Ridge Regressor, Ridge Classifier, Lasso, Random Forest, Decision Tree, Hist Gradient Boost, Categorical Naive Bayes...

Predictive models : 

All the "predictive" models in Machine Learning and Deep Learning were been built to repond to one objective :
- In a time-based perspective, and if we didn't have all the informations from the field (NFI Data), can we predict the future of a protective forest ?...
For this objective, various approaches are possible :
- we just keep NFI informations at t-1 and SAT / Meteo data at t and we try to predict our target at t (similar to a descriptive model)
- we have NFI informations of t-3, t-2, t-1... and we try to predict t (it's a "time series" problematic)
- we have NFI informations of t-3, t-2, t-1... and we have SAT / Meteo data at t, and we try to predict t (it's a "time series" problematic with time dependent regressors)
Models tested : Ridge Regressor, Ridge Classifier, XGBoost, Multi-Layers Dense, Mutli-Layers RNN with additional pipeline of Multi-Layers Dense...


-------------------
ABOUT MY PERSONNAL CONTRIBUTION AND THIS REPOSITORY






-------------------
OTHER CREDITS




