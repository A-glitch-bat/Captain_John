# Architecture

## Launcher

- Always-on Rust launcher
- Bubble view
- Small panel view
  - Show backend status
  - Start/stop backend, keep tabs on it
  - Show frontend status
  - Start frontend, keep tabs on it
  - Open Cyberspace


## Frontend

- Main PyQt interface with no heavy startup. Done already, very easy
- Backend-dependent controls shown as disabled when backend is offline


## Backend

- Router bot / intent classification
- Main bot route handling
- Schizobot / local chat model
- Summarizer
- Web search / scraping
- Whisper transcription
- Vosk wake word listener
- Text-to-speech
- Spotify API control
- Timer execution
- Error logging
- System performance logging
- Database
- Raspberry Pi server routes
- Heavy model loading
- Long-running workers

