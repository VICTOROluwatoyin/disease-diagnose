# Deployment Guide

## 🚀 Deploy to Render

### Prerequisites
- GitHub account
- Render account (free)
- Gemini API key

### Step 1: Create Local Environment File
```bash
# Create .env file in the rag directory
cp env-template.txt .env

# Edit .env file and add your actual API key:
GEMINI_API_KEY=your_actual_gemini_api_key_here
SECRET_KEY=your_secret_key_here
```

### Step 2: Push to GitHub
```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Medical Symptom Analyzer with live features"

# Add remote repository
git remote add origin https://github.com/yourusername/medical-symptom-analyzer.git

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your repository: `medical-symptom-analyzer`
5. Configure deployment:
   - **Name**: `medical-symptom-analyzer`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

### Step 4: Set Environment Variables
In Render dashboard, go to Environment tab and add:
- **GEMINI_API_KEY**: `your_actual_gemini_api_key_here`
- **FLASK_ENV**: `production`

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Your app will be live at: `https://your-app-name.onrender.com`

## 🔧 Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env-template.txt .env

# Edit .env with your API key
# Run the application
python app.py
```

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `SECRET_KEY`: Flask secret key (required)
- `FLASK_ENV`: development or production (optional)
- `HOST`: Host address (optional, default: 0.0.0.0)
- `PORT`: Port number (optional, default: 5000)

## 📋 Troubleshooting

### Common Issues
1. **API Key Error**: Make sure GEMINI_API_KEY is set correctly
2. **Build Failures**: Check requirements.txt for correct versions
3. **Permission Errors**: Ensure camera/screen sharing permissions in browser
4. **HTTPS Required**: Some browsers require HTTPS for screen sharing

### Logs
- Check Render logs in the dashboard
- Use browser console (F12) for frontend debugging
- Enable debug mode for local development

## 🛡️ Security Notes
- Never commit .env files to version control
- Use environment variables for all sensitive data
- Regularly rotate API keys
- Enable HTTPS in production

## 📞 Support
For deployment issues, check:
- Render documentation
- GitHub repository issues
- Browser compatibility for live features 