# 🌿 MsituGuard - Environmental Protection Platform

**Kenya's AI-Powered Environmental Monitoring & Protection System**

MsituGuard connects forest-adjacent communities with local environmental organizations to monitor, report, and address environmental threats across Kenya. Supporting Kenya's 15 Billion Trees Initiative with cutting-edge AI technology.

## ✨ Key Features

### 🤖 AI & Machine Learning
- **AI Tree Survival Prediction** - 93.2% accuracy ML model for optimizing tree planting success
- **Species Recommendations** - Data-driven suggestions for optimal tree species selection
- **Predictive Analytics** - Environmental risk assessment and conservation planning

### 🌍 Environmental Protection
- **Environmental Report Submission** with GPS coordinates and photo evidence
- **Tree Planting Registration** for Kenya's 15 Billion Trees Initiative
- **Fire Risk Assessment** with real-time weather data integration
- **Impact Tracking** - Personal dashboards showing conservation contributions

### 👥 Community Engagement
- **Community Forum** for environmental discussions and knowledge sharing
- **Rewards System** with tokens, badges, and incentives for environmental actions
- **User Role Management** - Differentiated experiences for community members vs organizations
- **Gamification** - Progressive rewards system encouraging sustained participation

### 🏢 Organization Tools
- **Organization Dashboard** for comprehensive report management
- **Field Assessment Tools** for environmental monitoring
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
- **AI Models**: RandomForest Classifier with 93.2% accuracy
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

## 📱 Demo Credentials

### Test Accounts
- **Community Member**: `demo_user` / `MsituGuard2024!`
- **Organization**: `demo_org` / `MsituGuard2024!` 
- **Admin**: `admin` / `MsituGuard2024!`

### AI Features Demo
- **Anonymous Users**: 1 free tree prediction
- **Registered Users**: Unlimited predictions + species recommendations
- **Organizations**: Full analytics dashboard + field assessment tools

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
- ✅ Full AI tree prediction system
- ✅ Environmental reporting with GPS
- ✅ Community forum and rewards
- ✅ Organization dashboard
- ✅ Mobile-responsive design
- ✅ Real-time notifications

## 📊 Project Structure

```
MsituGuard/
├── App/                          # Main Django application
│   ├── ml_utils.py              # AI model utilities
│   ├── views_ml.py              # ML API endpoints
│   ├── templates/App/           # HTML templates
│   │   ├── tree_prediction.html # AI prediction interface
│   │   ├── home.html           # Landing page
│   │   └── ...                 # Other templates
│   └── static/                 # CSS, JS, images
├── Tree_Prediction/             # AI/ML system
│   ├── models/                 # Trained ML models
│   ├── training/               # Model training scripts
│   └── integration/            # Django integration files
├── crisis_communication/        # Django project settings
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎯 MVP Status: Complete ✅

### Core Features Delivered
- [x] AI-powered tree survival prediction
- [x] Environmental reporting system
- [x] Community engagement platform
- [x] Organization management tools
- [x] Mobile-responsive design
- [x] Rewards and gamification
- [x] Real-time notifications
- [x] Professional UI/UX

### Technical Achievements
- [x] 93.2% accuracy ML model
- [x] Scalable Django architecture
- [x] Modern responsive design
- [x] Production deployment
- [x] Comprehensive testing
- [x] Clean code practices

## 🌍 Environmental Impact

### Alignment with Kenya's Goals
- **15 Billion Trees Initiative**: Direct support for national reforestation
- **Climate Action**: Data-driven conservation strategies
- **Community Empowerment**: Grassroots environmental protection
- **Technology for Good**: AI serving environmental sustainability

### Real-World Applications
- **NGOs**: Environmental monitoring and reporting
- **Government**: Policy support and data collection
- **Communities**: Citizen science and conservation
- **Researchers**: Environmental data and insights

## 🤝 Contributing

We welcome contributions to MsituGuard! Please see our contributing guidelines and feel free to:
- Report bugs and issues
- Suggest new features
- Improve documentation
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Kenya Forest Service** - Environmental data and guidance
- **NEMA** - Regulatory framework support
- **Local Communities** - Real-world testing and feedback
- **Environmental Organizations** - Domain expertise and validation

---

**Built for Kenya's Environmental Future with AI Innovation** 🌿🤖

*MsituGuard - Where Technology Meets Conservation*