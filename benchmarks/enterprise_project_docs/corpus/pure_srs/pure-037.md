# 1995 - gemini - 6. hardware interlocks - these will prevent both software and hardware from action - there

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 1995 - gemini.pdf

Section: 6. hardware interlocks - these will prevent both software and hardware from action - there

6. hardware interlocks - these will prevent both software and hardware from action - there
will be no bypass of these systems
7. hard stops - the mechanism cannot move beyond this point due to mechanical limit(s). In
general hard stops will use dampers to avoid damage to equiment.

A TTRIBUTES
The Gemini 8m Telescopes software shall be able to bring the Gemini 8m Telescopes
system quickly to a safe state upon detection of danger. Safety aspects shall be analyzed during the functional specification phase of the software.
Security must be provided in order to both prevent accidental mix-up of commands
from different users on different parts of the system and to prevent intrusion from the
wide area network into the Gemini 8m Telescopes. In particular, the astronomical
database must be protected from intrusion, whether the purpose is to access private
data or to be destructive. It is acceptable, and may well prove to be the best solution,
to provide intrusion security by a well designed network gateway acting as a firewall.
A system that is operating in Engineering/Maintenance mode must ignore directives
from other systems, though status information should still be provided for use by
other systems.
There should be security preventing the intrusion into the system by unauthorized
users, or users at unauthorized access levels.
All systems are appropriately interlocked. This interlock must not depend on any
software for reliable operation. Details of the interlock system are found in the Mount
Control System Work Package Definition.
The interlock philosophy is as follows:

•All hazards capable of causing death and/or loss of irreplacable equipment shall be
passively interlocked.

•All hazards capable of causing injury and/or severe damage to equipment shall be
actively interlocked (severe damage implies that repairs are not repairable at the
depot level.

•All other hazards may be interlocked via software.
The precedence for conforming to safety requirements will be:
