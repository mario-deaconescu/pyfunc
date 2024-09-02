import pytest

from pyfunc import OrError
from pyfunc.Trace import trace


@pytest.fixture
def sample_json():
    return '{\n  "Actors": [\n    {\n      "name": "Tom Cruise",\n      "age": 56,\n      "Born At": "Syracuse, NY",\n      "Birthdate": "July 3, 1962",\n      "photo": "https://jsonformatter.org/img/tom-cruise.jpg",\n      "wife": null,\n      "weight": 67.5,\n      "hasChildren": true,\n      "hasGreyHair": false,\n      "children": [\n        "Suri",\n        "Isabella Jane",\n        "Connor"\n      ]\n    },\n    {\n      "name": "Robert Downey Jr.",\n      "age": 53,\n      "Born At": "New York City, NY",\n      "Birthdate": "April 4, 1965",\n      "photo": "https://jsonformatter.org/img/Robert-Downey-Jr.jpg",\n      "wife": "Susan Downey",\n      "weight": 77.1,\n      "hasChildren": true,\n      "hasGreyHair": false,\n      "children": [\n        "Indio Falconer",\n        "Avri Roel",\n        "Exton Elias"\n      ]\n    }\n  ]\n}'

@trace
def test_json_parse(sample_json: str):
    from pyfunc.JSON import Parser, Object
    from pyfunc.Core import String

    result = OrError.ok_exn(Parser.parse(String.t(sample_json)))

    string = Object.to_json(result)
    assert string == sample_json
