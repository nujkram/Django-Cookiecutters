import 'package:flutter/material.dart';
import 'screens/auth/index.dart';


class Routes {
  final routes = <String, WidgetBuilder>{
    '/Auth': (BuildContext context) =>  new Auth()
  };

  Routes() {
    runApp(new MaterialApp(
      title: '{{cookiecutter.app_verbose}}',
      routes: routes,
      home: new Auth(),
    ));
  }
}