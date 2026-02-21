# ✨ AI-Powered Flutter App with Google Gemini
### Built with Claude (Agentic AI) — Cross-Platform Mobile App

---

## 📱 What This App Does
A beautiful cross-platform AI chat app built with **Flutter** + **Google Gemini API** that runs on:
- ✅ Android
- ✅ iOS
- ✅ Web
- ✅ macOS / Windows / Linux

## 🏗️ Project Structure
```
lib/
├── main.dart                  # App entry point
├── models/
│   └── chat_message.dart      # Message data model
├── screens/
│   └── chat_screen.dart       # Main chat UI (StatefulWidget)
├── services/
│   └── gemini_service.dart    # Google Gemini AI integration
├── widgets/
│   ├── message_bubble.dart    # Chat bubble with Markdown support
│   └── suggestion_chips.dart  # Quick prompt suggestions
└── theme/
    └── app_theme.dart         # Light/Dark theme
```

## 🚀 Setup & Run

### 1. Prerequisites
```bash
flutter --version  # Needs Flutter 3.x+
```

### 2. Get Gemini API Key
- Go to https://aistudio.google.com
- Click **Get API Key** → Create new key
- Copy the key

### 3. Add Your API Key
Open `lib/services/gemini_service.dart` and replace:
```dart
static const String _apiKey = 'YOUR_GEMINI_API_KEY_HERE';
```

### 4. Install Dependencies
```bash
cd ai_chat_app
flutter pub get
```

### 5. Run the App
```bash
# Android
flutter run -d android

# iOS
flutter run -d ios

# Web
flutter run -d chrome

# All devices
flutter devices
flutter run -d <device-id>
```

## 🌟 Features
| Feature | Description |
|---|---|
| 💬 Streaming Responses | Real-time token streaming from Gemini |
| 🌙 Dark/Light Mode | Adapts to system theme |
| 📝 Markdown Support | Code blocks, bold, lists rendered |
| 💡 Suggestion Chips | Quick-start prompts |
| 🔄 Session Reset | Start fresh conversations |
| ⚡ Early Stopping | Prevents repeated loading |
| 📱 Cross-Platform | Android, iOS, Web, Desktop |

## 📦 Dependencies
```yaml
google_generative_ai: ^0.4.3   # Official Google Gemini SDK
flutter_markdown: ^0.6.18       # Render AI markdown responses
shared_preferences: ^2.2.2      # Local storage
intl: ^0.18.1                   # Internationalization
```

