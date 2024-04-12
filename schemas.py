from datetime import datetime
from enum import Enum
from typing import Annotated, Union

from pydantic import BaseModel, Field, ValidationError, constr


class Weapon(str, Enum):
    sword = "sword"
    axe = "axe"
    mace = "mace"
    spear = "spear"
    bow = "bow"
    crossbow = "crossbow"


class Armor(str, Enum):
    leather = "leather"
    chainmail = "chainmail"
    plate = "plate"


class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"
    black = "black"
    white = "white"
    brown = "brown"


class Character(BaseModel):
    name: constr(max_length=10)
    age: int
    armor: Armor
    weapon: Weapon
    strength: int


class BoyCharacter(BaseModel):
    name: constr(max_length=10)
    age: int
    armor: Armor
    weapon: Weapon
    strength: int


class GirlCharacter(BaseModel):
    name: constr(max_length=10)
    age: int
    armor: Armor
    weapon: Weapon
    strength: int
    shoe_color: Color
    hair_color: Color


class MainCharacter(BaseModel):
    character: Union[BoyCharacter, GirlCharacter]


def custom_datetime_schema():
    return {
        "type": "string",
        "format": "date-time",
    }


class Marking(str, Enum):
    unclassified = "U"
    classified = "C"
    secret = "S"
    top_secret = "TS"
    fouo = "U//FOUO"


def parse_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as e:
        raise ValidationError([str(e)])


class CatalogMaintenanceObjective(BaseModel):
    sensor_name: str
    data_mode: str
    classification_marking: Marking
    patience_minutes: int = Field(default=30)
    end_time_offset_minutes: int = Field(default=20)
    objective_name: str = Field(default="Catalog Maintenance Objective")
    objective_start_time: Annotated[datetime, Field(default_factory=datetime.now)]
    objective_end_time: Annotated[datetime, Field(default_factory=datetime.now)]
    priority: int = Field(default=10)

    _parse_objective_start_time = parse_datetime
    _parse_objective_end_time = parse_datetime


char_schema = """{
    "title": "Character",
    "type": "object",
    "properties": {
        "name": {
            "title": "Name",
            "maxLength": 10,
            "type": "string"
        },
        "age": {
            "title": "Age",
            "type": "integer"
        },
        "armor": {"$ref": "#/definitions/Armor"},
        "weapon": {"$ref": "#/definitions/Weapon"},
        "strength": {
            "title": "Strength",
            "type": "integer"
        }
    },
    "required": ["name", "age", "armor", "weapon", "strength"],
    "definitions": {
        "Armor": {
            "title": "Armor",
            "description": "An enumeration.",
            "enum": ["leather", "chainmail", "plate"],
            "type": "string"
        },
        "Weapon": {
            "title": "Weapon",
            "description": "An enumeration.",
            "enum": ["sword", "axe", "mace", "spear", "bow", "crossbow"],
            "type": "string"
        }
    }
}"""

main_char_schema = """{
  "title": "MainCharacter",
  "type": "object",
  "properties": {
    "character": {
      "title": "Character",
      "anyOf": [
        {"$ref": "#/definitions/BoyCharacter"},
        {"$ref": "#/definitions/GirlCharacter"}
      ]
    }
  },
  "required": ["character"],
  "definitions": {
    "BoyCharacter": {
      "title": "BoyCharacter",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "maxLength": 10,
          "type": "string"
        },
        "age": {
          "title": "Age",
          "type": "integer"
        },
        "armor": {"$ref": "#/definitions/Armor"},
        "weapon": {"$ref": "#/definitions/Weapon"},
        "strength": {
          "title": "Strength",
          "type": "integer"
        }
      },
      "required": ["name", "age", "armor", "weapon", "strength"]
    },
    "GirlCharacter": {
      "title": "GirlCharacter",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "maxLength": 10,
          "type": "string"
        },
        "age": {
          "title": "Age",
          "type": "integer"
        },
        "armor": {"$ref": "#/definitions/Armor"},
        "weapon": {"$ref": "#/definitions/Weapon"},
        "strength": {
          "title": "Strength",
          "type": "integer"
        },
        "shoe_color": {"$ref": "#/definitions/Color"},
        "hair_color": {"$ref": "#/definitions/Color"}
      },
      "required": ["name", "age", "armor", "weapon", "strength", "shoe_color", "hair_color"]
    },
    "Armor": {
      "title": "Armor",
      "description": "An enumeration.",
      "enum": ["leather", "chainmail", "plate"],
      "type": "string"
    },
    "Weapon": {
      "title": "Weapon",
      "description": "An enumeration.",
      "enum": ["sword", "axe", "mace", "spear", "bow", "crossbow"],
      "type": "string"
    },
    "Color": {
      "title": "Color",
      "description": "An enumeration.",
      "enum": ["red", "green", "blue", "black", "white", "brown"],
      "type": "string"
    }
  }
}"""

