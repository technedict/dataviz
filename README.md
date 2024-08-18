# Data Analysis and Visualization Platform

## Overview

This web application allows users to upload datasets in CSV or Excel format, perform data cleaning and exploratory data analysis (EDA), and generate visualizations such as histograms, scatter plots, and bar charts. The platform also supports downloadable reports and offers API endpoints for programmatic data analysis.

## Features

- **User Authentication & Authorization:** Secure login system with role-based access control.
- **Data Uploading:** Support for CSV and Excel files.
- **Data Cleaning:** Automated and manual data cleaning options.
- **Exploratory Data Analysis (EDA):** Tools for summary statistics, correlation matrices, and more.
- **Data Visualization:** Interactive and static plots using Matplotlib, Seaborn, and Plotly.
- **Downloadable Reports:** Generate and download PDF or HTML reports of your analysis.
- **API Endpoints:** Access the analysis tools via RESTful API.

## Tech Stack

- **Backend:** Python, Flask
- **Data Handling:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Containerization:** Docker
- **Version Control:** Git, GitHub

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/data-viz-platform.git

2. **Navigate to the Project Directory**
   ```bash
   cd dataviz

3. **Build the Docker Container:**
   ```bash
   docker-compose up --build

4. **Access the Application:**
   The application will be available at http://localhost:5000.
