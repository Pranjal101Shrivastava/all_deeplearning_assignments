import 'package:google_generative_ai/google_generative_ai.dart';

class GeminiService {
  // 🔑 Replace with your actual Gemini API key from https://aistudio.google.com
  static const String _apiKey = 'YOUR-API-KEY-HERE';

  late final GenerativeModel _model;
  late ChatSession _chatSession;

  GeminiService() {
    _model = GenerativeModel(
      model: 'gemini-1.5-flash',
      apiKey: _apiKey,
      generationConfig: GenerationConfig(
        temperature: 0.8,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 2048,
      ),
      systemInstruction: Content.system(
        'You are a helpful, friendly, and knowledgeable AI assistant. '
        'Answer questions clearly and concisely. '
        'You can help with coding, writing, analysis, and general questions.',
      ),
    );
    _startNewSession();
  }

  void _startNewSession() {
    _chatSession = _model.startChat();
  }

  /// Send a message and get a streaming response
  Stream<String> sendMessageStream(String userMessage) async* {
    try {
      final response = _chatSession.sendMessageStream(
        Content.text(userMessage),
      );
      await for (final chunk in response) {
        final text = chunk.text;
        if (text != null && text.isNotEmpty) {
          yield text;
        }
      }
    } catch (e) {
      yield 'Error: ${e.toString()}. Please check your API key and try again.';
    }
  }

  /// Send a message and get a single response
  Future<String> sendMessage(String userMessage) async {
    try {
      final response = await _chatSession.sendMessage(
        Content.text(userMessage),
      );
      return response.text ?? 'No response received.';
    } catch (e) {
      return 'Error: ${e.toString()}. Please check your API key.';
    }
  }

  void resetSession() => _startNewSession();
}
