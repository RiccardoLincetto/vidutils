import pytest
from numpy.typing import ArrayLike

from vidutils.artifacts import Artifact


def test_instantiation():
    with pytest.raises(TypeError):
        Artifact()


class MockArtifact(Artifact):
    name: str

    def draw(self, frame: ArrayLike) -> ArrayLike:
        return frame


@pytest.fixture
def mock_artifact() -> Artifact:
    return MockArtifact(name="MockArtifact")


def test_serialization(mock_artifact: MockArtifact):
    serialized = mock_artifact.json()
    assert isinstance(serialized, str)
    assert serialized == '{"name": "MockArtifact"}'


def test_deserialization(mock_artifact: MockArtifact):
    serialized = mock_artifact.json()  # checked in test_serialization
    deserialized = MockArtifact.parse_raw(serialized)
    assert isinstance(deserialized, Artifact)
    assert isinstance(deserialized, MockArtifact)
    assert deserialized.name == "MockArtifact"
