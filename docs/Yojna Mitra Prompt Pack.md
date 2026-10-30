# TRIVON Prompt Pack

## Setup: how to use this pack

Paste the master prompt once, attach the problem statement, then run the phase prompts in order. Every phase ends with a Decision Record that you save as a file, so every chat starts from the same facts.

**Your four chats**

| Chat | Job | Roadmap phases | Tool |
| --- | --- | --- | --- |
| 1. Solution | Understand the problem, freeze the solution, decide how it works | 1-3 | ChatGPT and Claude, cross-checking each other |
| 2. Delegation | Master brief, one brief per person, Antigravity rules | 4 | Either |
| 3. Build support | Checkpoint reviews, cutting scope, getting unstuck | 5-6 | Either; Antigravity writes the code |
| 4. Test and submit | Evidence, deck, demo script, Judge Q&A, final check | 6-7 | Either |

**Project setup (do before 2:00 PM)**

- [ ] Create one Project in ChatGPT and one in Claude with the same name; the two tools cannot read each other's chats
- [ ] Paste the Master Prompt (next section) into each Project's instructions
- [ ] Upload the TRIVON Hackathon Roadmap, and later the event rules, judging criteria and problem statement
- [ ] Create the four chats above inside each Project
- [ ] Create a file called decisions.md in the Project files and in your GitHub repo's docs folder

**The Decision Record habit**

At the end of each phase, the AI prints a Decision Record in a fixed format. Copy it into decisions.md, replace the old file in both Projects, and say "frozen" in the chat. Do not rely on one chat remembering another; rely on the file.

**ChatGPT plus Claude**

Use one tool as the driver and the other as the challenger. Run each phase prompt in the driver, then paste its Decision Record into the challenger with the Challenge Prompt from Chat 1. Time box the challenge to 10 minutes, then the lead decides.

**Antigravity**

Antigravity only writes code. It receives the master brief, the person's brief and the rules from Chat 2, never open-ended planning questions.

**How to run any prompt**

1. Open the right chat and paste the prompt.
2. Answer its questions briefly; if you do not know, say "unknown" and let it propose options.
3. Challenge anything that sounds vague or unproven.
4. When all three of you agree, say "frozen" and save the Decision Record.

## Master prompt (Project instructions)

Paste this once into the instructions of your ChatGPT Project and your Claude Project, and attach the problem statement and event rules. It applies to every chat inside the Project.

```text
ROLE
You are the TRIVON hackathon mentor and decision facilitator. Think like an experienced hackathon winner and a pragmatic senior engineer. You help three people decide, freeze and plan quickly. You do not write product code unless I ask.

TEAM AND EVENT
- Team TRIVON: Ankush Poonia (team lead, agentic AI, integration), Anamika (ML, basic level), Aditya (UI/UX, frontend, presentation). All three have some agentic AI experience.
- Event: 24-hour hackathon, 30 Oct 2:00 PM to 31 Oct 2:00 PM IST. Track: AI/ML only. Our internal submission deadline is 1:00 PM on 31 Oct.
- Discussion happens here. All coding happens in Antigravity.
- Goal: a hackathon-winning, demo-ready product, not a production system.
- The problem statement, event rules and judging criteria are attached to this Project and are the source of truth. If something is missing, say so instead of guessing.

OPERATING RULES
1. Problem first, solution second, tools last.
2. Prefer the simplest method that works. Do not suggest an LLM, multi-agent setup, vector database or custom-trained model unless the need is stated and simpler options are ruled out.
3. Everything you propose must be buildable by three people in the time left. State a rough build time for each feature.
4. Never invent facts, statistics, citations, benchmarks or user quotes. If a fact is missing, label it ASSUMPTION or NEEDS VERIFICATION and say how we can check it quickly.
5. Label every number MEASURED, ESTIMATED or TARGET.
6. Tie each decision to the judging criteria whenever they are known.
7. Priorities: P0 must work, P1 should work, P2 is optional. Keep P0 small.
8. Ask at most 5 questions at a time, most important first. If I answer "unknown", give 2-3 options and a recommendation with the reason.
9. Be direct. Challenge weak ideas, vague wording and scope creep, including mine. Say when something is a bad idea and why.
10. Keep answers short and scannable: tables and checklists, no filler, no praise.
11. Respect time. If I tell you the time left, adjust. If the discussion drifts, say so and propose the decision.
12. Do not move to the next phase until I say "frozen".

DECISION RECORD
At the end of each phase, print a Decision Record in exactly this format and nothing after it:
DECISION RECORD - [phase] - [time]
FROZEN: [numbered decisions, one line each]
OPEN: [unresolved items and owner]
ASSUMPTIONS: [list]
NEXT: [next phase and its first action]

CHALLENGE MODE
If I paste another AI's output and write "challenge", act as a skeptical judge. List the 5 biggest weaknesses, every claim without evidence, scope and time risks, and what you would change. Be specific and brief.

When you have read this, reply only: "TRIVON mentor ready. Send the first phase prompt."
```

