# Exploratory Data Analysis on Flight Dataset

This is an EDA on the infamous Flights Dataset.

## Getting Started

- Decompress the zip file work under this directory
- Run `downloadData.sh` to fetch original datasets and set up the working environment
- Run `....hive` to generate the datasets used for plots (saved to the folder `generated_datasets`)
- Run `main.R` to generate plots (generated plots will be stored in the folder `plots`)
- Run `....py` to generate plots (*save plots?*)

## Built With

- [RStudio](https://www.rstudio.com/) - The framework we used to create the analysis
- Jupyter Notebook - The environment we used to create the Python portion
- Hive - The framework we used to wrangling large datasets

## Authors

- **Yoon Chang** - [Portfolio](https://yooniverse.me/)
- **Yi Xu**
- **Yingyi Lai**
- **Junyao Chen**

## Roadmap

### 1 Introduction (LY)

### 2 Wrangling (LY)
- byCarr (Hive)
- byModel (Hive)
- ...
### 3 Visualization & Analysis
#### 3.1  Feature Analysis (LY) stream graph for each variable + num flights
- Departure/Arrival  Delay (JC) (XY)
- Cancellation (Python) (Yoon)
#### 3.2  Multivariate Analaysis & General Trends
- Treemap Analysis (R) (JC) (YX)
- Correlation Heatmap Analysis (R) (Yoon)
- Geography Map Thingy Analysis (Yoon)
- Most busiest airports (YL)

### 4 Case study
#### 4.1 delay ~  m_year (Yoon)
#### 4.2 (actual - expected) ~ delay (Yoon)

### 5 Conclusion

## License

This project is licensed under the MIT License

## Acknowledgments

- Statistics 480: blah blah blah
- **Darren Glosemeyer**