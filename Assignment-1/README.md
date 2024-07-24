# RESTful API-Driven Data Engineering Platform

## Architecture Design
![RestFulAPiSercices](Picture1.png)

## Author

- Name: Sasidhar Naidu
- Roll No: G23AI1034

### Components

#### Data Ingestion

Components: API Gateway, Ingestion Services

API Gateway: Centralized entry point for incoming data.
Ingestion Services: Microservices responsible for different data sources (e.g., batch ingestion, streaming data, real-time data).
Architecture:

External applications and data sources send data to the API Gateway.
The API Gateway routes the data to the appropriate Ingestion Service based on the type and source of the data.
Ingestion Services preprocess the data (e.g., validation, transformation) and forward it to Data Storage.

#### Data Storage
Components: Data Lake, Data Warehouse, Database

Data Lake: Stores raw and unstructured data.
Data Warehouse: Stores structured and processed data.
Database: Operational data storage (e.g., NoSQL, SQL databases).
Architecture:

Ingestion Services push raw data to the Data Lake via RESTful APIs.
Data Processing components pull data from the Data Lake for transformation and processing.
Processed data is stored in the Data Warehouse for analysis and reporting.
Operational databases store data needed for real-time applications.

#### Data Processing
Components: ETL/ELT Pipelines, Processing Engines

ETL/ELT Pipelines: Extract, Transform, Load processes for data transformation.
Processing Engines: Tools like Apache Spark, Flink, or other processing frameworks.
Architecture:

Data Processing services extract data from the Data Lake via RESTful APIs.
Transformation and processing tasks are performed using processing engines.
Processed data is loaded back into the Data Lake or Data Warehouse.

#### Data Aggregation
Components: Aggregation Services, Data Mart

Aggregation Services: Microservices to aggregate and summarize data.
Data Mart: Stores aggregated data for specific business needs.
Architecture:

Aggregation Services fetch data from the Data Warehouse or Data Lake via RESTful APIs.
Data is aggregated and summarized according to business requirements.
Aggregated data is stored in Data Marts for quick access.

#### Data Visualization
Components: Visualization Tools, Dashboard Services

Visualization Tools: Tools like Tableau, Power BI, or custom web applications.
Dashboard Services: RESTful services providing data for dashboards and reports.
Architecture:

Visualization tools pull aggregated data from Data Marts via RESTful APIs.
Dashboard Services provide endpoints for customized data views and analytics.
Users access visualizations through web interfaces or embedded dashboards.

# High-Level Architecture Diagram

                +----------------------+
                |   External Sources   |
                +----------+-----------+
                           |
                           v
                +----------v-----------+
                |     API Gateway      |
                +----------+-----------+
                           |
                           v
                +----------v-----------+
                |  Ingestion Services  |
                +----------+-----------+
                           |
                           v
          +----------------v----------------+
          |         Data Storage             |
          | +------------+    +------------+ |
          | |  Data Lake |    | Data Whouse| |
          | +------------+    +------------+ |
          +----------------v----------------+
                           |
                           v
              +------------v-----------+
              |   Data Processing      |
              | (ETL/ELT Pipelines)    |
              +------------+-----------+
                           |
                           v
                +----------v-----------+
                |  Aggregation Services|
                +----------+-----------+
                           |
                           v
                +----------v-----------+
                |    Data Marts        |
                +----------+-----------+
                           |
                           v
                +----------v-----------+
                | Visualization Tools  |
                +----------------------+


#### RESTful API Integration
- API Gateway: Exposes endpoints for data ingestion.
- Ingestion Services: Exposes endpoints for data validation and preprocessing.
- Data Storage: Exposes endpoints for data retrieval and storage operations.
- Data Processing: Exposes endpoints for initiating ETL/ELT jobs.
- Aggregation Services: Exposes endpoints for data aggregation and summarization tasks.
- Visualization Tools: Exposes endpoints for data retrieval for visualization.