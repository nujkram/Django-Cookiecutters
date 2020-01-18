import 'package:flutter/material.dart';
import 'widgets/login_button/index.dart';

class Auth extends StatelessWidget {

  @override
  Widget build(BuildContext context){
    return new Scaffold(
      appBar: new AppBar(
        title: new Text("Authentication")
      ),
      body: new Container(
        child: new Center(
          child: new Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              new LoginButton(),
              new Padding(
                padding: new EdgeInsets.all(8.0)
              )

            ]
          )
        )
      )
    );
  }
}