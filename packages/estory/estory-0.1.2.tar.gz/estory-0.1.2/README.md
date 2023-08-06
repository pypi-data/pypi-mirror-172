# estory — read from and write to event stores

```console
$ estory init <IDENTIFIER>
$ estory read <IDENTIFIER>
$ estory write <IDENTIFIER>
$ estory guess <IDENTIFIER>
```

**IDENTIFIER** is either:

- a proper DSN (`driver://user:password@host:port/database`) ;
- a file that will be interpreted as a DSN (`sqlite:///<FILE>`) ;
- a name matching an environment variable (`ESTORY_DSN_<NAME>`).

To initialise an event store:

```console
$ export ESTORY_DSN_TMP="sqlite:////tmp/event_store.sqlite"
$ estory init TMP
```

To write an event to a store:

```console
$ jo stream="uuid" version=1 name="EventName" data=$(jo id=1) unixtime=$(date +%s) | estory write TMP
```

To read events from a store:

```console
$ estory read TMP
{"stream": "uuid", "name": "EventName", "data": {"id": 1}, "unixtime": 1647876362, "who": "", "id": 1}
```

To copy events from one store to another:

```console
$ export ESTORY_DSN_TMP2="sqlite:////tmp/another_event_store.sqlite"
$ estory init TMP2
$ estory read TMP | estory write TMP2
```

To copy only some events from one store to another:

```console
$ estory read TMP | jq '.|select(.id==2)' | estory write TMP2
```

To modify events while copying them from one store to another:

```console
$ estory read TMP | jq '.|.name="EventNewName"' | estory write TMP2
```
