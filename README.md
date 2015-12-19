### Description
midi-connect allows you to connect two MIDI-ports automatically. For example, you can connect MIDI-keyboard and synthesizer software once they both turned on.

### Usage
midi-connect.py port_from port_to

You can use the following formats to describe ports:
- client_name/port_name (e.g. "Midi Through/Midi Through Port-0")
- port_name (e.g. "Midi Through Port-0")

You can also use regular expressions to describe both client_name and port_name (e.g. "FLUID Synth.*/.*")
