# Medical Symptom Analyzer

A professional AI-powered medical symptom analyzer that uses Google's Gemini API to provide preliminary analysis of visual symptoms from uploaded images.

## ⚠️ Important Medical Disclaimer

**This application is NOT a substitute for professional medical advice, diagnosis, or treatment.** Always consult healthcare professionals for proper medical care.

## 🚀 Features

- **AI-Powered Analysis**: Uses Google Gemini 1.5 Flash for advanced image analysis
- **Multiple Capture Methods**: Upload files, live camera, or screen sharing
- **Live Camera Capture**: Real-time symptom analysis using device camera
- **Screen Sharing**: Analyze symptoms from other applications or medical images
- **Visual Symptom Recognition**: Analyzes photos of symptoms, rashes, injuries, etc.
- **Severity Assessment**: Provides preliminary urgency ratings
- **Medical Recommendations**: Suggests next steps and when to seek care
- **Professional UI**: Clean, medical-grade user interface with tabbed navigation
- **Privacy Focused**: Images are processed temporarily and deleted after analysis
- **Mobile Responsive**: Works on all devices with touch-friendly controls

## 📋 What It Analyzes

- Skin conditions (rashes, lesions, discoloration)
- Visible injuries and wounds
- Swelling and inflammation
- Eye conditions
- Oral health issues
- And many other visual symptoms

## 🛠️ Installation & Deployment

### Local Development
1. **Setup environment**
   ```bash
   cd rag
   pip install -r requirements.txt
   ```

2. **Create environment file**
   ```bash
   cp env-template.txt .env
   # Edit .env and add your Gemini API key
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

### 🚀 Deploy to Render (Free Hosting)
1. **Push to GitHub** (API key will be hidden)
2. **Connect to Render**
3. **Set environment variables**
4. **Deploy!**

👉 **Full deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🎯 How to Use

### Option 1: Upload Image
1. **Upload Image**: Drag and drop or click to select an image of your symptoms
2. **Wait for Analysis**: The AI will analyze the image (takes 10-30 seconds)
3. **Review Results**: Get detailed analysis with possible conditions and recommendations

### Option 2: Live Camera 📱
1. **Start Camera**: Click "Start Camera" to activate your device's camera
2. **Position Symptom**: Position the symptom in view of the camera
3. **Capture & Analyze**: Click "Capture & Analyze" for instant analysis
4. **Review Results**: Get immediate AI analysis of the captured image

### Option 3: Screen Sharing 🖥️
1. **Start Screen Share**: Click "Start Screen Share" to share your screen
2. **Navigate to Content**: Open the application or image you want to analyze
3. **Capture & Analyze**: Click "Capture & Analyze" to analyze what's on screen
4. **Review Results**: Get analysis of the captured screen content

### Always Remember
- **Consult Professional**: Always verify results with healthcare providers
- **Emergency Situations**: Call emergency services for severe symptoms

## 📸 Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WEBP (.webp)
- Maximum file size: 16MB

## 🔧 Technical Details

- **Framework**: Flask (Python web framework)
- **AI Model**: Google Gemini 1.5 Flash
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Live Features**: WebRTC, MediaDevices API, Screen Capture API
- **Image Processing**: PIL (Python Imaging Library), HTML5 Canvas
- **Security**: File validation, size limits, secure filenames, stream cleanup
- **Browser Support**: Modern browsers with camera/screen sharing support

## 📁 Project Structure

```
rag/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Main page
│   ├── about.html       # About page
│   ├── 404.html         # 404 error page
│   └── 500.html         # 500 error page
└── uploads/             # Temporary image storage (auto-created)
```

## 🛡️ Privacy & Security

- Images are processed temporarily and immediately deleted
- No personal information is collected or stored
- No medical records are created or maintained
- All analysis is done locally through the API
- Secure file handling with validation

## ⚠️ Limitations

- AI analysis may not be 100% accurate
- Some conditions cannot be diagnosed from images alone
- Results should be interpreted by healthcare professionals
- Not suitable for emergency situations
- May not detect all medical conditions

## 🆘 Emergency Situations

**Call emergency services immediately for:**
- Severe chest pain or difficulty breathing
- Signs of stroke
- Severe bleeding or trauma
- Loss of consciousness
- Severe allergic reactions
- Any life-threatening symptoms

## 🔗 API Information

This application uses Google's Gemini API for image analysis. The API key is configured in the application code.

## 📞 Support

For technical issues or questions about the application (not medical advice), please refer to the documentation or contact the developer.

## 📄 Legal Notice

By using this application, you acknowledge that:
- This tool is for informational purposes only
- Results are not medical advice or diagnosis
- You will consult healthcare professionals for medical concerns
- You understand the limitations of AI-based analysis
- The developers are not responsible for medical decisions based on this tool

---

**Remember: Always consult healthcare professionals for proper medical diagnosis and treatment.** 