**Start line for every new chat**

Paste this as the first message of any chat so it picks up the saved decisions:

```text
Read decisions.md and the attached problem statement. Summarize in 5 lines what is frozen, what is open, and what we do next. Do not add anything new.
```

## Chat 1: Solution discussion (roadmap phases 1-3)

Run these in order, in one chat, from 2:00 PM to about 5:30 PM. Replace anything in \[brackets\]. To close a phase, send: "Frozen. Print the Decision Record." Then save it to decisions.md.

### 1.1 Event Brief and go/no-go (2:00 PM, 30 minutes)

**Attach:** problem statement(s), event rules, judging criteria.

```text
PHASE 1.1 - EVENT BRIEF AND GO/NO-GO
Time left before build starts: [e.g. 4 hours]. Read the attached problem statement(s), rules and judging criteria.

TASK
1. Fill an Event Brief table: theme and constraints; judging criteria with weights; submission requirements (repo, deck, video, hosted link); presentation length; allowed tools (including AI coding tools), pre-built components, open-source code and datasets; deadline and when judging happens. Write NOT STATED for anything the material does not say.
2. List what we must confirm with the organizers, ranked by risk, maximum 6 items.
3. For each problem statement we are considering, score 1-5 with a one-line reason: fit with the AI/ML track; fit with our three skill areas; buildable in about 12 hours of build time; easy to show in a short demo; clear path to the judging criteria.
4. Recommend GO, NO-GO or GO WITH CONDITIONS and name the single biggest risk.

RULES: use only the attached material. Do not propose solutions yet.
OUTPUT: Event Brief table, questions list, fit table, recommendation. Then wait for me.
```

### 1.2 Problem and user (2:30 PM, 60 minutes)

```text
PHASE 1.2 - PROBLEM AND USER
Problem statement chosen: [paste name or number]. Time box: 60 minutes.

First ask me up to 5 questions you need answered, then wait. After my answers produce:
1. The problem in one sentence: [specific user] struggles to [task] because [root cause], leading to [consequence].
2. Symptom versus root cause: a five-whys chain, ending at a cause our product could change.
3. One specific user persona: role, goal, current workflow step by step, main pain point, constraints, and what would stop them adopting a new tool.
4. The single most painful friction point we should target, and why not the others.
5. Existing alternatives (including spreadsheets, chat groups, a person doing it, and doing nothing), and the gap each leaves.
6. Evidence plan: the 3 facts about scale or cost that would most strengthen our pitch, and how to check each in 20 minutes. If you can browse, give sources with date; if not, mark them NEEDS VERIFICATION. Never invent numbers.
7. Three questions to ask real people at the venue about the last time this problem happened.
8. Success criteria: what must be true for a judge to call this a good solution.

RULES: mark every claim as FACT (with source), ASSUMPTION or NEEDS VERIFICATION.
OUTPUT: items 1-8 as short sections. Then wait.
```

### 2.1 Solution options and USP (3:30 PM, 30 minutes)

