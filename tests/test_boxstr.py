import importlib.util
import sys
import types
import unittest
from pathlib import Path


def _load():
    seaborn = types.ModuleType("seaborn")
    sys.modules["seaborn"] = seaborn

    pil = types.ModuleType("PIL")
    pil.__path__ = []
    for name in ("Image", "ImageDraw", "ImageFont"):
        sub = types.ModuleType(name)
        setattr(pil, name, sub)
        sys.modules[f"PIL.{name}"] = sub
    sys.modules["PIL"] = pil

    mpl = types.ModuleType("matplotlib")
    mpl.__path__ = []
    font_manager = types.ModuleType("font_manager")
    mpl.font_manager = font_manager
    sys.modules["matplotlib"] = mpl
    sys.modules["matplotlib.font_manager"] = font_manager

    spacy = types.ModuleType("spacy")
    spacy.load = lambda *args, **kwargs: None
    sys.modules["spacy"] = spacy

    path = Path(__file__).resolve().parents[1] / "utils" / "utils" / "grounding_parser.py"
    spec = importlib.util.spec_from_file_location("grounding_parser", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = _load()


class BoxStringTest(unittest.TestCase):
    def test_a_box_with_spaces_keeps_its_corners(self):
        self.assertEqual(
            mod.boxstr_to_boxes("100, 200, 300, 400"),
            [[0.1, 0.2, 0.3, 0.4]],
        )

    def test_a_box_without_spaces_stays_the_same(self):
        self.assertEqual(
            mod.boxstr_to_boxes("100,200,300,400"),
            [[0.1, 0.2, 0.3, 0.4]],
        )


if __name__ == "__main__":
    unittest.main()
