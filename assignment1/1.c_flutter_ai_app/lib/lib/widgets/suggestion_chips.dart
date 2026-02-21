import 'package:flutter/material.dart';

class SuggestionChips extends StatelessWidget {
  final Function(String) onSuggestionTap;

  const SuggestionChips({super.key, required this.onSuggestionTap});

  static const List<String> suggestions = [
    '🐍 Write a Python hello world',
    '🌍 Fun fact about space',
    '📝 Help me write an email',
    '🧮 Explain machine learning',
    '🎨 Creative writing prompt',
    '💡 Productivity tips',
  ];

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Padding(
          padding: EdgeInsets.symmetric(vertical: 8),
          child: Text(
            'Try asking...',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 13,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          alignment: WrapAlignment.center,
          children: suggestions
              .map(
                (s) => ActionChip(
                  label: Text(s, style: const TextStyle(fontSize: 13)),
                  onPressed: () => onSuggestionTap(s),
                  side: BorderSide(
                    color: Theme.of(context).colorScheme.primary.withOpacity(0.4),
                  ),
                ),
              )
              .toList(),
        ),
      ],
    );
  }
}
