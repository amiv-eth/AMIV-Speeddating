"""
Defines signals used for hooks.
"""
from app import participant_signals, event_signals

# Emitted, every time a participant submits the signup form
SIGNAL_NEW_SIGNUP = participant_signals.signal('new-signup')

# Emitted, each time an Events signup_open is automatically set to True
SIGNAL_REGISTRATION_OPENED = event_signals.signal('registration-opened')

# Emitted, each time an Events signup_open is automatically set to False
SIGNAL_REGISTRATION_CLOSED = event_signals.signal('registration-closed')
