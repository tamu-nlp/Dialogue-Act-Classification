TAMU Dialogue Act Classifier (TDAC) Testing
============================

The Texas A&M Dialog Act Classifier runs on the Testbed Message Bus.  It subscribes to the following topics:
```
agent/asr/final
agent/control/rollcall/request
trial
minecraft/chat
```

It publishes messages on the following topics:
```
agent/uaz_tdac_agent/versioninfo
agent/dialog_act_classifier
agent/control/rollcall/response
agent/dialogue_act_classfier/heartbeat
```

Each input and output topic is tested, you can also run 'all' to run everything at once.
