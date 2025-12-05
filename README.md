# Horror Movie Analysis

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Predicting Horror Movie Revenue with Machine Learning

This project analyzes what factors best predict box-office revenue for horror movies. The goal is to understand which movie characteristics matter most for financial success and to compare different machine learning models on their ability to predict log-transformed revenue.

The dataset used is a merged horror movie dataset created by combining IMDb, TMDb, The Numbers, and additional box office sources. The cleaned dataset includes features such as budget, runtime, IMDb ratings, vote counts, language, region, and release month.


## Sprint 2 progress
### Updates
- Added the raw horror movie dataset (`data/raw/horror_data_master_v10_final_only.csv`)
- Added data gathering, cleaning, and exploratory data analysis notebooks (`notebooks/Sprint_2_EDA.ipynb`, `notebooks/building_core_imdb_horrort2_.ipynb`, `notebooks/horror_data_gatheringpt1.py` )
- Completed exploratory analysis and variable review in Sprint 2

### Summary
In Sprint 2, I successfully gathered and cleaned the horror movie dataset, performed exploratory data analysis, and refined my problem statement to focus on predicting box office revenue for horror films. The next sprint will focus on building predictive models and testing which features best explain box office performance.

## Sprint 3 Summary

Gradient boosting is the strongest and most stable model

IMDb vote related features are the most important predictors

Movies with missing or zero budgets create major prediction errors

Low revenue films remain difficult for all models to predict

Next steps include collecting more complete data and tuning hyperparameters

### Models
I have trained three models:

1. Linear Regression (Baseline)

    -   Simple, interpretable model
	-	Used as a baseline to compare improvements
	-	Stored as: linear_regression_model.pkl

2. Random Forest Regressor
	-	Ensemble method using multiple decision trees
	-	Higher performance but more prone to overfitting
	-	Stored as: random_forest_model.pkl

3. Gradient Boosting Regressor (Final Model)
	-	Best overall generalization performance
	-	Handles nonlinear relationships well
	-	Stored as: gradient_boosting_model.pkl

All performance metrics are in model_results.json




## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         horror_movie_analysis and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── horror_movie_analysis   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes horror_movie_analysis a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

