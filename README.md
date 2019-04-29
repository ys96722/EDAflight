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
#### 3.1  Feature Analysis 

##### 3.1.1 First glance of the features
*(LY) stream graph for each variable + num flights*
##### 3.1.2 Delay 
*(JC) (XY)*
- Monthly / Day of Week trend of departure/arrival delay

- Zoom in: Percentile of departure dealy in June

- Reason of delay in 2006

  ![Delay Time for Each Reason in 2006](plots/Delay Time for Each Reason in 2006.png)

This graph shows the total time of delay by reason in each month of 2006. The y-axis indicates the sum of delay time in the unit of minute. For the sum, June, July and December had higher values, while January and February had relatively lower ones. For these five delay reasons, the distributions of them in each month were similar. Late aircraft, NAS, and carrier were three common reasons leading to most delay time, and the weather did not cause too much delay, which is unexpected. Delay caused by security was rare that we can hardly see the blocks with darker color from the graph. 

We expected that there would be more delay time in winter, but actually June and July had the largest delay time caused by weather. Thus we might guess that some events or some extreme weather happened at that time. As we went back to the news, we found that there was a severe heat wave in 2006 summer that affected most of the United States and Canada, killing hundreds of people, and temperatures in many locations made the highest temperature records.

##### 3.1.3  Cancellation 

*(Python) (Yoon)*
#### 3.2  Multivariate Analaysis & General Trends
##### 3.2.1  Treemap Analysis (R) (JC) (YX)
- byState

- byCarrier

- byModel

  The next two graphs show the relationships between cancellation rate and the plane model as well as the delay rate and the model type. The size of a square indicates the number of flights with that particular model. And a darker color indicates a larger ratio value.

  For the two years, Boeing was the leading position of the number of flights. In 1998, McDonnell Douglas was in the second position while the ranking was lowered to the fifth in 2006. Embraer and Bombardier INC., which were not in the top 4 in 1998, became the second and third largest manufactures in 2006. The models in 1998 and 2006 differed a lot. Most old models were replaced by newer ones.

  ![Cancellation Rate for Each Model](plots/Cancellation Rate for Each Model.png)

In 2006, most models in the top 8 manufactures had relatively low cancellation rates. On the contrary, large cancellation rates happened to flights with small manufactures. But this trend was not the same in 1998, the top several manufactures all had models with high cancellation rates.

![Delay Rate for Each Model](plots/Delay Rate for Each Model.png)

This graph is not that interesting, because the colors are similar between models, manufactures and years. The delay rate was not affected significantly by models and manufactures.

##### 3.2.2 Correlation Heatmap Analysis (R) (Yoon)

##### 3.2.3 Geography Map Thingy Analysis (Yoon)
##### 3.2.4 Most busiest airports (YL)

### 4 Case study
#### 4.1 delay ~  m_year (Yoon)
#### 4.2 (actual - expected) ~ delay (Yoon)

### 5 Conclusion

## License

This project is licensed under the MIT License

## Acknowledgments

- Statistics 480: blah blah blah
- **Darren Glosemeyer**