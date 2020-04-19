type voting is record [
  state : bool;
]

// variant defining pseudo multi-entrypoint actions
type action is
| Reset of int
| Vote of voting
| SetAdmin of address
| SetPaused of bool

type myVote is map(address, bool)

type storage is record [
  votes: myVote;
  admin: address;
  voteCount: int;
  state: string;
  paused: bool;
]

function isAdmin(const s: storage): bool is
    block { skip } with (sender = s.admin)

function setAdmin (const s : storage ; const newAdmin : address) : storage is
  block { if(sender = s.admin) then 
    s.admin := newAdmin
    else failwith("Not Admin cannot change admin")
  } with s

function setPaused (const s : storage ; const newPause : bool) : storage is
  block { if(sender = s.admin) then 
    s.paused := newPause
    else failwith("Not Admin cannot change paused state")
  } with s

function isPaused(const s: storage): bool is
    block { skip } with (s.paused)

function getFinalState (const s : storage) : string is
  block { 
    var cmpt : int := 0;
    for vt in map s.votes block {
      case s.votes[vt] of
        Some(bool) -> if bool = True then cmpt := cmpt + 1 else cmpt := cmpt
        | None -> block { skip }
      end
    };
    if cmpt > 5 then
      s.state := "Victoire"
    else if cmpt < 5 then
      s.state := "Defaite"
    else
      s.state := "Nul";
    // const finalstate : string = s.state;
  } with (s.state)

function setVote (const choice : bool ; const s : storage) : storage is
  block {
    if isAdmin(s) then 
      failwith("Admin is not able to vote !")
    else if isPaused(s) then 
      failwith("Vote is paused !")
    else 
      case s.votes[sender] of
        Some(bool) -> failwith("you have already voted !")
        | None -> block {
          s.votes[sender] := choice;
          s.voteCount := s.voteCount + 1;
          if s.voteCount = 10 then block {
            s.paused := True; 
            s.state := getFinalState(s);
          } else skip
        }
      end
  } with (s)

function resetVotes (const s : storage): storage is
  block { 
    if(isAdmin(s)) then block {
      s.voteCount := 0;
      s.state := "";
      s.paused := False;
      for vt in map s.votes block {
        remove(vt: address) from map s.votes
      };
    }
    else failwith("You are not the admin !");
  } with (s)

// real entrypoint that re-routes the flow based
// on the action provided
function main (const p : action ; const s : storage) : (list(operation) * storage) is
  block { skip } with ((nil : list(operation)),
  case p of
    | Reset(a) -> resetVotes(s)
    | Vote(v) -> setVote(v.state, s)
    | SetAdmin(a) -> setAdmin(s, a)
    | SetPaused(b) -> setPaused(s, b)
  end)