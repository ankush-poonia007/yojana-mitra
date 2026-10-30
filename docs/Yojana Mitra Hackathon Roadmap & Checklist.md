# TRIVON Hackathon Roadmap & Checklist

Oct 29, 2026 · @Ankush Poonia

## How to use this roadmap

Work top to bottom, tick each box when it is done, and do not start a phase until the checkpoint of the previous one is ticked. Every step works for any problem statement.

Three rules override everything else:

1. Problem first, tech stack last. Never pick tools before the solution is frozen.
2. Integrate early. When time runs short, cut P2 features first, never integration or rehearsal time.
3. A task that runs past its time box goes to a team decision, not to another hour of solo effort.

Event window: 30 Oct, 2:00 PM to 31 Oct, 2:00 PM. The goal is a feature-complete, integrated project by 10-11 AM, so the last 3-4 hours are a recovery buffer.

| Person | Role | Main area |
| --- | --- | --- |
| Ankush | Team lead | Agentic AI, architecture, integration, merges |
| Anamika | ML | ML approach, data, testing, evaluation |
| Aditya | UI/UX | Frontend, presentation, demo polish |

## Phase 0: Before the event (before 2:00 PM, 30 Oct)

This phase is for templates, accounts and rules, not product code. Finish it in about 90 minutes, then rest; you need to be fresh at 2:00 PM.

**Notion and templates**

- [ ] Duplicate the Notion One-Page Canvas, Event Brief row, Feature Board, Submission Checklist, Judge Q&A Bank and Retro Template for this event
- [ ] Prepare a blank judging-criteria checklist: criterion, weight, which feature or slide answers it
- [ ] Prepare blank templates for the master brief, API contract, test checklist and final demo checklist
- [ ] Skim the Free AI Tools list in Notion and note each tool's free-tier limits

**Repo and tools**

- [ ] Create the GitHub repo with README, .gitignore (covering .env) and .env.example only; add no product code unless the event rules allow starter code
- [ ] Agree branch names (one per person), the pull request rule, and who may merge to main
- [ ] Agree that main must always run
- [ ] Create accounts and API keys for the LLM, hosting and any datasets; note each limit and whether the service sleeps when idle
- [ ] Test Antigravity with a hello-world task and save the instruction template that points to the master brief and each personal brief
- [ ] Confirm every laptop can run the project tools and push to GitHub

**Team and logistics**

- [ ] Share this roadmap and agree the roles, the sleep rota and the 30-minute rule (stuck 30 minutes means ask for help)
- [ ] Pack chargers, a mobile hotspot as backup internet, headphones, water and food
- [ ] Do not pre-build an architecture, database or agent workflow; you cannot know what the problem needs

**Gate:** accounts work, repo is empty but ready, templates are duplicated, everyone has slept.

## Phase 1: Understand the event and the problem (2:00-3:30 PM)

By 3:30 PM everyone must be able to explain the rules, how the project is judged, and the problem in one minute. The Playbook allows about 2.4 hours here; this roadmap compresses it to 90 minutes because the templates are ready.

**Read the rules together (first 30 minutes)**

- [ ] Read the official rules and judging criteria aloud as a team; underline the weights
- [ ] Fill one Event Brief row: theme and constraints, criteria and weights, submission requirements, deadline, presentation length, team size, allowed tools and data, three to five fitting problem areas
- [ ] Confirm whether AI coding tools (Antigravity), pre-built components, open-source libraries and public datasets are allowed
- [ ] Confirm what must be submitted: repository, deck, video, hosted link or report
- [ ] Confirm when judging or demo slots happen; if teams present before 2 PM, move every later deadline earlier
- [ ] Set an internal submission deadline of 1:00 PM at the latest

**Pick and define the problem (next 60 minutes)**

- [ ] Go or no-go: does the problem fit the AI/ML track, our three skill areas, and the rubric? Decide in 10 minutes
- [ ] Write the problem in one sentence: \[specific user\] struggles to \[task\] because \[root cause\], leading to \[measurable consequence\]
- [ ] Separate the symptom from the root cause; ask why it happens
- [ ] Define one specific user: role, goal, current workflow, main pain point, constraints, what stops them adopting a new tool
- [ ] Pick one painful friction point, not every problem in the workflow
- [ ] Find scale evidence in 20 minutes and record source, date, population and what the number measures; do not treat a headline as proof
- [ ] List existing alternatives, including spreadsheets, chat groups, a human doing it, and doing nothing
- [ ] Write the success criteria and the first idea of the primary metric
- [ ] Ask two or three people at the venue about their real behavior: "Tell me about the last time this happened"

