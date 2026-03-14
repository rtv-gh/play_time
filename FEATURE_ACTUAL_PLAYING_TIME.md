# Actual Playing Time Recording Feature

## Overview

Your app now includes a powerful feature for coaches to record **who actually played** in each match, accounting for injuries, substitutions, and other ad-hoc changes. This allows accurate tracking of real-world playing time vs. the planned schedule.

## Workflow

### Step 1-4: Create Schedule (Existing)
1. Select age group (U7-U11)
2. Set number of games
3. Edit player squad
4. Name opposition teams
5. Generate schedule

### Step 5: Record Actual Playing Time (NEW)
After the schedule is generated, a new section appears:

**"5. Record Actual Playing Time"**

For each game and each half:
- All squad members appear as **checkboxes** in a 3-column layout
- **Pre-checked**: Players scheduled for that half
- **Action**: Coaches check/uncheck to match actual playing roster
- **Feedback**: Shows ✓ or ⚠️ indicator with count comparison

#### Use Cases:
- **Injury**: Uncheck player who was scheduled but injured
- **Last-minute Sub**: Check a player who wasn't scheduled but played
- **Miscommunication**: Adjust if actual lineup differs from plan
- **Late arrival**: Check player who arrived after schedule set

#### Example:
```
Game 1 — vs Blackheath
1st Half — Check who actually played:
☑ Seb  ☑ Albie  ☑ Henry
☐ Ben  ☑ Pierce ☑ George
...
✓ 7 players (7 planned)  ← Normal
```

vs.

```
(If player Ben got injured but Arthur played instead)
1st Half — Check who actually played:
☑ Seb  ☑ Albie  ☑ Henry
☐ Ben  ☑ Pierce ☑ George  ← Ben unchecked (injured)
☑ Arthur  ← Arthur checked (unexpected sub)
...
⚠️ 7 players (7 planned)  ← Flag: different composition
```

### Step 6: Actual Playing Time Summary
Shows comparison between **Scheduled vs Actual**:

- **✓**: Player played exactly as scheduled (no issues)
- **+Xh**: Player played MORE than scheduled (substitution in their favor)
- **-Xh**: Player played LESS than scheduled (injury/left bench)

Example:
```
Albie: 3h ✓        (scheduled 3, played 3)
Arthur: 2h +1h     (scheduled 1, played 2 - unexpected sub)
Ben: 1h -1h        (scheduled 2, played 1 - injured)
```

### Step 7: Export Results
**"📥 Download actual playing time (CSV)"** button

Downloads `actual_playing_time.csv` containing:
```
Player,Scheduled Halves,Actual Halves,Difference
Albie,3,3,0
Arthur,1,2,1
Ben,2,1,-1
...
```

**Use for**:
- Archive records for the tournament
- Parent communication (official playing time record)
- Performance analysis
- Restoring app session if browser closes

## Best Practices for Coaches

### During Tournament:
1. ✓ Keep the browser tab **open** throughout all games
2. ✓ After each game/half, quickly check/uncheck boxes
3. ✓ Watch for the count indicators (✓ or ⚠️)
4. ✓ Refer to the schedule (Step 4) when needed

### If Browser Closes:
1. Generate the schedule again (same setup)
2. ✓ Download CSV from your last session (if saved)
3. ✓ Re-create actual playing time from records
4. ✓ Or export again to backup current session

### Tips:
- **Pre-game**: Review the schedule together with coaching staff
- **At halftime**: Gather actual roster, quickly update checkboxes
- **Post-game**: Download & save CSV before leaving
- **For records**: Keep CSVs with tournament folder for reference

## Technical Details

### Data Storage:
- **Session State**: Lives in browser while tab is open
- **Not persistent** across page refreshes or browser close
- **CSV export** is the permanent record

### Session Management:
- Keep app running during entire tournament (4-6 hours typical)
- Modern browsers handle this well
- If crash occurs, regenerate schedule and re-enter actuals

### Mobile Friendly:
- Checkboxes work on touch screens
- Responsive layout for tablets
- Good for sideline use during matches

## Example Scenario

**Tournament: Friday afternoon, 3 games**

```
Pre-game:
- Coach generates schedule at 1:00 PM
- Reviews with assistants

Game 1 (1:15-1:45):
- During halftime: Updates 1st half checkboxes
- After game: Updates 2nd half checkboxes

Game 2 (2:00-2:30):
- Updates both halves

Game 3 (2:45-3:15):
- Updates both halves

Post-tournament (3:45 PM):
- Reviews Actual vs Scheduled summary
- Clicks "Download CSV"
- Sends summary email to parents
- Keeps CSV for records

Result: Complete, accurate playing time record with zero additional effort!
```

## Troubleshooting

### Q: I unchecked someone but the count didn't change
**A**: The count shows both scheduled and actual. Try refreshing understanding - it counts checked boxes.

### Q: Can I restore a previous session?
**A**: Download CSV before closing. To restore: regenerate schedule, then manually re-enter from CSV or memory.

### Q: What if I make a mistake?
**A**: Simply check/uncheck again. Changes are instant. Download CSV when final.

### Q: Does this work on mobile?
**A**: Yes! Open `streamlit run app.py` and access via phone browser. Checkboxes work with touch.

---

**Feature added**: March 2026  
**Status**: Ready for deployment to Streamlit Community Cloud
