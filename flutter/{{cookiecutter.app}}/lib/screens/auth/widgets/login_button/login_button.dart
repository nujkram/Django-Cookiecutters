import 'package:flutter/material.dart';
import 'package:{{cookiecutter.app}}/widgets/app_button/index.dart';


class LoginButton extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return new AppButton(
      buttonName: "login",
      onPressed: null,
      buttonTextStyle: null
    );
  }
}