```text
PHASE 2.1 - SOLUTION AND USP
Use the frozen problem and user from decisions.md. Time box: 30 minutes.

TASK
1. Propose 3 genuinely different solution options. For each: one-sentence idea, how the user benefits, core AI/ML approach in plain words, main risk, rough build time for a 3-person team.
2. Compare them in a table scored 1-5 on: user value, fit with the judging criteria, feasibility in our time, demo clarity, risk of failure, differentiation from existing alternatives.
3. Recommend one option and say why, including what we give up.
4. Give 3 candidate USPs for the recommended option. Each must say who benefits, what gets easier, why it differs from the alternatives, and how the demo will show it. Reject vague claims such as "AI-powered".
5. Write the value proposition: For [user] who needs to [job], our product [benefit] by [how it works], unlike [current alternative].
6. List 5 things we will NOT build.
7. Describe the core user journey in 3-6 steps.

RULES: no solution may need data or access we do not have; flag any that do.
OUTPUT: options, comparison table, recommendation, USPs, value proposition, non-goals, journey. Then wait.
```

### 2.2 Features, priorities and demo (4:00 PM, 30 minutes)

```text
PHASE 2.2 - FEATURES, METRIC AND DEMO
Use the frozen solution and USP from decisions.md. Time box: 30 minutes.

TASK
1. List candidate features, maximum 12, each with: purpose, user benefit, rough build time, owner by role (Ankush: AI/agent and integration; Anamika: ML; Aditya: UI and deck).
2. Score each feature 1-5 on: user value, judging-criteria importance, feasibility, demo clarity, risk of failure, outside dependencies.
3. Assign P0, P1, P2. P0 means the core solution does not work without it; keep P0 to 3-5 features that work end to end. Mark which features are demo-critical.
4. For each P0, write one line saying exactly how we verify it works.
5. Propose the primary metric, how to measure the baseline (the current way of doing the task) against our prototype under the same conditions, and a target clearly labeled TARGET.
6. Write 5 test cases: typical, edge, ambiguous, invalid or missing input, and failure of an outside service.
7. Write the demo scenario: one user, one story, one outcome, under 3 minutes.
8. Check that the demo shows the USP within the first minute.
9. Propose the feature-freeze time (suggest 6:00 AM) and checkpoints (9 PM, midnight, 3 AM, 6 AM).

RULES: cut anything that does not help the judging criteria or the demo. Flag every P0 that depends on something we have not confirmed.
OUTPUT: feature table, P0/P1/P2 list, metric, test cases, demo scenario, freeze plan. Then wait.
```

### 2.3 Challenge prompt (use in the other AI)

**When:** after each Decision Record, in the AI you did not use as the driver. Paste the record below the prompt. Time box: 10 minutes.

```text
challenge
Act as a skeptical hackathon judge using the attached judging criteria. Read the Decision Record below.
1. Score each judging criterion 1-10 and name the one change that would raise it most.
2. List the 5 biggest weaknesses, most serious first.
3. List every claim with no evidence behind it.
4. List scope or time risks for a 3-person team with about 12 hours of build time.
5. Name one thing that is likely a waste of time and one thing that is missing.
6. Give your recommended changes in order of importance, maximum 5.
Be specific and brief. Do not rewrite the whole plan.

[PASTE DECISION RECORD]
```

Bring the answers back to the driver chat as: "The challenger said: \[paste\]. Accept, reject or modify each point with a reason."

### 3.1 User flow and feature logic (4:30 PM, 25 minutes)

```text
PHASE 3.1 - FLOW AND LOGIC
Use the frozen P0 features and demo scenario from decisions.md. Time box: 25 minutes.

TASK
1. Write the user flow as numbered steps: what the user does, what the system does, what the user sees. Note every place a failure can happen.
2. For each P0 feature fill a table: input, processing, output, method, why this is the simplest method that works, what happens if it fails or is wrong.
3. Method choices: plain logic, an existing model or API, an LLM, a trained ML model, or a combination. Explain why not the simpler option above it. Do not use an LLM only because this is the AI/ML track.
4. Say honestly what part of ML or AI is genuinely needed, who builds it, and a safe fallback if it does not work in time.
5. Decide how the product shows its evidence or reasoning to the user, and how we handle uncertainty and errors.
6. List the data needed (demo data, test data, sources) and confirm nothing private or restricted is used.
7. List the main screens the interface needs, based on the flow.

RULES: keep every method buildable in the time; mark any risky step RISK with a mitigation.
OUTPUT: flow, feature logic table, method and fallback notes, data list, screen list. Then wait.
```

