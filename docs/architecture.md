# SURA AI architecture

SURA AI is a local, layered Windows desktop application. PySide6 renders the interface, `AssistantController` coordinates session state, the deterministic chatbot returns structured intents, and `CommandRouter` executes only reviewed allowlisted actions. OpenCV camera capture, speech recognition, and pyttsx3 are isolated behind service modules so failures do not crash typed chat.

## Safety boundary

The webcam workflow is a **face-presence demonstration check**. Haar detection confirms only that one face-like region is visible for consecutive frames. It does not identify a person or authenticate identity. No face images, biometric templates, microphone recordings, or cloud requests are stored by the application.
