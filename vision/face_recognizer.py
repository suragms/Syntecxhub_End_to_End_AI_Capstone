"""Optional identity recognition is deliberately not enabled in SURA AI.

The mandatory workflow performs only face presence detection. This module exists
as a clear extension point and prevents accidental claims of authentication.
"""
class FaceRecognizer:
    enabled = False
    def verify(self, *args, **kwargs):
        raise NotImplementedError("Identity recognition is not implemented; use face presence demo mode")
