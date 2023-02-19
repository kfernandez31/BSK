# Finding the flag in code
This subtask can be brute-forced by just found by scrolling through the `.rdata` section of the task's executable. For the unmodified executable and the flag contents are:
```
FLAG{gr3pp!ng-thr0ugh-str1ngs?-isn't-th4t-t0o-ez?}
```

# Finding the flag in-game
By viewing the `.rdata` section in IDA one can find the address of a function each string constant corresponds to, where it is displayed. For the flag-string, that is `player_mailbox` where it is passed in the `RCX` register. Inside `player_mailbox`, the flag would have been passed to the `show_text` function if not for the conditional jump that occurs when `check` returns `0`. After examinining `check` and similar functions `mark` and `clear` one sees they in fact do the bit operations their names suggest on a bitmap from the `data` section. For all intents and purposes, the bitmap represents the game state and the (fifth) bit checked by `check` holds information on whether to display the usual mailbox message or the flag. 

A reference to the aforementioned bitmap can be found in `overworld_keypress`, where if the key pressed is not the spacebar, it is checked whether after xor'ing with `0x6A` the key matches the i-th character in `"\t\v\x04\x03\x02\v\x10\f\x06\v\r\x1A\x06\x12"`. After decrypting each byte with xor, the string becomes `"canihazflagplx"`. After entering this key combination in-game, the flag is then displayed.

# Unconditional noclip
This can be achieved by modifying just one byte! In the `player_step` function, one can modify the conditional jump that occurs after checking `object_can_move`'s result from being a `JZ` to a `JS`. As that function returns only `0` or `1`, the sign flag will not be set either case, so this jump will never occur and as a result each obstacle becomes passable.

# Noclip when holding the SHIFT key
To achieve this, I replaced `CALL player_step` with a `JMP` to a segment of code that I wrote in place of blocks of `INT3`. This code was essentially a function that performed:
```c
return object_can_move() || (keyboard_state(lshift) == 1);
```
