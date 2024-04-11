"""FastAPI server for handling Large Language Model (LLM) requests."""

from datetime import datetime
from enum import Enum
from typing import Optional, Union

import vllm
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from langchain.llms import VLLM
from outlines.serve.vllm import JSONLogitsProcessor
from pydantic import BaseModel, Field, ValidationError, constr
from typing_extensions import Annotated

from config import Settings

# from llm_agent.llm_agent import LLMAgent
# from llm_agent.llm_memory import MemoryLLM
from llm_agent.llm_router import LLMRouter

settings = Settings()


class GenerateRequest(BaseModel):
    """Schema for LLM text generation request."""

    text: str


class CustomVLLM(VLLM):
    """Custom VLLM class with additional attributes and methods."""

    def generate(self, prompt, sampling_params):
        return self._generate([prompt], **sampling_params.__dict__)


def create_llm(
    quantization: Optional[str] = None, use_agent: Optional[bool] = False
) -> CustomVLLM:
    """Creates and returns CustomVLLM instance based on current configuration."""
    if quantization is None:
        gpu_utilization = settings.DEFAULT_GPU_UTIL
        dtype_value = "bfloat16"
    else:
        gpu_utilization = getattr(
            settings, f"{quantization.upper()}_GPU_UTIL", settings.DEFAULT_GPU_UTIL
        )
        dtype_value = "half" if quantization in ["awq", "gptq"] else "bfloat16"

    try:
        llm = CustomVLLM(
            model=settings.DEFAULT_MODEL,
            temperature=settings.TEMPERATURE,
            use_beam_search=False,
            max_new_tokens=settings.MAX_TOKENS,
            tensor_parallel_size=settings.NUM_GPUS,
            trust_remote_code=False,
            dtype=dtype_value,
            vllm_kwargs={
                "quantization": quantization,
                "gpu_memory_utilization": gpu_utilization,
                # "max_model_len": settings.MAX_SEQ_LEN,
            },
        )

        if use_agent:
            return LLMRouter(llm=llm)
        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}")


# Initialize configurations and dependencies
# quantization = os.environ.get("QUANTIZATION", "None")
# quantization = quantization if quantization != "None" else None

quantization = "gptq" if "GPTQ" in settings.DEFAULT_MODE else "None"
llm = create_llm(quantization="gptq", use_agent=settings.USE_AGENT)

app = FastAPI()


def get_llm_instance():
    """Function to retrieve the LLM instance."""
    return llm


def get_llm():
    """Dependency injector for the LLM.

    Useful for testing the /generate endpoint. Easily swap LLM with a mock or stub
    during testing.
    """
    try:
        return get_llm_instance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# sampler._apply_logits_processors = _patched_apply_logits_processors


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


char_schema = '''{
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
}'''

main_char_schema = '''{
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
}'''

main_char_schema2 = '''{
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
}'''

cmo_schema = '''{
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
}'''

logits_processor = JSONLogitsProcessor(
    main_char_schema2, llm.client.llm_engine
)


@app.post("/generate")
async def generate(request: Request, llm: CustomVLLM = Depends(get_llm)):
    """Endpoint to generate text using LLM."""
    try:
        request_data = await request.json()
        query = GenerateRequest(**request_data).text
        # response = llm(query)
        response = llm.generate(
            query,
            sampling_params=vllm.SamplingParams(
                max_tokens=settings.MAX_TOKENS,
                logits_processors=[logits_processor],
            ),
        )
        return JSONResponse({"text": response.generations[0][0].text})
        # return JSONResponse({"text": response})
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing user request: {e}"
        )
