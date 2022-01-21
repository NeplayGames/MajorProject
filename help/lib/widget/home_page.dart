import 'package:avatar_glow/avatar_glow.dart';
import 'package:flutter/material.dart';
import '../api/speech_api.dart';
import '../main.dart';
import '../widget/substring_highlighted.dart';
import '../application.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String text =
      'Click on any part of screen and give command as /open youtube.com';
  bool isListening = false;

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTap: toggleRecording,
        child: Scaffold(
          appBar: AppBar(
            title: Text(Helper.title),
            centerTitle: true,
          ),
          body: SingleChildScrollView(
            reverse: true,
            padding: const EdgeInsets.all(30).copyWith(bottom: 150),
            child: SubstringHighlight(
              text: text,
              terms: Command.all,
              textStyle: TextStyle(
                fontSize: 32.0,
                color: Colors.black,
                fontWeight: FontWeight.w400,
              ),
              textStyleHighlight: TextStyle(
                fontSize: 32.0,
                color: Colors.red,
                fontWeight: FontWeight.w400,
              ),
            ),
          ),
          floatingActionButtonLocation:
              FloatingActionButtonLocation.centerFloat,
          floatingActionButton: AvatarGlow(
            animate: isListening,
            endRadius: 75,
            glowColor: Theme.of(context).primaryColor,
            child: Icon(isListening ? Icons.mic : Icons.mic_none, size: 36),
          ),
        ),
      );

  Future toggleRecording() => SpeechApi.toggleRecording(
        onListening: (isListening) {
          setState(() => {
            print(StackTrace.current),
                this.isListening = isListening,
                print(isListening),
              });
          if (!isListening) {
            Future.delayed(Duration(seconds: 1), () {
              Application.scanText(text);
            });
          }
        },
        onResult: (text) => setState(() => {
              this.text = text,
            }),
      );
}
