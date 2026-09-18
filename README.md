# Identification of Regular Languages

This repository contains the application developed for the report [“Identification of Regular Languages with Computable Scientists”](./Report.pdf).

The application learns a regular language over the binary alphabet `{0, 1}` from labeled examples. You provide words that should be accepted or rejected, and the program searches through deterministic finite automata (DFAs) until it finds the next minimal DFA consistent with all the evidence.

The project is an implementation of a computable scientist from learning theory. It is also a visual tool for seeing how a DFA hypothesis changes as more information is provided.

## Features

- Learns from positive and negative examples
- Supports the empty word, entered as `eps`
- Enumerates initially connected DFAs in increasing state count
- Keeps the current conjecture while it remains consistent with the evidence
- Filters out non-minimal DFAs
- Renders each conjecture as a PNG using Graphviz
- Displays the current DFA and previous conjectures in a Tkinter GUI
- Loads and exports evidence files
- Uses multiprocessing when a new DFA search is required

## Performance improvements

Recent revisions make the search more than 8× faster on representative examples. The main improvements are:

- storing accepting and rejecting state sets as bitmaps;
- searching independent flag layouts in parallel;
- keeping a rolling queue of worker tasks so finished workers receive new work immediately;
- preserving enumeration order while selecting the first valid conjecture; and
- stopping surplus worker processes once the required conjecture is found.

## Requirements

The application requires:

- Python 3
- Tkinter
- Pillow
- the Python `graphviz` package
- the Graphviz command line tools

On macOS, install Graphviz with Homebrew:

```sh
brew install graphviz
```

On Debian or Ubuntu:

```sh
sudo apt install graphviz python3-tk
```

Create a virtual environment and install the Python packages:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Tkinter is included with many Python installations. On some Linux distributions it must be installed separately, as shown above.

## Running the application

Run the GUI from the repository root:

```sh
python gui.py
```

The application starts with an empty evidence set and an initial DFA. Use the two input fields to add words that should be accepted or rejected. Words may contain only `0` and `1`; enter `eps` for the empty word.

The interface also allows you to:

- move through the conjecture images with `<` and `>`;
- change the font size and image scale;
- load an evidence file;
- export the current session; and
- reset the scientist and start a new session.

The GUI writes generated files to `current_session/`. This directory contains the evidence file and the rendered conjecture images. Starting or resetting the application recreates this directory.

## Evidence files

Evidence files contain one example per line:

```text
1 010
0 11
1 eps
```

The first value is `1` for an accepted word and `0` for a rejected word. The second value is the binary word, or `eps` for the empty word.

The repository includes saved sessions with conjecture images and evidence files, including:

- [`even0and1_more_clues`](./even0and1_more_clues/), an example involving words with even numbers of `0`s and `1`s;
- [`even0and1_more_guesses`](./even0and1_more_guesses/), a shorter related session;
- [`at_least_6_0s`](./at_least_6_0s/), an example that requires a larger search; and
- [`0%1`](./0%1/), [`%1_`](./%1_/), [`%0max(1)0%`](./%0max(1)0%), and [`%00%or%11%`](./%00%or%11%/), additional saved experiments.

## How it works

The scientist considers DFAs over `{0, 1}` with initial state `0`. It uses Rogério Reis's enumeration of initially connected transition structures, which assigns states in first-discovery order and avoids equivalent state-name permutations.

For each candidate transition structure, the observed words determine whether their final states must be accepting or rejecting. Candidates that conflict with the evidence are discarded. The remaining candidate is checked for minimality with the DFA distinguishability table-filling algorithm.

When new evidence is consistent with the current conjecture, the conjecture is kept. When it is contradicted, the search continues forward through the enumeration until it finds the next consistent minimal DFA.

The main implementation is split across:

- [`dfa.py`](./dfa.py), which represents DFAs, enumerates transition tables, checks minimality, and renders graphs;
- [`scientist.py`](./scientist.py), which stores evidence, updates accepting states, searches for new conjectures, and tracks progress; and
- [`gui.py`](./gui.py), which provides the Tkinter interface.

## Limitations

The search is exhaustive, so its running time grows quickly as the required number of states increases. Larger examples can take minutes or longer, and the GUI may appear unresponsive while a search is running.

The current implementation is specialized to binary words and does not provide a command line interface or a library API. The multiprocessing search improves the way candidate layouts are evaluated, but it does not remove the cost of exhaustive enumeration.

## Report

The accompanying report explains the DFA definitions, minimality algorithm, Reis enumeration, scientist behavior, implementation, and performance considerations:

[`Report.pdf`](./Report.pdf)