### 3.2 Tech stack and architecture (4:55 PM, 20 minutes)

```text
PHASE 3.2 - STACK AND ARCHITECTURE
Technologies our team already knows well: [list languages, frameworks, tools]. Tools or accounts already set up: [list]. Time box: 20 minutes.

TASK
1. Propose the stack for frontend, backend, AI/ML, database, outside APIs and deployment. For each: the choice, the reason, one alternative, setup time, cost or usage limits, and a fallback. Prefer what we already know over anything new.
2. Say whether a database is needed at all; if not, say so.
3. Check free-tier limits, cold starts and rate limits that could hurt the demo.
4. Describe the architecture as a numbered list of components with: its job, what it receives, what it returns, and who owns it. Add a simple text diagram showing how the components connect.
5. Name the three most likely failure points and a mitigation for each.

RULES: no new technology unless it clearly saves time; no component without a P0 feature that needs it.
OUTPUT: stack table, database decision, limits check, architecture list and diagram, failure points. Then wait.
```

### 3.3 API contract and folder structure (5:15 PM, 15 minutes)

```text
PHASE 3.3 - API CONTRACT AND STRUCTURE
Use the frozen flow, logic, stack and architecture from decisions.md. Time box: 15 minutes.

TASK
1. API contract table: endpoint, method, input fields, output fields, error cases, owner.
2. A sample success response and a sample error response for each endpoint, so the frontend can start on mock data now.
3. Shared data formats the components must agree on.
4. A folder structure with one line per folder or key file saying what it holds, and which person owns it.
5. Environment variable names (names only, no values) and the run commands described in words.
6. Rules for mock data versus real data, and how we switch.

RULES: keep the contract as small as possible; every field must be used by a P0 feature or the interface.
OUTPUT: contract table, sample responses, shared formats, folder tree, env names, mock rule. Then wait.
```

## Chat 2: Delegation and Antigravity setup (roadmap phase 4, 5:30-6:15 PM)

Start this chat with the start line from the setup section, and attach decisions.md with every frozen Decision Record. Send the first three prompts to the AI, then give the outputs to the team.

### 4.1 Master brief

```text
PHASE 4.1 - MASTER BRIEF
Compile every frozen Decision Record in decisions.md into one Master Brief. Maximum 3 pages. Do not add new decisions; if something is missing, list it under OPEN.

SECTIONS
1. Problem, user and evidence (with labels FACT / ASSUMPTION / NEEDS VERIFICATION)
2. Solution, USP and value proposition
3. Scope: P0, P1, P2 features, and the explicit non-goals
4. User flow and demo scenario
5. Feature logic: input, processing, output, method for each P0
6. Tech stack and architecture, with the component list
7. API contract and sample responses
8. Folder structure and ownership
9. Metric, baseline, test cases
10. Checkpoints and freeze time (9 PM mock slice, midnight real end-to-end, 3 AM P0 basic, 6 AM freeze)
11. Known risks and fallbacks
12. Glossary of the names we use for components and data, so everyone and every AI uses the same words

RULES: plain language, tables where possible, no repetition.
OUTPUT: the Master Brief only.
```

### 4.2 Personal briefs

```text
PHASE 4.2 - PERSONAL BRIEFS
Using the Master Brief, write one brief each for Ankush (team lead, AI and agent core, integration), Anamika (ML) and Aditya (UI/UX, frontend, deck). Each brief maximum 1 page.

EACH BRIEF HAS
- Objective in one sentence
- What I receive (inputs, files, mock data, contract sections)
- What I must deliver, with a 9 PM deliverable, a midnight deliverable and a 6 AM deliverable
- Files and folders I own, and files I must not touch
- Dependencies on the other two people, and how I work without waiting (mocks)
- Acceptance criteria: how I know each deliverable is done
- How I test my part alone
- Out of scope: what I must not build
- If I get stuck: the 30-minute rule and who to ask first

RULES: no brief may need information that is not in the Master Brief. Make each deliverable specific enough to be checked yes or no.
OUTPUT: three briefs, clearly separated.
```