**Gate:** all three can explain the rules and the judging, then describe the user, the painful task, the evidence, the alternatives and the remaining gap in under one minute. If the user need is not validated, label it an assumption and design a demo that does not pretend otherwise.

## Phase 2: Freeze the solution and the features (3:30-4:30 PM)

At 4:30 PM the solution is frozen; after that it changes only if a P0 feature proves impossible. Use the Notion One-Page Canvas as the solution brief so you write it once.

**Freeze the solution**

- [ ] Choose one solution; check it against the rubric by mapping every criterion to a feature or a pitch section
- [ ] Write the value proposition: For \[user\] who needs to \[job\], our product \[benefit\] by \[how it works\], unlike \[current alternative\]
- [ ] Write a specific USP that answers who benefits, what gets easier, why it differs from the alternative, and whether the demo can show it; "AI-powered" alone is not a USP
- [ ] Fill the Canvas Problem and Product sections: one-sentence solution, main benefit, USP, a 3-6 step core journey, and what we will not build
- [ ] Pick one demo scenario: one user, one story, one outcome

**Define the features**

- [ ] List every candidate feature, then score each on user value, rubric importance, feasibility, demo clarity, risk of failure and outside dependencies
- [ ] Sort into P0 (must work), P1 (should work) and P2 (nice to have); keep P0 to a small set that works end to end
- [ ] Enter each feature on the Notion Feature Board with an owner, a priority, a demo-critical tick and how it will be verified
- [ ] Agree the primary metric, how the baseline will be measured, and a target labeled as a target, not a result
- [ ] Write five test cases: typical, edge, ambiguous, invalid or missing input, and a failed-service case
- [ ] Set the feature-freeze time (suggested 6:00 AM) and the integration checkpoints (suggested 9 PM and midnight)

**Checkpoint:** all three describe the same product in the same words. If they describe three different products, the solution is not frozen yet.

## Phase 3: Decide how it works, then the tools (4:30-5:30 PM)

Decide what each feature does before choosing any technology, in this order: flow, logic, stack, architecture, contract, structure. Write all of it in one master brief with a section per step, not nine separate files.

**Flow and logic**

- [ ] Write the user flow as a numbered sequence (what the user enters, what happens, what result they see) and sketch the main screens
- [ ] For each P0 feature write the input, the processing and the output
- [ ] Pick the simplest method that works: plain logic, an existing model, an LLM, a trained ML model, or a mix; do not use an LLM only because this is the AI/ML track
- [ ] Decide how the system shows its evidence, and what happens when the AI is wrong (validation, fallback, human review)

**Stack and architecture**

- [ ] For each of frontend, backend, AI/ML, database, outside APIs and deployment, record the choice, the reason, one alternative, setup time, cost or usage limit, and a fallback
- [ ] Confirm a database is needed at all; skip it if the core flow needs no saved records
- [ ] Check free-tier limits and which services sleep or cold-start when idle
- [ ] Sketch the architecture: each component, its job, what it receives, what it returns

**Contract and structure**

- [ ] Write the API contract: endpoint, method, input, output, errors, owner
- [ ] Save sample responses so the frontend can start on mock data immediately
- [ ] Agree the data: demo data, seed data, test cases, and that nothing private is used
- [ ] Agree the folder structure, which person owns which folder, the environment variable names, and the run commands

**Checkpoint:** each person can start work without waiting for anyone else, and the sample API responses exist.

### Decision register

Every hackathon needs these decisions, whatever the problem statement.

| Decision | Question to answer | Decided by | By |
| --- | --- | --- | --- |
| Go or no-go on the problem | Does it fit the track, our skills and the rubric? | Team | 2:45 PM |
| User and problem | Who, doing what, blocked by what? | Team | 3:30 PM |
| Solution and USP | What do we build and why is it different? | Ankush, team agrees | 4:00 PM |
| Priorities | What is P0, P1, P2? | Ankush | 4:30 PM |
| Metric and baseline | How do we show it helps? | Anamika, Ankush | 4:30 PM |
| Demo scenario | Which one story do we show? | Ankush, Aditya | 4:30 PM |
| AI/ML method | Simplest method that meets the need? | Ankush, Anamika | 5:00 PM |
| Tech stack | Fastest reliable tools we already know? | Ankush | 5:15 PM |
| Architecture and API contract | Which parts, what do they send? | Ankush | 5:30 PM |
| Folders and ownership | Who owns which files? | Ankush | 5:30 PM |
| Feature freeze and checkpoints | When do we stop adding? | Team | 4:30 PM |
| Demo fallback | What if live fails, and is a backup allowed? | Team | 9 AM |
| Submission owner | Who runs the final checklist? | Ankush | 6 AM |