main_char_schema2 = """{
  "title": "MainCharacter",
  "type": "object",
  "properties": {
    "character": {
      "title": "Character",
      "anyOf": [
        {"$ref": "#/definitions/BoyCharacter"},
        {"$ref": "#/definitions/GirlCharacter"}
      ]
    }
  },
  "required": ["character"],
  "definitions": {
    "BoyCharacter": {
      "title": "BoyCharacter",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "maxLength": 10,
          "type": "string"
        },
        "age": {
          "title": "Age",
          "type": "integer"
        },
        "armor": {"$ref": "#/definitions/Armor"},
        "weapon": {"$ref": "#/definitions/Weapon"},
        "strength": {
          "title": "Strength",
          "type": "integer"
        }
      },
      "required": ["name", "age", "armor", "weapon", "strength"],
      "not": {
        "anyOf": [
          {"required": ["shoe_color"]},
          {"required": ["hair_color"]}
        ]
      }
    },
    "GirlCharacter": {
      "title": "GirlCharacter",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "maxLength": 10,
          "type": "string"
        },
        "age": {
          "title": "Age",
          "type": "integer"
        },
        "armor": {"$ref": "#/definitions/Armor"},
        "weapon": {"$ref": "#/definitions/Weapon"},
        "strength": {
          "title": "Strength",
          "type": "integer"
        },
        "shoe_color": {"$ref": "#/definitions/Color"},
        "hair_color": {"$ref": "#/definitions/Color"}
      },
      "required": ["name", "age", "armor", "weapon", "strength", "shoe_color", "hair_color"]
    },
    "Armor": {
      "title": "Armor",
      "description": "An enumeration.",
      "enum": ["leather", "chainmail", "plate"],
      "type": "string"
    },
    "Weapon": {
      "title": "Weapon",
      "description": "An enumeration.",
      "enum": ["sword", "axe", "mace", "spear", "bow", "crossbow"],
      "type": "string"
    },
    "Color": {
      "title": "Color",
      "description": "An enumeration.",
      "enum": ["red", "green", "blue", "black", "white", "brown"],
      "type": "string"
    }
  }
}"""

cmo_schema = """{
  "title": "CatalogMaintenanceObjective",
  "type": "object",
  "properties": {
    "sensor_name": {
      "title": "Sensor Name",
      "type": "string"
    },
    "data_mode": {
      "title": "Data Mode",
      "type": "string"
    },
    "classification_marking": {"$ref": "#/definitions/Marking"},
    "patience_minutes": {
      "title": "Patience Minutes",
      "type": "integer",
      "default": 30
    },
    "end_time_offset_minutes": {
      "title": "End Time Offset Minutes",
      "type": "integer",
      "default": 20
    },
    "objective_name": {
      "title": "Objective Name",
      "type": "string",
      "default": "Catalog Maintenance Objective"
    },
    "objective_start_time": {
      "title": "Objective Start Time",
      "type": "string",
      "format": "date-time",
      "default": "CURRENT_DATETIME"
    },
    "objective_end_time": {
      "title": "Objective End Time",
      "type": "string",
      "format": "date-time",
      "default": "CURRENT_DATETIME"
    },
    "priority": {
      "title": "Priority",
      "type": "integer",
      "default": 10
    }
  },
  "required": ["sensor_name", "data_mode", "classification_marking", "patience_minutes", "end_time_offset_minutes", "objective_name", "objective_start_time", "objective_end_time", "priority"],
  "definitions": {
    "Marking": {
      "title": "Marking",
      "description": "An enumeration of classification markings.",
      "enum": ["U", "C", "S", "TS", "U//FOUO"],
      "type": "string"
    }
  }
}"""

schemas = {
    "char_schema": char_schema,
    "main_char_schema": main_char_schema,
    "main_char_schema2": main_char_schema2,
    "cmo_schema": cmo_schema,
}