### 4.3 Antigravity rules

Save the text below in the rules or instructions file your Antigravity workspace uses, once per laptop. It keeps the coding agent on task.

```text
PROJECT RULES FOR THE CODING AGENT
1. Before any work, read the Master Brief and the personal brief for this person. Treat them as the source of truth. If they conflict with a request, stop and ask.
2. Build only the tasks in this person's brief. Edit only the files and folders this person owns. Never rewrite another person's files.
3. Follow the API contract exactly: same endpoint names, field names and error format. If you think the contract must change, stop and say so; do not change it yourself.
4. Prefer the simplest implementation that works. No new libraries, services or architecture without asking and giving a reason.
5. Start with a short plan listing the files you will create or change. Wait for approval on anything larger than one feature.
6. Work in small steps. After each step, tell me how to run it and what I should see, in plain words.
7. Use mock data until real components exist. Keep mock and real data behind one switch.
8. Never put keys, tokens or private data in code. Use environment variables listed in .env.example.
9. Handle errors and empty inputs with clear messages for the user.
10. Keep the code readable with short comments where the logic is not obvious. Keep the README run steps up to date.
11. If a fix fails 3 times, stop. Summarize the error, what you tried and your best next idea, and wait for me.
12. Never claim something works without running it. Say clearly what you did not test.
```

### 4.4 Repo scaffold (Ankush, in Antigravity)

**Attach:** Master Brief, section 8 (folder structure) and section 7 (API contract).

```text
REPO SCAFFOLD
Read the attached Master Brief. Create only the folder structure and placeholder files described in section 8, plus README.md, .gitignore (covering .env and dependency folders) and .env.example listing the variable names from the brief with empty values.

RULES
- No feature code. Placeholder files contain only a one-line comment saying their purpose and owner.
- Add the sample API responses from section 7 as mock data files in the shared folder.
- The README must explain in plain steps how to install and run each part, which branch each person uses, and the rule that main always runs.
- Do not install anything beyond what the stack in section 6 names.

When done, list every file created and how to start the base project, then stop.
```

### 4.5 Kickoff prompt for each person (in Antigravity)

Each person pastes the general prompt first, with their own role block under it. Replace anything in \[brackets\].

```text
KICKOFF
I am [Ankush / Anamika / Aditya]. Read the Master Brief and my personal brief in the docs folder, and the project rules. Then reply with:
1. My objective in your own words.
2. The files and folders I own.
3. Your step-by-step plan for my 9 PM deliverable, with the files for each step.
4. Anything in the briefs that is unclear or conflicts with the contract.
Do not write code until I approve the plan.
```

**Ankush (AI and agent core)**

```text
ROLE BLOCK - AI CORE
Build the AI/agent workflow described in section 5 of the Master Brief behind the API contract. Start with a version that returns the sample responses from the mock files, then replace the mock with the real logic one step at a time. Show the evidence or reasoning in the output as the brief requires. Add a safe fallback for when the model or outside service fails. Keep prompts and settings in one place so they are easy to change.
```

**Anamika (ML)**

```text
ROLE BLOCK - ML
Build the ML component described in section 5 of the Master Brief with the exact input and output format in the contract. Start with the simplest working baseline, then improve only if time allows. Build a small evaluation script that runs the 5 test cases and the metric from section 9 and prints the results clearly. Record the baseline result first. Never present a guess as a measured result.
```

**Aditya (UI and presentation)**

```text
ROLE BLOCK - INTERFACE
Build the interface for the screens in the Master Brief using only the mock API responses first. Cover loading, empty, error and success states. Make the main demo flow work in three clicks or fewer. Keep the design clean and readable on a projector. When the real API is ready, switch from mock to real through one setting, without changing the screens.
```

## Chat 3: Build support (roadmap phases 5-6, 6:15 PM-9:00 AM)

This chat is for decisions about the build, never for writing the code. Start with the start line and attach decisions.md plus a screenshot or text copy of the Feature Board. Antigravity writes the code.

### 5.1 Checkpoint review (9 PM, midnight, 3 AM, 6 AM, 9 AM)

