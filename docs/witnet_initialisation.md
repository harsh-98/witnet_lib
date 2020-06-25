## Initialisation

When `witnet node server` is executed, the `src/cli/node/with_node` calls the module `node/src/actor/node.rs` where all the managers are initialised. Among all managers, the most interesting one `SessionManager`.

### Structure of Witnet Modules
There is usually `actor.rs`, `handler.rs` and `mod.rs`. 
- `actor.rs` is called when a new object of module is initialised.
- `handler.rs` is responisble for handling the messages sent to object via `do_send` function call.
- `module.rs` is where object struct and properties are defined.

### SessionManager
It starts bootstrapping of peers. For this, it calls `bootstrap_peers` function of connection_mngr which firstly connects to each ip, to check if the port is open or not. Connection_mngr then passes a `OutboundTcpConnect` message to `connection_manager/handler.rs` which inturn passes `Create` message to `SessionManager`. SessionManager creates a new Session for the peer, by calling `src/cli/node/session/actor.rs(started)`. Session passes the `register` message to session_manager and waits for `handshake_timeout` before terminating the connection.

`SessionManager` maintains session via `p2p/src/sessions`. This `sessions` is different from the previous discussed session module. This new `sessions` module is responsible for maintaining five types of connection. Namely:
- inbound Unconsolidated
- inbound concolidated
- Outbound unconsolidated
- Outbound consolidated
- Consensus outbound 

If the peer is connected via outbound connection, then its `sock_addr` goes from `outbound unconsolidated` -> `outbound consolidated` -> `consensus outbound`.

If the peer is connected via inbound connection, then its `sock_addr` goes from `inbound unconsolidated` -> `inbound consolidated`.

For moving from `unconsolidated` to `consolidated`. Handshake between the peers must take place. Under this 4 messages, two from each side are exchange. Namely Version and Verack. If any of these is not received by other side, then the connection is terminated after `handshake_timeout`.

```
                    Peer 1 --------- Peer 2
                       |  --Version-->  |
                       |                |
                       |  <--Version--  |
                       |                |
                       |  <--Verack--   |
                       |                |
                       |  --Verack-->   |
                    ########################
```

After the connection is consolidated, both parties maintain a `keep alive` connection.

`witnet_lib` does this handshake to start a `tcp connection` with the peers. And sends messages like `GetPeers` for getting the peers of the node, and iterates over them in a DAG(directed acyclic graph) fashion.