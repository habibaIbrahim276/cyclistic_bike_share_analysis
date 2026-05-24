Cyclistic Bike-Share Analysis 

Project Overview
This project analyzes Cyclistic bike-share trip data to understand the behavioral differences between casual riders and annual members. 

The analysis aims to support business decisions and identify opportunities to convert casual riders into annual members. 

Project Structure 
cyclistic_bike_project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── staging_layer.ipynb
│   └── analysis_layer.ipynb
│
├── visuals/
│
├── report/
│     └── analysis_report.pdf
├── app/
│   └── streamlit_app.py
│
├── requirements.txt
│
└── README.md

Tools & Technologies
- Python 
- Pandas
- NumPy
- Plotly
- Streamlit
- Jupyter Notebook

Data Processing 
The project includes: 
- Data cleaning 
- Data transformation 
- Feature engineering 
- Exploratory data analysis (EDA)
- Interactive dashboard development 

Installation 
install required libraries using: 
pip install -r requirements.txt

Running the streamlit dashboard 

py -m streamlit run streamlit_app.py

Dashboard
An interactive Streamlit dashboard was created to visualize: 
- User behavior
- Ride trends 
- Seasonal patterns 
- Bike preferences 
- Usage comparisons between casual riders and members 

Report 
A detailed analysis report containing: 
- Business task 
- Data processing steps 
- Analysis findings 
- Visualizations 
- Recommendations
is included in the report/ directory

Author
Habiba Ibrahim