```text
BUILD CHECKPOINT
Time now: [time]. Next checkpoint: [time]. Scheduled freeze: 6:00 AM.

STATUS (from the Feature Board)
- Ankush: [done / in progress / blocked / at risk, one line each]
- Anamika: [same]
- Aditya: [same]
- Real versus mocked right now: [what runs for real, what is still mock]
- Remaining sleep rota: [who sleeps when]

TASK
1. Judge honestly whether we can reach the next checkpoint with every P0 working. Say ON TRACK, AT RISK or OFF TRACK and give the reason.
2. If AT RISK or OFF TRACK, list what to cut in this order: P2, P1, polish, optional slides. Never cut integration, testing, rehearsal or the submission buffer.
3. Name the single most important thing each person does in the next 3 hours.
4. Name any integration risk between components, and who fixes it.
5. Say what we must not start now.

RULES: base everything on the status I gave; if something is missing, ask me instead of guessing. No new features.
OUTPUT: status line, cut list (if any), next-3-hours plan per person, risks, do-not-start list.
```

### 5.2 We are behind: cut scope

```text
CUT SCOPE
We are behind. Time now: [time]. Hours left until the 6:00 AM freeze: [hours]. Unfinished features and their remaining build estimates: [list].

TASK
1. For each unfinished feature, recommend KEEP, SIMPLIFY or CUT and give one line of reasoning based on the judging criteria and the demo.
2. For each SIMPLIFY, describe the smallest version that still shows the value and is honest about its limits.
3. Show what the demo looks like after the cuts, and what we say about the cut items (planned work, never presented as built).
4. Give the new plan for the next 3 hours, with an owner for each item.

RULES: protect the P0 path, the demo scenario and the time for testing and rehearsal. Be blunt; do not soften cuts.
```

### 5.3 Loop breaker (stuck for 30 minutes or more)

```text
LOOP BREAKER
We have been stuck for [minutes] minutes. Problem: [one sentence]. What we tried: [list]. Error or behavior we see: [paste]. Feature priority: [P0 / P1 / P2]. Time left to the next checkpoint: [time].

TASK
1. Say in two sentences what you think is really going on. Separate what is known from what you are guessing.
2. Give 3 options: (a) a specific next step to try, with a time box; (b) a different approach; (c) cut or replace the feature. Include a time cost for each.
3. Recommend one and say what we do if it fails.
4. Name one check that would confirm or rule out your diagnosis in under 5 minutes.

RULES: do not repeat anything we already tried; do not suggest new technology unless it removes the problem; be short.
```

### 5.4 Integration help

```text
INTEGRATION CHECK
Two parts do not work together: [e.g. frontend and backend]. Contract section: [paste the endpoint]. What the sender produces: [paste actual output]. What the receiver expects or the error it shows: [paste].

TASK
1. Compare the actual output with the contract field by field and list every mismatch.
2. Say which side should change, based on the contract being the source of truth, and why.
3. Give a short, exact message I can send to the person who owns that side.
4. Say whether the contract itself needs an update, and if so write the new version for all three of us to approve.
```

### 5.5 Bug report for Antigravity

Paste this to the coding agent when something breaks. Fill in every line.

```text
BUG REPORT
What I did: [steps]
What I expected: [result]
What happened: [result or exact error, pasted in full]
Files I think are involved: [names, or "unknown"]
What I already tried: [list]

First explain the most likely cause in plain words. Then propose the smallest fix that touches only the files I own. Do not refactor or add features. After the fix, tell me exactly how to check that it works, and what else it might have affected.
```

### 5.6 Pre-merge review (before anything goes to main)

```text
PRE-MERGE REVIEW
Review this change before it goes to main. Check only:
1. Does it follow the API contract exactly?
2. Does it touch files outside the owner's area?
3. Are there keys, tokens or private data in the code or in logs?
4. Does the main workflow still run, and what is the quickest way to check?
5. Are errors and empty inputs handled with clear messages?
6. Is anything left half done or hard-coded that should not be?
Answer MERGE, FIX FIRST or DO NOT MERGE with a short list of reasons. Do not suggest improvements outside these six checks.

[PASTE DIFF OR FILE LIST]
```

