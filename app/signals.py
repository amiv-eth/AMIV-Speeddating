from app import participant_signals

# Emitted, every time a participant submits the signup form
new_signup = participant_signals.signal('new-signup')