## Phase 4: Repo setup and personal briefs (5:30-6:15 PM)

By 6:15 PM every person holds one short brief and a working branch. Keep it to one master brief plus one brief per person, so nobody spends hours reading before building. Anyone who has what they need after 5:30 PM may start early.

**Repo**

- [ ] Commit the folder structure from the master brief with empty placeholder files
- [ ] Everyone clones the repo, creates their own branch and confirms the base project runs on their laptop
- [ ] Commit .env.example with the variable names; keep real keys out of Git
- [ ] Put the sample API responses and shared data formats in a shared folder

**Briefs**

- [ ] Write a brief per person with: objective, inputs, expected outputs, files owned, dependencies, acceptance criteria, and what is out of scope
- [ ] Link each brief to the master brief and the Feature Board rows that person owns
- [ ] Set up the Antigravity instruction for each person: read the master brief and personal brief first, touch only owned files, commit after every working step
- [ ] Each person reads their brief and says back in one sentence what they will deliver by 9 PM

**Checkpoint:** three branches exist, the base project runs for everyone, and each person has stated their 9 PM deliverable.

## Phase 5: Parallel build and early integration (6:15 PM-6:00 AM)

Build one working end-to-end path first, then widen it. The Playbook calls this a vertical slice: input, processing, a useful result and clear errors, all connected. This is the longest phase, so the checkpoints below keep it honest.

**Working rules**

- [ ] Small commits, pushed at least every hour; open a pull request when a piece works
- [ ] Main always runs; merge only code that starts and passes a quick check
- [ ] Whoever is awake may merge a working pull request; the lead does not have to be the only merger
- [ ] Update the Feature Board status as each feature moves to Building and Done
- [ ] Keep a claims list from the start: what is built, partial, mocked, planned, measured or only hypothesized
- [ ] Keep README run instructions updated as you go, not at the end

**Checkpoints**

- [ ] 9 PM: first thin slice runs end to end, even if parts use mock data
- [ ] Midnight: first real end-to-end run with real components; if not, cut P2 and review P1 immediately
- [ ] 3 AM: all P0 features work in at least a basic form
- [ ] 6 AM: core complete; feature freeze

**Per person, in parallel**

- [ ] Ankush: AI and agent core, then integration of every part, then code review of pull requests
- [ ] Anamika: ML pipeline or model, the test cases, and a record of baseline timings and results for the evidence slide
- [ ] Aditya: interface on mock data first, then real API; also the deck template and the first draft of slides 1-4
- [ ] Help rule: when your part is blocked or finished, take a task from the Feature Board or help the person who is behind

**Rhythm**

- [ ] Five-minute stand-up every two hours: done, doing, blocked, at risk
- [ ] Take a short break every two hours: water, food, walk
- [ ] Follow the sleep rota from midnight (see Time management)

**Gate:** a teammate who did not build the feature can run the main workflow from a clean start and explain what happened.

## Phase 6: Freeze, test, deploy, fix (6:00-9:00 AM)

After the freeze only bug fixes go in, so the demo you rehearse is the demo you submit. Aim to leave this phase with a deployed, tested product and a reset procedure.

**Freeze and test**

- [ ] Announce the feature freeze; new ideas go on a "later" list, not into the code
- [ ] A teammate who did not build the feature runs the main workflow from a clean start and explains what happened
- [ ] Test empty input, invalid input, slow response, a failed API request, unexpected output, and a page refresh
- [ ] Run the five test cases (typical, edge, ambiguous, invalid, service failure) and record the real results, including failures
- [ ] Check small-screen layout and the demo account or permissions, if they matter
- [ ] Fix only critical bugs; log the rest as known limitations

**Safety and reliability**

- [ ] Confirm no secrets, keys or private data are in the repo, the screen or the demo
- [ ] Confirm demo data is appropriate and non-sensitive
- [ ] Check remaining API quota; add caching or a fallback for the demo path
- [ ] Deploy, or choose a stable local setup, and open it from another device and network
- [ ] Wake any sleeping free-tier service and note how long a cold start takes
- [ ] Seed demo data, prepare a second valid input, and write a reset procedure that returns the demo to a clean start

