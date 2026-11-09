# Mad Poker Challenge: Hand Structure

_How every hand in a video is built. For Ben (script and VO) and Karim (edit and graphics)._

## Basics

- **Show:** Mad Poker Challenge, a YouTube poker vlog. NLH cash games at Casino Gran Vía, Madrid.
- **On screen:** Ben is "Ben60".
- **Edit:** Karim.
- **Positions:** U8, U7, LJ, HJ, CO, BTN, SB, BB.
- **Villain names:** recurring villains get a fixed name ("Scandi reg", "Splashy"). One-off players are named by position only.
- **Writing:** simple English. No em dashes.
- **Length:** max 2:00 per hand.

## Core: every hand (~45 sec, max ~100 words of VO)

| # | Part | What it does |
|---|---|---|
| 1 | Hand card | Graphic only. Stake, Ben60 position + cards, villain(s). |
| 2 | Setup | One sentence: the read, and why I play it this way. |
| 3 | Action | The graphic shows the streets. The VO only says the plan. |
| 4 | Key moment | The one decision that makes the hand. One reason. |
| 5 | Result + takeaway | One line each. |

## Add-ons (~20 sec, ~35 words each)

| Add-on | What it does |
|---|---|
| Range | Cut villain's range to 2 hands, with a graphic. |
| Second decision | Explain one more street. |
| Table moment | Snap call, reaction, what villain said. |
| Pause & Play | Later episodes. |

## Sizes

| Size | What's in it | Length |
|---|---|---|
| Quick | Core only | ~45 sec |
| Standard | Core + 1 add-on | ~1:15 |
| Big | Core + 2 add-ons | max 2:00 |

**Never 3 add-ons.**

## Rules

- Never show the result before the decision.
- The VO doesn't repeat what the graphic shows (sizes, board).

## Worked example: the 99 hand (Big)

Big = river as key moment + preflop as second decision + table moment.

**Hand card (graphic):** Ben60 (SB) 99 · Tight reg (LJ) · LAG (BTN) · loose passive (BB) · [stake]

**Preflop (second decision):**
> "Nines in the small blind. A tight reg opens, a loose aggressive player calls on the button, and the big blind is loose and passive. Those two are my targets. A 3-bet only isolates the reg, the one player I don't want. So I call."

**Action:**
> "King, nine, eight. Set. The reg bets 13, the button calls. I want the money in over three streets, so I check-raise to 70. Only the reg calls. Turn is a blank. I bet 140, a size his draws and his strong hands both call."

**River (key moment):**
> "River, three of hearts. I fill up, and the flush gets there. I can bet small for ace-king. But at these stakes, ace-five of hearts won't raise me. Too much money. So I go after the flushes. All-in, 300."

**Table moment:**
> "Snap call. Am I beat? Eights? I show the nines. He mucks. Ace-king, with the ace of hearts. And he had a reason."

**Takeaway:**
> "Thinking players find a GTO reason to call. Other players find a reason to fold."

**VO length:** ~167 words. The Big budget is ~170 (100 core + 2 × 35).

### Still open for the 99 graphic

- [ ] The stake.
- [ ] The opener: LJ or U7.
- [ ] Which flop cards were hearts.

**What the script already fixes for the board:**

- **Turn:** a 3, not a heart. The river 3 of hearts only "fills up" the set of nines if the turn was a 3. (A K, 9 or 8 on the turn would have filled up already.)
- **Flop:** exactly two of K, 9, 8 are hearts. The river is the third heart, and the flush only "gets there" on the river.

## Template for a new hand

```
Hand:          [short name]          Size: Quick / Standard / Big
Hand card:     Ben60 ([pos]) [cards] · [villain] ([pos]) · [stake]
Setup:         [1 sentence: the read, and why I play it this way]
Action:        [the plan only, no sizes, no board]
Key moment:    [the 1 decision + 1 reason]
Result:        [1 line]
Takeaway:      [1 line]
Add-on 1:      [Standard and Big only]
Add-on 2:      [Big only]
```
