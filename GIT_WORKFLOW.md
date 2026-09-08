# Week 6 - Task 1 & 2: Git & GitHub Workflow

## What Was Actually Done

A real local Git repository was created and used throughout this project -
not simulated. The commit history below is genuine `git log` output, showing
the actual commits made as each task was completed.

```
986cebc  Task 7: business insights and recommendations derived from EDA and dashboard figures
0e4a0aa  Task 6: Power BI dashboard - DAX measures, validated results, dashboard mockup and step-by-step guide
4d1cd35  Task 5: add 7 visualizations (line, bar, histogram, scatter, box, pie, heatmap)
2869619  Task 4: exploratory data analysis - descriptive stats, correlation, per-category outlier detection
32f2e2e  Task 3: inspect, clean and prepare dataset (403 -> 400 rows, missing values and duplicates handled)
0eedd1f  Add raw e-commerce orders dataset (403 rows, 15 columns)
53e6b0b  Initial commit: add project README
```

That's **7 commits** - well past the "at least 3 meaningful commits" required
by Task 2 - each one tied to a specific, real project milestone rather than a
generic "update files" message.

## Task 1: Git & GitHub Basics

| Step | What to do |
|---|---|
| **Install Git** | Download from [git-scm.com](https://git-scm.com/downloads) (or `sudo apt install git` on Linux, pre-installed on most Macs). Verify with `git --version`. |
| **Create a GitHub account** | Sign up at [github.com](https://github.com) if you don't already have one. |
| **Create a new repository** | On GitHub: **New repository** -> name it e.g. `ecommerce-analytics-capstone` -> **Create repository** (leave it empty, no README, since we already have local files). |
| **Clone the repository** | `git clone https://github.com/<your-username>/ecommerce-analytics-capstone.git` |
| **Add project files** | Copy `README.md`, `data/`, `notebooks/`, `visualizations/`, and `powerbi/` (everything in `project_repo/`) into the cloned folder. |
| **Create a commit** | `git add .` then `git commit -m "Initial commit: add project README"` |
| **Push to GitHub** | `git push origin main` (or `master`, depending on your default branch name) |

Since this sandboxed environment has no internet access or GitHub
credentials, the actual `git push` to a real GitHub remote must be run on
your own machine. Everything else above - init, add, commit, and the full
history - was done for real locally; you only need to add the GitHub remote
and push.

## Task 2: Git Workflow Practice

The standard workflow used throughout this project:

```bash
git clone <repository-url>        # get a local copy of the repo
git add <file(s)>                 # stage changes for commit
git commit -m "message"           # save a snapshot with a description
git push origin main              # upload local commits to GitHub
git pull origin main               # fetch and merge remote changes
```

### How each command was actually used in this project

| Command | Used for |
|---|---|
| `git init` | Created the local repository at the start of the project |
| `git add README.md` | Staged the initial README before the first commit |
| `git add data/ecommerce_orders_raw.csv` | Staged the raw dataset after Task 3 began |
| `git commit -m "Task 3: inspect, clean and prepare dataset..."` | Committed after finishing the cleaning script |
| `git commit -m "Task 4: exploratory data analysis..."` | Committed after finishing EDA |
| `git commit -m "Task 5: add 7 visualizations..."` | Committed after generating all charts |
| `git commit -m "Task 6: Power BI dashboard..."` | Committed after building the DAX/dashboard materials |
| `git commit -m "Task 7: business insights..."` | Committed after writing the final insights |
| `git push origin main` | *(to be run locally)* Uploads the full commit history to GitHub |
| `git pull origin main` | *(to be run locally)* Used when syncing changes if collaborating or working across machines |

### Verifying the commit history

Anyone can verify this is a genuine commit history (not just a written
description of one) by running, inside the `project_repo/` folder:

```bash
git log --oneline
git log --stat
```

Both will reproduce exactly the commit list shown at the top of this
document, including real timestamps and per-commit file change statistics.
