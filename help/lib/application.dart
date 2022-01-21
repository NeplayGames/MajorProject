import 'dart:convert';
import 'dart:typed_data';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'package:text_to_speech/text_to_speech.dart';

class Command {
  static final all = [email, browser1, browser2, readText, see, callNumber];

  static const email = 'write email';
  static const browser1 = 'open';
  static const browser2 = 'go to';
  static const readText = 'read';
  static const see = 'see';
  static const callNumber = "call to";
}

class Application {
  static void scanText(String rawText) {
    final text = rawText.toLowerCase();
    print(text);
    if (text.contains(Command.email)) {
      final body = _getTextAfterCommand(text: text, command: Command.email);

      openEmail(body: body);
    }
    if (text.contains(Command.browser1)) {
      final url = _getTextAfterCommand(text: text, command: Command.browser1);

      openLink(url: url);
      return;
    }
    if (text.contains(Command.browser2)) {
      final url = _getTextAfterCommand(text: text, command: Command.browser2);

      openLink(url: url);
      return;
    }
    if (text.contains(Command.see)) {
      See("see");
      return;
    }
    if (text.contains(Command.readText)) {
      See("read");
      return;
    }
    if (text.contains(Command.callNumber)) {
      _launchCall((9840092372).toString());
      return;
    }
  }

  static void initialCommand(String rawText) {}
  static String _getTextAfterCommand({
    @required String text,
    @required String command,
  }) {
    final indexCommand = text.indexOf(command);
    final indexAfter = indexCommand + command.length;

    if (indexCommand == -1) {
      return null;
    } else {
      return text.substring(indexAfter).trim();
    }
  }

  ///Opean the link with the given url
  static Future openLink({
    @required String url,
  }) async {
    if (url.trim().isEmpty) {
      // final response = await http.head(Uri.parse('https://$url.com'));
      // print(url);
      // if (response.statusCode == 200) {
      //   if (await canLaunch("$url.com")) {
      //     await launch("$url.com");
      //   }
      // } else {}
      await _launchUrl('https://google.com');
    } else {
      await _launchUrl('https://$url');
    }
  }

  static Future openEmail({
    @required String body,
  }) async {
    final url = 'mailto: ?body=${Uri.encodeFull(body)}';
    await _launchUrl(url);
  }

  static Future _launchCall(String number) async {
    print(await canLaunch(number));
    //  if (await canLaunch(number)) {
    await launch("tel://" + number);
    //  }
  }

  ///Launch the url if it is possible to launch the url
  static Future _launchUrl(String url) async {
    if (await canLaunch(url)) {
      await launch(url);
    }
  }

  static Future See(String command) async {
    final cameras = await availableCameras();
    final camera = cameras.first;

    String result = await _showCamera(camera);
    http.Response output = await http
        .post(Uri.parse("http://192.168.1.67:5000/${command}"), body: result);
    if (output.statusCode == 200) {
      TextToSpeech tts = TextToSpeech();
      await tts.setLanguage("ne-NP");
      String res = await output.body.toString();
      tts.speak(res);
    }
  }

  ///This function will call the camera component and click the photo which is converted to base64 and then sent return the string
  ///after converting it into json after creating map of info
  ///It returns string

  static Future<String> _showCamera(var camera) async {
    try {
      Uint8List _imgBytes;
      CameraController _cameraController;
      Future<void> _initializeCameraControllerFuture;
      _cameraController = CameraController(camera, ResolutionPreset.high);
      _initializeCameraControllerFuture = _cameraController.initialize();
      await _initializeCameraControllerFuture;
      final picture = await _cameraController.takePicture();
      _imgBytes = await picture.readAsBytes();
      String base64encode = base64.encode(_imgBytes);
      Map<String, dynamic> d = {'name': picture.name, 'img': base64encode};
      String result = json.encode(d);
      return result;
    } catch (e) {
      print(e);
      return "Error";
    }
  }
}
