## Fraud Detection for E-Commerce and Banking Transactions 👋

This project focuses on detecting fraud in transaction datasets using machine learning models,
explainable AI tools (SHAP and LIME), and model deployment with Flask, Docker, and MLflow 
for tracking experiments and reproducibility.

## Project Structure

1. **Data Processing and Modeling:**

- Various ML models (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, MLP) were trained on fraud and credit card datasets.
- Model performance metrics such as accuracy, precision, recall, and F1-score were evaluated.
  
2. **Model Explainability:**

- SHAP and LIME were used to interpret model predictions, providing insights into feature importance and individual prediction factors.
  
3. **Model Deployment:**

- A Flask API serves both fraud and credit detection models with endpoints for summary statistics, fraud trends, and device/browser analysis.
- A Dockerfile enables containerized deployment of the API.
  
4. **Interactive Dashboard:**

- Built with Dash, this dashboard visualizes fraud trends, device/browser analysis, and summary statistics in real time.
  
5. **Experiment Tracking with MLflow:**

- MLflow tracks model parameters, metrics, and artifacts, enabling easy comparison across model versions.

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt

```
2. Run the Flask API:
```bash
python serve_model.py

```
3. Run the Dashboard:

```bash
 python dashboard_combined.py
```
4. Build and run the Docker container:
```bash
docker build -t fraud-detection-model .
docker run -p 5000:5000 fraud-detection-model

```
## Key Files   

- **serve_model.py:** Flask API for model serving
- **dashboard_combined.py:** Dashboard visualization with Dash
- **Dockerfile:** Docker configuration for deployment
- **requirements.txt:** List of dependencies

## Additional Information

- Use MLflow’s UI (``mlflow ui``) to visualize experiment metrics and models.
- Detailed experiment results and insights are available in the ``mlruns`` directory.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## Acknowledgements
- **10 Academy:** For providing the challenge.

## Contribution
Contributions are welcome! Please create a pull request or issue to suggest improvements or add new features.


## Author

👤 **Naima Tilahun**

* Github: [@NaimaT15](https://github.com/NaimaT15)
