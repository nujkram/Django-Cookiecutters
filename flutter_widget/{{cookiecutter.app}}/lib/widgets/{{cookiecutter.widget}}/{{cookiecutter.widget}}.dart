import 'package:flutter/material.dart';


class {{cookiecutter.widget_class}} extends StatelessWidget{
  final String {{cookiecutter.widget_camel}}Name;

  {{cookiecutter.widget_class}}({
    this.{{cookiecutter.widget_camel}}
  });

  @override
  Widget build(BuildContext context){
    return new {{cookiecutter.widget_base}}(
      onPressed: onPressed
    )
  }
}