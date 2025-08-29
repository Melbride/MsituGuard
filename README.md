# 🌿 MsituGuard - Environmental Protection Platform

**Kenya's AI-Powered Environmental Monitoring & Protection System**

MsituGuard connects forest-adjacent communities with local environmental organizations to monitor, report, and address environmental threats across Kenya. Supporting Kenya's 15 Billion Trees Initiative with cutting-edge AI technology.

## ✨ Key Features

### 🤖 AI & Machine Learning
- **AI Tree Survival Prediction** - 93.2% accuracy ML model for optimizing tree planting success
- **MISTRAL AI Integration** - Advanced fire risk analysis and field assessment recommendations
- **Species Recommendations** - Data-driven suggestions for optimal tree species selection
- **Predictive Analytics** - Environmental risk assessment and conservation planning
- **GPS Auto-Detection** - Automatic climate and soil data retrieval from coordinates

### 🌍 Environmental Protection
- **Environmental Report Submission** with GPS coordinates and photo evidence
- **Tree Planting Registration** for Kenya's 15 Billion Trees Initiative
- **AI-Powered Fire Risk Assessment** with MISTRAL AI analysis and Kenya-specific parameters
- **Impact Tracking** - Personal dashboards showing conservation contributions
- **Real-time Weather Integration** - Simulated weather data for cost-effective deployment

### 👥 Community Engagement
- **Community Forum** for environmental discussions and knowledge sharing
- **Rewards System** with tokens, badges, and incentives for environmental actions
- **User Role Management** - Differentiated experiences for community members vs organizations
- **Gamification** - Progressive rewards system encouraging sustained participation

### 🏢 Organization Tools
- **Organization Dashboard** for comprehensive report management
- **AI-Enhanced Field Assessment Tools** - MISTRAL AI analysis for environmental monitoring
- **Export Functionality** - Field assessment reports with AI recommendations
- **Analytics & Reporting** - Data insights for conservation decision making
- **Verification System** - Quality control for environmental reports

### 📱 User Experience
- **Mobile-First Design** - Optimized for field use on smartphones and tablets
- **Responsive Interface** - Seamless experience across all device sizes
- **Professional UI/UX** - Modern design following industry best practices
- **Accessibility** - Inclusive design for diverse user needs

## 🚀 Technology Stack

### Backend & AI
- **Framework**: Django (Python 3.11+)
- **Machine Learning**: scikit-learn, pandas, numpy
- **AI Models**: RandomForest Classifier with 93.2% accuracy + MISTRAL AI
- **AI Integration**: mistralai==1.0.1 for advanced environmental analysis
- **Data Processing**: Advanced feature engineering and model serialization

### Frontend & Design
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Bootstrap 5
- **UI Framework**: Modern responsive design with CSS Grid/Flexbox
- **Icons**: Font Awesome 6.4+
- **Fonts**: Inter, Poppins (Google Fonts)

### Infrastructure & Services
- **Database**: Supabase PostgreSQL (Production), SQLite (Development)
- **Media Storage**: Cloudinary CDN for images and file uploads
- **Deployment**: Render.com with automatic deployments
- **Version Control**: Git with comprehensive commit history

## 🧠 AI Model Performance

### Tree Survival Prediction Model
- **Algorithm**: RandomForest Classifier
- **Accuracy**: 93.2% on test dataset
- **Features**: 13 environmental and planting factors
- **Training Data**: 10,000+ Kenyan tree planting records
- **Validation**: Cross-validated with stratified sampling

### Key Prediction Factors
1. **Tree Species** - Native vs non-native adaptation
2. **Soil Conditions** - pH, type, and drainage
3. **Climate Data** - Rainfall, temperature, altitude
4. **Planting Method** - Technique and timing optimization
5. **Care Level** - Maintenance and monitoring intensity

## 🎯 Platform Access

### User Experience
- **Anonymous Users**: Tree prediction with basic features
- **Registered Users**: Unlimited predictions + species recommendations + AI fire risk analysis
- **Organizations**: Full dashboard + AI field assessments + export functionality
- **Admin**: Complete platform management and analytics

### AI Features Available
- **Tree Survival Prediction**: 93.2% accuracy ML model
- **Fire Risk Analysis**: MISTRAL AI-powered assessment
- **Field Assessment AI**: Environmental monitoring with AI insights
- **Species Recommendations**: Location-based tree selection

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/Melbride/MsituGuard.git
cd MsituGuard

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Access Points
- **Local Development**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin`
- **API Endpoints**: `http://localhost:8000/api/`

### ML Model Setup
```bash
# Navigate to ML training directory
cd Tree_Prediction/training

# Train the model (optional - pre-trained models included)
python train_tree_model.py

# Models are automatically loaded from Tree_Prediction/models/
```

## 🌐 Live Demo

**Production URL**: https://msituguard.onrender.com

### Live Features
- ✅ Full AI tree prediction system with 93.2% accuracy
- ✅ MISTRAL AI fire risk analysis and field assessments
- ✅ Environmental reporting with GPS auto-detection
- ✅ Community forum and rewards system
- ✅ Enhanced organization dashboard with AI tools
- ✅ Mobile-responsive design with improved UX
- ✅ Real-time notifications and impact tracking

## 📊 Project Structure

```
MsituGuard/
├── App/                          # Main Django application
│   ├── fire_risk_analyzer.py   # MISTRAL AI fire risk analysis
│   ├── mistral_ai.py           # AI integration utilities
│   ├── climate_data.py         # Climate data processing
│   ├── ml_utils.py              # AI model utilities
│   ├── views_ml.py              # ML API endpoints
│   ├── templates/App/           # HTML templates
│   │   ├── tree_prediction.html # AI prediction interface
│   │   ├── field_assessment.html # AI field assessment
│   │   ├── fire_risk.html      # Fire risk analysis
│   │   ├── home.html           # Landing page
│   │   └── ...                 # Other templates
│   └── static/                 # CSS, JS, images
├── Tree_Prediction/             # AI/ML system
│   ├── models/                 # Trained ML models
│   ├── training/               # Model training scripts
│   └── integration/            # Django integration files
├── crisis_communication/        # Django project settings
├── requirements.txt            # Python dependencies (includes mistralai)
└── README.md                   # This file
```

## 🆕 Recent Updates

### Version 2.0 - AI Enhancement Release
- **MISTRAL AI Integration**: Advanced fire risk analysis and field assessments
- **Enhanced UI/UX**: Improved branding emphasizing AI-powered conservation
- **Registration Improvements**: Streamlined account creation with better UX
- **Access Control**: Species recommendations restricted to registered users
- **Mobile Optimization**: Better responsive design and spacing
- **Export Functionality**: AI field assessment reports with recommendations
- **Navigation Enhancement**: Reordered menu prioritizing Tree Prediction

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built for Kenya's Environmental Future with AI Innovation** 🌿🤖

*MsituGuard - Where Technology Meets Conservation*