**Docs**

- [ ] README explains how to run the project from scratch, with required attribution and licenses

**Gate:** the deployed version works from a clean start, a second person can run it, and the reset procedure is tested.

## Phase 7: Evidence, deck, rehearsal, submission (9:00 AM-1:00 PM)

Submit by 1:00 PM at the latest, aiming for 12:30 PM, which leaves the last hour as a recovery buffer. If judging happens before 2 PM, move every time in this phase earlier.

**Evidence (9:00-10:00 AM)**

- [ ] Measure the baseline and the prototype on the same task under the same conditions
- [ ] Label every number as measured, estimated or targeted; leave out any number you cannot back
- [ ] Write down the known limitations and how the AI can be wrong

**Deck and demo script (10:00-11:00 AM)**

- [ ] Build the deck from the pitch structure: 1 problem and user, 2 evidence, 3 cost and urgency, 4 solution and difference, demo, 5 before and after, optional architecture, final team and next steps
- [ ] Fit the deck to the official presentation length; do not pad it
- [ ] Write the demo script: one scenario, start from the home screen, show the main value early, speak about the user's problem rather than every button
- [ ] Mark each feature honestly as built, partial, mocked, planned or measured

**Rehearsal (11:00 AM-12:00 PM)**

- [ ] Two timed run-throughs on the exact device, screen and network of the demo
- [ ] Rehearse speaker handoffs; everyone can explain the problem, the flow and the limits
- [ ] Prepare a backup (recorded demo or screenshots) only if the rules allow it, and say clearly when it is not live
- [ ] Rehearse the Judge Q&A Bank: listen, clarify, answer directly, give evidence, state the limit; decide who answers what
- [ ] Wake sleeping services again 30 minutes before the slot

**Submit (12:00-1:00 PM)**

- [ ] Fix critical bugs only
- [ ] Run the full Notion Submission Checklist: problem and product, technical quality, impact and evidence, pitch and demo, submission
- [ ] Check that links, repository access and forms open from a logged-out browser
- [ ] Submit, then save a screenshot of the confirmation
- [ ] Use the remaining time for questions practice and rest; do not start new work
- [ ] After the event, fill the Retro Template

**Gate:** the submission is confirmed, the demo has been rehearsed twice, and each member can answer basic questions.

## Role roadmap

Each person owns a lane in every phase, and everyone helps when blocked. These are starting responsibilities, not rigid walls; the Playbook's three roles (product and research, engineering and integration, frontend and demo) are spread across the team below, with Anamika taking the research, evidence and metric work so Ankush is not the bottleneck.

| Phase | Ankush (lead, AI) | Anamika (ML) | Aditya (UI/UX, deck) |
| --- | --- | --- | --- |
| 0. Before start | Repo, templates, accounts, Antigravity instruction | Check ML tools and data access work | Set up UI tools and a blank deck template |
| 1. Understand | Runs the rules read, Event Brief, go or no-go | Scale evidence with sources, alternatives | Judging view on design and demo; persona; venue questions |
| 2. Freeze | Facilitates, writes Canvas, USP, P0/P1/P2 | Metric, baseline, test cases, ML feasibility | Demo scenario and storyline, demo clarity check |
| 3. Decide | Flow, logic, stack, architecture, API contract, folders | Logic for ML parts, data sources, method | Wireframes from the flow; confirms fields the UI needs |
| 4. Briefs | Writes master and personal briefs, repo, Antigravity setup | Reads brief, sets up environment | Reads brief, sets up frontend base |
| 5. Build | AI and agent core, integration, reviews and merges | ML pipeline, test cases, baseline timings | UI on mock data, then real API; deck slides 1-4 |
| 6. Freeze and test | Coordinates testing, deploys backend, critical fixes | Runs test cases, records real results | UI polish, error states, small screen, clean-start test |
| 7. Submit | Architecture slide, final checklist, submission owner | Before and after evidence, ML questions | Deck design, demo flow, timekeeping in rehearsal |

**Always true for everyone**

- [ ] I can explain the problem, the core flow and the honest limits in one minute
- [ ] I update the Feature Board when my status changes
- [ ] I ask for help after 30 minutes stuck
- [ ] I push my work and leave a three-line note before I sleep

