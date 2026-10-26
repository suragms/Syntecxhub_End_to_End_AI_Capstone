from vision.face_verification import FacePresenceVerifier

def test_stable_single_face():
    verifier = FacePresenceVerifier(3)
    assert not verifier.update(1); assert not verifier.update(1); assert verifier.update(1)
def test_multiple_or_empty_resets():
    verifier = FacePresenceVerifier(2); verifier.update(1); assert not verifier.update(2); assert verifier.streak == 0
