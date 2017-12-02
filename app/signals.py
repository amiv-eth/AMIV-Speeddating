"""
Defines signals used for hooks.
"""
from app import participant_signals

# Emitted, every time a participant submits the signup form
SIGNAL_NEW_SIGNUP = participant_signals.signal('new-signup')