## Time management

Planning and deciding take the first 3.5 hours, the build ends at 6:00 AM, and the last 8 hours protect testing, rehearsal and submission. The Notion Playbook's sample split spends about 6 hours on rules, planning and task split; this plan compresses that because your templates are ready, and it starts the build at 6:15 PM instead of about 8 PM. Treat the split as a starting point and move it if the problem demands.

&#91;embedded content: schedule timeline · 8 phases, 4 checkpoints\]

Decisions finish by 5:30 PM and briefs by 6:15 PM, the build runs 11.75 hours to the 6 AM freeze, and the last 8 hours cover testing, rehearsal, submission and buffer.

**Time boxes**

- Decisions: 10 minutes each; if the team is split, the lead decides and the team moves on
- Debugging: stuck 30 minutes means ask for help; stuck 60 minutes means change approach or cut the feature
- Any new non-P0 idea that needs more than 2 hours is cut
- Research: 20 minutes per question, then write down what you have
- Meetings: stand-ups are 5 minutes, every 2 hours

**Gate checks**

At 9 PM, midnight, 3 AM, 6 AM, 9 AM and 11 AM, ask one question: are we on track for the next gate? If not, cut in this order: P2 features, P1 features, polish and animations, optional slides. Never cut integration, testing, rehearsal or the submission buffer.

**Sleep rota (suggested)**

Two people stay awake at all times. Each sleeper pushes their work and leaves a three-line note first. Swap the order to match who is most tired.

| Slot | Sleeper | Awake |
| --- | --- | --- |
| 12:00-2:00 AM | Aditya | Ankush, Anamika |
| 2:00-4:00 AM | Ankush | Anamika, Aditya |
| 4:00-6:00 AM | Anamika | Ankush, Aditya |

Eat and drink at fixed times, and take a five-minute break every two hours. Tired people make the mistakes you fix at 11 AM, so do not skip the rota to gain two hours of code.

## What to avoid

Most hackathon losses come from a handful of traps, each with a warning sign and a rule that breaks it. Read this table at every gate check.

| Trap | Warning sign | Rule that breaks it |
| --- | --- | --- |
| Debug loop | Same error for over 30 minutes | Ask a teammate at 30 minutes; at 60 minutes change approach or cut the feature |
| AI-assistant loop | The coding agent keeps rewriting or undoing the same thing | After 3 failed tries, restate the exact error, file and expected result, or write it by hand; commit before every big agent run |
| Agent edits others' files | Merge conflicts, broken pages nobody touched | Each person's instruction names owned files only; review every diff |
| Choosing tools before the solution | Stack debate in the first hour | Tools come after flow and logic (Phase 3) |
| Stack churn | Switching library or model at night | A stack change needs the lead's approval and a stated reason |
| Scope creep | New feature ideas after 4:30 PM | Put it on the "later" list; non-P0 over 2 hours is cut |
| Over-engineering | Multiple agents, vector store or database no one needs | Use the simplest method that meets the need |
| Research rabbit hole | Reading for an hour with nothing written | 20-minute box, then record the source and move on |
| Polish too early | Animations before the core works | No visual polish until the end-to-end path runs |
| Late integration | Parts only meet after midnight | Mock slice by 9 PM, real end-to-end by midnight |
| Merge chaos | Main is broken or has conflicts | Main always runs; small pull requests; merge when green |
| Solo hero | One person stuck or overloaded while others idle | Help rule: finished or blocked means take a Feature Board task |
| Unsupported claims | Numbers on slides nobody measured | Label every number measured, estimated or targeted; leave out the rest |
| Faking the demo | Mock output shown as live | Say which parts are live, partial, mocked or planned |
| Free-tier traps | Slow first load, quota errors on demo day | Check limits early, wake services, cache, keep a fallback |
| Secrets in Git | Keys in code or on screen | Use .env, keep it ignored, rotate any leaked key |
| Ignoring the rubric | Features that no criterion rewards | Map every feature and slide to a criterion |
| Skipping sleep | Careless bugs, short tempers after 3 AM | Follow the rota; two people awake at all times |
| Too many documents | Hours of writing before any code | One master brief plus one brief per person |
| Last-minute panic | New work after the freeze, deck started at noon | Freeze at 6 AM; rehearse twice; submit by 1 PM |

If you notice yourself in a loop, say "loop" out loud and run the 30-minute rule: stop, ask, and decide to continue, change approach or cut.
