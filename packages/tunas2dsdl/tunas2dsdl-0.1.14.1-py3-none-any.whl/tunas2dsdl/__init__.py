from tunas2dsdl.generator.generate import Generation
from tunas2dsdl.parser import DetectionParse, SemanticSegmentationParse
from .general.classdomain import ClassDomain, Label
from .general.struct import Struct, Field
from .general import OptionEatAll
from .__version__ import __version__

__all__ = [
    "Generation",
    "DetectionParse",
    "ClassDomain",
    "Label",
    "Struct",
    "Field",
    "OptionEatAll",
    "__version__",
]