### 5.7 Sleep handoff note

The person going to sleep writes this in three lines in the team chat.

```text
HANDOFF - [name] - [time]
Done and pushed: [what, branch]
In progress and where I stopped: [what, file]
Next thing to do or watch: [one line]
```

## Chat 4: Test, evidence, deck and submission (roadmap phases 6-7, 6:00 AM-1:00 PM)

Start with the start line and attach decisions.md, the Master Brief, the real test results and, when you reach 6.6, the Notion Submission Checklist and the event rules.

### 6.1 Test plan (6:00 AM)

```text
TEST PLAN
The feature freeze has started. Time now: [time]. Features marked built: [list, from the Master Brief P0/P1].

TASK
1. Create a test checklist table: test, steps, expected result, who runs it, pass/fail. Include: the main demo scenario from a clean start; the 5 test cases; empty input; invalid input; slow response; failed outside service; page refresh or restart; a small screen if it matters.
2. Order the tests by risk to the demo, most risky first.
3. Say which tests need a person who did not build the feature.
4. List the checks for safety: no keys or private data in the repo, screen or demo; the demo data is appropriate; API quota left; any sleeping service woken.
5. Define what counts as a critical bug (fix now) versus a known limitation (document it).

OUTPUT: the checklist table, the safety checks, the bug rule. Then wait for results.
```

### 6.2 Evidence and claims audit (9:00 AM)

```text
EVIDENCE AUDIT
Here are our real results: baseline method and measurements [paste], prototype measurements [paste], test case results including failures [paste]. Here are the claims currently in our deck and write-up: [paste].

TASK
1. Build a before-and-after table using only what I pasted. Label each number MEASURED, ESTIMATED or TARGET.
2. Check every claim: SUPPORTED (by what), WEAK (what is missing) or UNSUPPORTED. List unsupported claims for deletion or rewording.
3. Write a plain list of known limitations and where the AI can be wrong, in words a judge will respect.
4. Write a status table of every feature as BUILT, PARTIAL, MOCKED or PLANNED, so we never overstate what we built.

RULES: never invent or round up a number. If evidence is missing, say what quick test could produce it.
```

### 6.3 Deck outline (10:00 AM)

```text
DECK OUTLINE
Presentation length from the rules: [minutes]. Use the Master Brief, the evidence table and the feature status table.

TASK
Write a slide-by-slide outline that fits the time. Use this order: 1 problem and user; 2 evidence; 3 cost of the problem and why it matters now; 4 our solution and what is different; the live demo (with a note on where to switch); 5 before and after results; optional architecture slide; final slide with team, honest limits and next steps.

FOR EACH SLIDE give: the one message, the 3 or fewer things on the slide, the visual to use, the speaker and the speaking time, and the speaker note in two sentences.
Also give the 30-second and 60-second spoken versions of the whole pitch.

RULES: every slide must answer a judging criterion; remove anything that does not. Use only items from the evidence table. No filler slides.
```

### 6.4 Demo script and fallback (10:30 AM)

```text
DEMO SCRIPT
Demo scenario from the Master Brief. Demo time allowed: [minutes]. Demo device and network: [describe].

TASK
1. Write the demo script as steps: what the speaker says, what the speaker does on screen, what the audience should see. Start from the home screen and show the main value within the first minute.
2. Mark the exact data or input to use for every step, plus a second valid input in case the first fails.
3. List what could fail at each step and the 10-second recovery line and action.
4. Write the reset steps that return the demo to a clean start.
5. Describe the fallback (recorded demo or screenshots), only if the rules allow it, and the honest sentence to say when switching to it.
6. Write a pre-demo checklist for 30 minutes before our slot.
```

### 6.5 Judge Q&A rehearsal (11:00 AM)

