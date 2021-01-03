#!/bin/env python3
from string import Template
from glob import glob
from pathlib import Path
import subprocess
import os

entity_images = glob("*.png")

print(entity_images)

all_puml_content = """@startuml

!define ENTITY_COLOR #232F3E
!define ENTITY_BG_COLOR #FFFFFF
!define ENTITY_BORDER_COLOR #FF9900
!define ENTITY_SYMBOL_COLOR ENTITY_COLOR

!define TECHN_FONT_SIZE 12

skinparam defaultTextAlignment center

skinparam wrapWidth 200
skinparam maxMessageSize 150
skinparam shadowing false

skinparam Arrow {
    Color #666666
    FontColor #666666
    FontSize 12
}

!definelong EntityColoring(stereo)
skinparam rectangle<<stereo>> {
    StereotypeFontSize 0
    BackgroundColor ENTITY_BG_COLOR
    BorderColor ENTITY_BORDER_COLOR
}
skinparam participant<<stereo>> {
    BackgroundColor ENTITY_BG_COLOR
    BorderColor ENTITY_BORDER_COLOR
}
!enddefinelong

!definelong Entity(e_alias, e_label, e_color, e_sprite, e_stereo)
rectangle "==e_label\\n<color:e_color><$e_sprite></color>\\n" <<e_stereo>> as e_alias
!enddefinelong

!definelong EntityWithNote(e_alias, e_label, e_note, e_color, e_sprite, e_stereo)
rectangle "==e_label\\n<color:e_color><$e_sprite></color>\\n//<size:TECHN_FONT_SIZE>[e_note]</size>//" <<e_stereo>> as e_alias
!enddefinelong

"""

template = """' START entity_name
$image_content
EntityColoring($entity_name)
!define $entity_name(e_alias, e_label) Entity(e_alias, e_label, #232F3E, $entity_name, $entity_name)

!define ${entity_name}WithNote(e_alias, e_label, e_note) EntityWithNote(e_alias, e_label, e_note, #232F3E, $entity_name, $entity_name)

' END entity_name

"""
string_template = Template(template)


for entity_image in entity_images:
    entity_image_path = Path(entity_image)
    entity_name = entity_image_path.stem

    image_completed_process = subprocess.run(["plantuml",  "-encodesprite", "16z", entity_image_path], stdout=subprocess.PIPE, check=True)
    image_content = image_completed_process.stdout.decode('utf-8')
    output = string_template.substitute(entity_name=entity_name, image_content=image_content)
    all_puml_content += output

all_puml_content += "\n@enduml"

all_puml_file = open(Path("all.puml"), mode="w")
all_puml_file.write(all_puml_content)
all_puml_file.close()
