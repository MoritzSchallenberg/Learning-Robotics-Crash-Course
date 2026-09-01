#!/usr/bin/env bash
#
# course-preflight.sh -- read-only readiness check for the Learning Robotics
# Crash Course.
#
# Run this the day before a session, not during it. It only reads state; it
# never installs anything, changes configuration, deletes a file, reads a
# credential, or contacts a private network target.
#
# Usage:
#   bash scripts/course-preflight.sh
#
# Exit code is 0 if there is no FAIL, 1 if there is at least one FAIL.
# WARNING never affects the exit code -- it is worth reading, not blocking.

set -u

PASS=0
WARN=0
FAIL=0

# ---------------------------------------------------------------------------
# Small helpers. Every check follows the same three-line shape: a check, a
# verdict, and (on WARNING/FAIL) one concrete next step.
# ---------------------------------------------------------------------------

_pass() { echo "  PASS     $1"; PASS=$((PASS + 1)); }
_warn() { echo "  WARNING  $1"; [ -n "${2:-}" ] && echo "           -> $2"; WARN=$((WARN + 1)); }
_fail() { echo "  FAIL     $1"; [ -n "${2:-}" ] && echo "           -> $2"; FAIL=$((FAIL + 1)); }

section() { echo; echo "== $1 =="; }

have() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------------------
# 1. Operating system and version
# ---------------------------------------------------------------------------

section "Operating system"

if [ -r /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    OS_NAME="${NAME:-unknown}"
    OS_VERSION="${VERSION_ID:-unknown}"
    echo "  Detected: ${OS_NAME} ${OS_VERSION}"

    case "${OS_VERSION}" in
        24.04) _pass "Ubuntu 24.04 detected (matches the Jazzy / Carologistics track)" ;;
        22.04) _pass "Ubuntu 22.04 detected (matches the Humble / ALeRT track)" ;;
        *)
            _warn "Ubuntu ${OS_VERSION} is not one of the two versions this course tests against (22.04, 24.04)" \
                "check docs/reference/compatibility.md for which release your track expects"
            ;;
    esac
else
    _warn "Could not read /etc/os-release -- are you on Ubuntu?" \
        "this course assumes Ubuntu 22.04 or 24.04; see docs/prerequisites/installation.md"
fi

# ---------------------------------------------------------------------------
# 2. ROS 2 distribution and CLI
# ---------------------------------------------------------------------------

section "ROS 2"

if [ -n "${ROS_DISTRO:-}" ]; then
    _pass "ROS_DISTRO is set to '${ROS_DISTRO}'"
else
    _fail "ROS_DISTRO is not set in this shell" \
        "source /opt/ros/<distro>/setup.bash, or check it is in ~/.bashrc and open a new terminal"
fi

if have ros2; then
    _pass "the 'ros2' command is available"
else
    _fail "'ros2' is not on PATH" \
        "ROS 2 is not sourced in this terminal -- see docs/prerequisites/installation.md"
fi

if have ros2; then
    if timeout 8 ros2 topic list >/dev/null 2>&1; then
        _pass "the ROS 2 CLI responds ('ros2 topic list' succeeded)"
    else
        _warn "'ros2 topic list' did not respond within 8 seconds" \
            "the ROS 2 daemon may need a moment on first use -- try 'ros2 daemon stop' then run this again"
    fi
fi

# ---------------------------------------------------------------------------
# 3. Python
# ---------------------------------------------------------------------------

section "Python"

if have python3; then
    PY_VERSION="$(python3 --version 2>&1)"
    _pass "python3 available (${PY_VERSION})"
else
    _fail "python3 not found" "install python3 via your package manager"
fi

# ---------------------------------------------------------------------------
# 4. Workspace
# ---------------------------------------------------------------------------

section "Workspace"

WORKSPACE_CANDIDATES=("$HOME/course_ws" "$HOME/robot_ws" "$HOME/ros2_ws")
FOUND_WS=""
for ws in "${WORKSPACE_CANDIDATES[@]}"; do
    if [ -d "$ws/install" ]; then
        FOUND_WS="$ws"
        break
    fi
