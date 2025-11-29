# 🎓 Student Performance Predictor

A comprehensive machine learning-powered web application that helps educators and parents predict student performance and identify at-risk students using advanced predictive analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-green.svg)

##  Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Model Performance](#-model-performance)
- [Contributing](#-contributing)
- [License](#-license)

##  Features

### For Students
- **Interactive Dashboard**: Adjust personal factors to see predicted performance
- **Real-time Predictions**: Get instant feedback on potential final grades
- **Risk Assessment**: Understand your academic risk level
- **Personalized Recommendations**: Receive tailored action plans

### For Teachers
- **Class Overview**: Monitor entire class performance distribution
- **At-Risk Alerts**: Identify students needing intervention
- **Bulk Data Import**: Upload CSV files to analyze multiple students
- **Model Retraining**: Update predictions with new data
- **Parent Communication**: Email alerts for at-risk students

### For Parents
- **Child Monitoring**: Track your child's academic performance
- **Performance Trends**: Visualize progress over time
- **Risk Notifications**: Stay informed about academic concerns
- **Actionable Insights**: Get specific recommendations to help

### Technical Features
- **Multi-language Support**: English, Hindi, Tamil, Telugu, Kannada, Malayalam
- **Responsive Design**: Works on desktop and mobile devices
- **Database Integration**: Persistent storage with SQLite
- **CSV Import/Export**: Easy data management
- **Real ML Models**: XGBoost regression and classification

##  Demo

### Live Demo
[View Live Application](https://vignesh0ss-student-performance-predictor-app.streamlit.app) *(Deploy on Streamlit Cloud)*

### Screenshots
*Add screenshots of your application here*

## 🛠 Technology Stack

- **Frontend**: Streamlit, HTML/CSS, Plotly
- **Backend**: Python 3.8+
- **ML Framework**: XGBoost, Scikit-learn, SHAP
- **Database**: SQLite
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly Express, Matplotlib

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vignesh0ss/Student-Performance-Predictor.git
   cd student-performance-predictor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the application**
   ```bash
   # Train the ML models (first-time setup)
   python -c "from model_engine import ModelEngine; engine = ModelEngine(); engine.train()"

   # Run the application
   streamlit run app.py
   ```

5. **Access the application**
   - Open http://localhost:8501 in your browser

##  Usage

### Getting Started
1. Select your role: **Student**, **Teacher**, or **Parent**
2. Choose your preferred language from the sidebar
3. Follow the role-specific instructions

### For Students
1. Adjust the sliders for your current academic factors
2. View your predicted final grade and risk level
3. Follow the personalized action plan

### For Teachers
1. Upload CSV files with student data
2. Review class performance analytics
3. Identify and contact at-risk students
4. Retrain models with new data

### For Parents
1. Select your child from the database
2. Monitor performance trends
3. Review recommendations for support

### CSV Upload Format
Your CSV file should contain these columns:
```csv
G1,G2,studytime,failures,absences,health,freetime,goout
15,14,3,0,2,5,3,2
16,15,2,1,4,4,2,3
```

## Project Structure

```
student-performance-predictor/
├── app.py                      # Main Streamlit application
├── model_engine.py             # ML model training and prediction
├── database.py                 # SQLite database operations
├── recommendations.py          # Personalized recommendation engine
├── translations.py             # Multi-language support
├── audit_model.py              # Model performance auditing
├── verify_system.py            # System verification script
├── run_system_tests.py         # Automated testing
├── requirements.txt            # Python dependencies
├── style.css                   # Custom CSS styling
├── models.pkl                  # Trained ML models (generated)
├── school_data.db              # SQLite database (generated)
├── views/                      # UI components
│   ├── student_view.py
│   ├── teacher_view.py
│   └── parent_view.py
├── student-mat.csv            # Sample dataset
└── README.md
```

## Model Performance

- **Regression Model**: XGBoost Regressor
  - R² Score: 0.82 (82% accuracy)
  - Predicts final grades (G3) from G1, G2, and behavioral factors

- **Classification Model**: XGBoost Classifier
  - Accuracy: 87.3%
  - Risk levels: Low, Medium, High

- **Features Used**:
  - G1: First period grade
  - G2: Second period grade
  - Study time: Weekly study hours
  - Failures: Past academic failures
  - Absences: School absences
  - Health: Health status (1-5)
  - Free time: Free time after school
  - Going out: Social activities

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python run_system_tests.py

# Verify system
python verify_system.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- **Dataset**: UCI Machine Learning Repository - Student Performance Dataset
- **ML Framework**: XGBoost for high-performance gradient boosting
- **UI Framework**: Streamlit for rapid web app development
- **Icons**: Emoji and custom CSS styling

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation in this README
- Review the code comments for implementation details

---

**Made with ❤️ for better education outcomes**
