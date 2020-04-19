# TezosTpVote
Serinkan Asci 3A IBC TP de vote en PascaLIGO


tezos mise en place des nodes :
cd tezos
./src/bin_node/tezos-sandboxed-node.sh 1 --connections 1 &
eval `./src/bin_client/tezos-init-sandboxed-client.sh 1`
tezos-client rpc get /chains/main/blocks/head/metadata
tezos-activate-alpha
tezos-client rpc get /chains/main/blocks/head/metadata
tezos-client list known addresses

compile contract:
cd ../voting
ligo compile-contract src/voting.ligo main > src/voting.tz

Dry Run pour tester : 
ligo dry-run --sender=tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV src/voting.ligo main 'SetAdmin(("tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV":address))' 'record votes = (map[] : map(address, bool)); admin = ( "tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV": address); voteCount = 1; state = ""; paused = False; end'

compile storage :
ligo compile-storage src/voting.ligo main 'record votes = (map[] : map(address, bool)); admin = ( "tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV": address); voteCount = 0; state = ""; paused = False; end'
Retourne :
(Pair (Pair (Pair "tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV" False) (Pair "" 0)) {})

tezos-client originate contract votingContract transferring 10 from bootstrap1 running src/voting.tz --init '(Pair (Pair (Pair "tz1TGu6TN5GSez2ndXXeDX6LgUDvLzPLqgYV" False) (Pair "" 0)) {})' --burn-cap 4.178 &

tezos-client bake for bootstrap1

ligo compile-parameter src/voting.ligo main "Vote(record state=True; end)"
Retourne :
(Right True)

Lancement des tests :
pytest tests/votingTest.py