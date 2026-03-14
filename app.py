import streamlit as st
import math
import csv
import io
from utils import allocate_halves, build_schedule

st.set_page_config(
    page_title="Rugby Festival Planner",
    page_icon="🏉",
    layout="centered",
)

st.title("🏉 Rugby Festival Planner")
st.caption("Equal playing time for every player")

# ── Step 1: Tournament setup ──────────────────────────────────────────────────
st.header("1. Tournament Setup")

# Age group to players per side mapping
age_group_map = {
    "U7 (4-a-side)": 4,
    "U8 (6-a-side)": 6,
    "U9 (7-a-side)": 7,
    "U10 (8-a-side)": 8,
    "U11 (9-a-side)": 9,
}

col1, col2, col3 = st.columns(3)
with col1:
    age_group = st.selectbox("Age group", list(age_group_map.keys()), index=1)
    players_per_side = age_group_map[age_group]
with col2:
    num_games = st.selectbox("Number of games", [3, 4, 5, 6], index=1)
with col3:
    st.metric("Players per side (RFU)", players_per_side, delta=None)

# ── Step 2: Squad ─────────────────────────────────────────────────────────────
st.header("2. Squad")

DEFAULT_PLAYERS = [
    "Seb", "Albie", "Henry", "Ben", "Pierce", "George",
    "Will", "Arthur", "RJ", "Antonio", "Daniel", "Mitchell",
    "Archie", "Jackson"
]

# Initialize with default players
raw = "\n".join(DEFAULT_PLAYERS)

with st.expander("✏️ Edit player names (tap to open)", expanded=False):
    raw = st.text_area(
        "One name per line",
        value=raw,
        height=300,
    )

players = [p.strip() for p in raw.splitlines() if p.strip()]
num_players = len(players)

if num_players < players_per_side:
    st.error(f"⚠️ You need at least {players_per_side} players for {age_group}.")
    st.stop()

total_slots = num_games * 2 * players_per_side  # games × halves × players per side
halves_each = allocate_halves(num_players, total_slots)

st.info(
    f"**{num_players} players** | **{num_games} games | "
    f"**{total_slots} half-time slots to fill"
)

# Show allocation summary
base = total_slots // num_players
remainder = total_slots % num_players
if remainder == 0:
    st.success(f"✅ Perfect split — every player gets **{base} halves**.")
else:
    fewer = num_players - remainder
    st.success(
        f"✅ Fair split — **{remainder} players** get **{base + 1} halves**, "
        f"**{fewer} players** get **{base} halves**."
    )

# ── Step 3: Opposition names ───────────────────────────────────────────────────
st.header("3. Opposition Teams")

opposition = []
for i in range(num_games):
    opp = st.text_input(f"Game {i + 1} — opposition", value="", key=f"opp_{i}",
                        placeholder="e.g. Blackheath, Bromley, Colfes, Dartfordians")
    opposition.append(opp.strip() if opp.strip() else f"TBC {i + 1}")

# ── Step 4: Schedule ───────────────────────────────────────────────────────────
st.header("4. Squad Selection")

if st.button("🎲 Generate schedule", type="primary", use_container_width=True):
    schedule = build_schedule(players, halves_each, num_games, players_per_half=players_per_side)
    st.session_state["schedule"] = schedule
    st.session_state["opposition"] = opposition

if "schedule" in st.session_state:
    schedule = st.session_state["schedule"]
    saved_opp = st.session_state.get("opposition", opposition)

    for g_idx, game in enumerate(schedule):
        opp_name = saved_opp[g_idx] if g_idx < len(saved_opp) else opposition[g_idx]
        st.subheader(f"Game {g_idx + 1} — vs {opp_name}")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.markdown("**1st Half**")
            for name in game["1st"]:
                st.markdown(f"- {name}")
        with col_h2:
            st.markdown("**2nd Half**")
            for name in game["2nd"]:
                st.markdown(f"- {name}")

    # Player tally
    st.subheader("📊 Playing time summary")
    tally = {p: 0 for p in players}
    for game in schedule:
        for half in ("1st", "2nd"):
            for name in game[half]:
                tally[name] += 1

    rows = sorted(tally.items(), key=lambda x: x[0])
    for name, count in rows:
        st.markdown(f"**{name}** — {count} half(ves)")

    # ── Step 5: Record Actual Playing Time ────────────────────────────────────
    st.header("5. Record Actual Playing Time")
    st.caption("💡 Adjust for injuries, substitutions, or other changes")

    # Initialize actual players tracking in session state
    if "actual_players" not in st.session_state:
        st.session_state["actual_players"] = {}

    actual_players_state = st.session_state["actual_players"]

    # Record actual players for each game and half
    for g_idx, game in enumerate(schedule):
        opp_name = saved_opp[g_idx] if g_idx < len(saved_opp) else opposition[g_idx]
        st.subheader(f"Game {g_idx + 1} — vs {opp_name}")

        for half_label in ("1st", "2nd"):
            scheduled = game[half_label]
            key_prefix = f"actual_{g_idx}_{half_label}"

            # Initialize this half's actual players if not exists
            if key_prefix not in actual_players_state:
                actual_players_state[key_prefix] = set(scheduled)

            st.markdown(f"**{half_label} Half** — Check who actually played:")

            # Display checkboxes in columns for compact layout
            cols = st.columns(3)
            for col_idx, player in enumerate(players):
                col = cols[col_idx % 3]
                with col:
                    is_checked = st.checkbox(
                        player,
                        value=player in actual_players_state[key_prefix],
                        key=f"check_{key_prefix}_{player}",
                    )
                    if is_checked:
                        actual_players_state[key_prefix].add(player)
                    else:
                        actual_players_state[key_prefix].discard(player)

            # Show count comparison
            scheduled_count = len(scheduled)
            actual_count = len(actual_players_state[key_prefix])
            if actual_count == scheduled_count:
                st.caption(f"✓ {actual_count} players ({scheduled_count} planned)")
            else:
                st.caption(f"⚠️ {actual_count} players ({scheduled_count} planned)")

    # ── Step 6: Actual Playing Time Summary ───────────────────────────────────
    st.header("6. Actual Playing Time Summary")

    actual_tally = {p: 0 for p in players}
    for key, selected_players in actual_players_state.items():
        for player in selected_players:
            actual_tally[player] += 1

    # Display actual vs scheduled comparison
    st.markdown("**Comparison: Scheduled vs Actual**")
    comparison_cols = st.columns(3)
    rows = sorted(actual_tally.items(), key=lambda x: x[0])
    for idx, (name, actual_count) in enumerate(rows):
        scheduled_count = tally[name]
        col = comparison_cols[idx % 3]
        with col:
            if actual_count == scheduled_count:
                st.metric(name, f"{actual_count}h", "✓")
            elif actual_count > scheduled_count:
                st.metric(name, f"{actual_count}h", f"+{actual_count - scheduled_count}h", delta_color="off")
            else:
                st.metric(name, f"{actual_count}h", f"{actual_count - scheduled_count}h", delta_color="off")

    # ── Step 7: Export Results ────────────────────────────────────────────────
    st.header("7. Export Results")

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Player", "Scheduled Halves", "Actual Halves", "Difference"])
    for name in sorted(players):
        scheduled = tally[name]
        actual = actual_tally[name]
        difference = actual - scheduled
        writer.writerow([name, scheduled, actual, difference])

    csv_content = csv_buffer.getvalue()
    st.download_button(
        label="📥 Download actual playing time (CSV)",
        data=csv_content,
        file_name="actual_playing_time.csv",
        mime="text/csv",
    )