done

if [ -n "$FOUND_WS" ]; then
    _pass "a built workspace was found at ${FOUND_WS} (has an install/ directory)"
    if [ -f "$FOUND_WS/install/setup.bash" ]; then
        _pass "setup.bash exists in that workspace"
    else
        _warn "no install/setup.bash in ${FOUND_WS}" "run 'colcon build' in that workspace"
    fi
else
    _warn "no built workspace found at ~/course_ws, ~/robot_ws or ~/ros2_ws" \
        "create one: mkdir -p ~/course_ws/src && cd ~/course_ws && colcon build"
fi

# ---------------------------------------------------------------------------
# 5. RViz
# ---------------------------------------------------------------------------

section "RViz"

if have rviz2; then
    _pass "'rviz2' is available"
else
    _fail "'rviz2' not found" \
        "install the desktop variant: sudo apt install ros-\$ROS_DISTRO-desktop"
fi

# ---------------------------------------------------------------------------
# 6. Simulation (Webots), if this looks like a simulation-track machine
# ---------------------------------------------------------------------------

section "Simulation"

if have webots; then
    _pass "'webots' is available on PATH"
elif [ -d "/usr/local/webots" ] || [ -d "/opt/webots" ]; then
    _pass "a Webots installation directory was found"
else
    _warn "Webots was not found" \
        "only relevant if your session uses simulation -- see docs/platforms/simulation.md"
fi

if have ros2 && timeout 5 ros2 pkg prefix webots_ros2 >/dev/null 2>&1; then
    _pass "the 'webots_ros2' ROS 2 package is installed"
else
    _warn "the 'webots_ros2' ROS 2 package was not found (or the CLI timed out)" \
        "only relevant if your session uses simulation -- sudo apt install ros-\$ROS_DISTRO-webots-ros2"
fi

# ---------------------------------------------------------------------------
# 7. ROS_DOMAIN_ID
# ---------------------------------------------------------------------------

section "Network configuration"

if [ -n "${ROS_DOMAIN_ID:-}" ]; then
    _pass "ROS_DOMAIN_ID is set to '${ROS_DOMAIN_ID}'"
else
    _warn "ROS_DOMAIN_ID is not set (defaults to 0)" \
        "fine for a single machine; ask your team for the shared ID before connecting to a real robot"
fi

if [ "${ROS_LOCALHOST_ONLY:-0}" = "1" ]; then
    _warn "ROS_LOCALHOST_ONLY=1 is set" \
        "this machine will not see any other machine on the network -- expected for solo simulation, wrong if you plan to reach a robot tonight"
fi

# ---------------------------------------------------------------------------
# 8. Basic network resolution (no private targets are ever queried)
# ---------------------------------------------------------------------------

section "Basic network resolution"

# Only a well-known PUBLIC hostname is resolved, and only resolved -- never
# connected to. This deliberately never queries anything on a private network
# or anything internal to the course infrastructure.
if have getent && getent hosts docs.ros.org >/dev/null 2>&1; then
    _pass "DNS resolution works (resolved docs.ros.org)"
elif have host && host docs.ros.org >/dev/null 2>&1; then
    _pass "DNS resolution works (resolved docs.ros.org)"
else
    _warn "could not resolve a public hostname" \
        "fine if you are offline on purpose; needed for pip/apt installs and this course's linked documentation"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo
echo "=================================================="
echo " Summary: ${PASS} pass, ${WARN} warning(s), ${FAIL} fail(s)"
echo "=================================================="

if [ "$FAIL" -gt 0 ]; then
    echo
    echo "Resolve every FAIL above before the session -- each one names the"
    echo "exact next step. See docs/prerequisites/installation.md for the"
    echo "full installation guide."
    exit 1
fi

if [ "$WARN" -gt 0 ]; then
    echo
    echo "No FAILs. The WARNINGs above may or may not matter for tonight's"
    echo "specific session -- check against that session's 'Preparation'"
    echo "section."
fi

exit 0
