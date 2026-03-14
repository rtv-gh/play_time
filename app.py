import streamlit as st
import math
from utils import allocate_halves, build_schedule

st.set_page_config(
    page_title="U10 Rugby Festival Planner",
    page_icon="🏉",
    layout="centered",
)

st.title("🏉 U10 Rugby Festival Planner")
st.caption("Equal playing time for every player")

# ── Step 1: Tournament setup ──────────────────────────────────────────────────
st.header("1. Tournament Setup")

col1, col2 = st.columns(2)
with col1:
    num_games = st.selectbox("Number of games", [4, 5], index=1)
with col2:
    st.metric("Players per side (RFU U10)", 8, delta=None)

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

if num_players < 8:
    st.error("⚠️ You need at least 8 players.")
    st.stop()

total_slots = num_games * 2 * 8  # games × halves × players per side
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
    schedule = build_schedule(players, halves_each, num_games)
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
