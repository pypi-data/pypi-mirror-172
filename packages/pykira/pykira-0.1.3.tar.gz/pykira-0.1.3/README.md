pyKira
======
Lightweight Python 2 and Python 3 module to send and respond to UDP packets from Keene Electronic's IR-IP bridge.

Dependencies
------------
No dependencies outside the builtin python modules

How to Use
----------

    >> import pykira

    >> kira = pykira.KiraReceiver()
    >> kira.registerCode("exampleCodeName", "<IR CODE>")
    >> kira.registerCallback(callbackFunction)
    >> kira.start()

In this snippet, callbackFunction will be called with "exampleCodeName" every time the matching IR code is received.

How to Capture Codes:
----------
Use netcat!

    $ nc -k -u -l 65432

The port used here is the default port that Kira modules use. Please note, Kira packets are UDP. Codes sent by Kira start with "K " and be followed by a series of 4-digit hex values.

Other Code Types:
----------
In addition to native Kira code sequences, both KiraReceiver and KiraModule can use Pronto codes. Pronto codes must be obtained from third parties.

Additionally, KiraReceiver is able to use NEC codes. These will be of the form "XXXX XXXX" and must be obtained from your manufacturer.

Using in Home Assistant:
----------
PyKira primarily exists to be used as a platform in Home Assistant. When the kira platform is first loaded, a file named ```kira_codes.yaml``` will be created in your configuration directory. You will need to add each code the kira platform should respond to here.

An example might look like this:

```
- name: LivingRoomTVOn
  code: "K 2322 228A 1126 023E 0227 023E 0207 023F 0658 025D 0207 023F 0227 0220 0227 023F 0222 023E 0222 0220 067D 023F 0658 0222 0227 025C 0640 023F 0658 025D 0640 023E 0658 025D 0640 023F 0222 025C 0207 0222 0678 023E 0207 023F 0227 023F 0222 025C 063B 025C 0640 023E 0660 023E 0658 025D 0207 0222 0678 023E 0660 0220 0678 023E 0202 025D 0207 023F 2000"
- name: LivingRoomTVOff
  code: "K 2322 22A7 1113 0220 0222 027A 01FA 025C 0640 023F 0222 025C 0202 023F 020F 023E 0222 025C 0202 025D 0640 023F 0658 023F 020F 023E 0658 025D 0640 023F 0658 025D 0640 023F 0658 025D 0640 023F 0222 025C 0640 023F 0222 023E 0207 025D 0207 025D 063B 025C 0640 025D 0202 023F 0658 023F 0227 023F 0658 023F 0660 023E 0640 023F 0227 025D 0202 025D 2000"
```

License
-------
This code is released under the MIT license.
