# G1-D Chess

Autonomous chess-playing pipeline for the Unitree G1-D humanoid robot.

## Goal

Build a system where the G1-D can:

1. See a chessboard
2. Identify board state and pieces
3. Choose a move using a chess engine
4. Plan a safe pick-and-place motion
5. Execute the move with verification and recovery

## Current Status

- Basic Python project structure
- Placeholder board detection
- python-chess integration
- Optional Stockfish support
- Board-square to XY coordinate mapping
- Dry-run robot motion planner
- Safety checker for workspace limits
- Camera and robot configuration files

## Pipeline

camera/depth -> board detection -> chess engine -> board coordinates -> motion planner -> safety checker -> robot controller

## Setup

python3 -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt

## Run

python src/main.py

## Test Stockfish / fallback move

python scripts/test_stockfish.py

## Safety

Real robot execution is disabled by default. The system starts in dry-run mode.