```text
JUDGE PANEL REHEARSAL
Act as a panel of three judges using the attached judging criteria: a technical judge, a business and impact judge, and a user-experience judge. Our team: Ankush (AI), Anamika (ML), Aditya (UI).

PROCESS
1. Ask me one question at a time, mixing the three judges, from hard to easy. Include tough ones about: why this problem, evidence, what is real versus mocked, how the AI can be wrong, why not a simple alternative, data and privacy, cost, scaling, what we would build next, and what each of us built.
2. After my answer, score it 1-5, say what was weak, and give a better 2-sentence version. Then ask the next question.
3. Track the questions I handled badly and list them at the end with the best answer for each.

ANSWER METHOD I WILL USE: listen, clarify if needed, answer directly, give evidence, state the limit.
Start with question 1.
```

### 6.6 Final submission check (12:00 PM)

```text
SUBMISSION CHECK
Attached: event rules, submission requirements and our Submission Checklist. Time now: [time]. Internal deadline: 1:00 PM.

TASK
1. Turn the requirements into a yes/no checklist: what to submit, format, links, repository access, the form fields, file size or length limits.
2. Add the quality checks: the problem and product, technical quality, evidence and impact, pitch and demo, and submission.
3. Ask me yes or no for each item, one section at a time, and keep a running list of any "no".
4. At the end, list what is still open, ranked by risk, and say clearly SUBMIT NOW or FIX FIRST with the reason.

RULES: do not assume an item is done; ask. Do not suggest new work after the freeze unless a requirement is missing.
```

### 6.7 Submission write-up

```text
SUBMISSION WRITE-UP
Write the project description for the submission form from the Master Brief, the evidence table and the feature status table. Length limit: [words or characters].

INCLUDE: the problem and user in two sentences, what we built, how it works in plain words, what makes it different, results labeled MEASURED or TARGET, honest limits, and what comes next.

RULES: no buzzwords, no claim without evidence, no feature that is not marked BUILT or PARTIAL in the status table. Write it in plain, confident language.
```

## Tips to keep in mind

The AI speeds up your thinking, but you own the decisions and the facts. These habits keep the chats useful instead of long.

**Before 2:00 PM**

- [ ] Master prompt is pasted into both Projects and the problem statement area is ready for upload
- [ ] decisions.md exists in both Projects and in the repo docs folder
- [ ] Antigravity rules are saved on every laptop
- [ ] Everyone is logged in to both AI tools, and you have checked your plan's message limits; if one tool runs out, the other takes over as driver

**Running the chats**

- One phase prompt at a time; do not jump ahead, and say "frozen" before moving on
- Start a timer when you paste each prompt; when it ends, the lead decides
- Answer briefly; "unknown" is a valid answer and makes the AI offer options
- Always attach the files; in a new chat paste the start line first
- If a chat gets long and slow, open a fresh one in the same Project and paste the latest Decision Records

**Challenge the AI**

- Ask: "What would make this fail?" and "What is the simplest version that still wins?"
- Ask for the option you rejected and why it lost
- Ask: "What evidence do you have for that?" AI states invented numbers with confidence
- Do not accept a feature without an owner, a build time and a way to verify it
- If the AI always agrees with you, switch to the challenger tool and run the challenge prompt

**Verify yourself, never trust the AI for these**

- Statistics, sources and citations: open the source and check the date
- Rules and judging criteria: read the original text, not the AI's summary
- Free-tier limits, prices and API names: check the provider's page; they change
- Commands and library names: run them
- Every claim in the deck: it needs a measured result or a labeled estimate

**ChatGPT plus Claude**

- Do not ask both the same question and average the answers; one drives, one challenges
- When they disagree, ask each for the strongest argument for the other's view, then the lead decides in 5 minutes
- Keep the final text in decisions.md only, never scattered across chats

**Antigravity**

- Give it the briefs and the rules, never a vague idea
- Approve a plan before it writes anything large, and read the plan for files outside your area
- Commit before every big agent run so you can go back
- If it fails the same thing 3 times, stop and use the bug report prompt
- Run the app yourself after each step; never trust "it works"
- Never paste keys or private data into a prompt

**Mindset**

- You are building a clear story with one working path, not a complete product
- One thing working beats five things half done
- Honest beats impressive: label what is built, partial, mocked or planned
- Whoever presents a part should understand it, not just have received it from the AI
- Protect the last 8 hours; they are for testing, rehearsal and submission, and nothing else
