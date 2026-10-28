# AI Prompt Documentation — CarePing

> Assessment note: This is a template for documenting AI assistance. Keep only the prompts you actually used, and add or edit entries to accurately describe your real process. Do not claim an AI model runs inside the app; AI assistance was used during development unless you separately integrate a model.

## Project goal
Build a small healthcare appointment scheduling demo that can be completed in one day, using free tools and Python in VS Code.

## Prompt 1 — Initial project plan
**Prompt**

> I am a beginner-to-intermediate Python learner building a one-day project for an AI Skills and Prompt Engineering assessment. Suggest a small healthcare technology project that can run locally, use free tools, and be demonstrated in a two-minute video. Avoid medical advice and paid APIs.

**Expected use**
- Choose a feasible scope.
- Identify core features and safety limitations.
- Keep the project small enough to test in one day.

## Prompt 2 — Build the first version
**Prompt**

> Create a complete beginner-friendly Streamlit app in Python called CarePing. It should let a user add fictional healthcare appointments with name, type, date, time, optional contact and notes; list appointments sorted by date/time; show counts for total, today, and next seven days; load sample records; remove a record; and export data to CSV. Include input validation and clear user feedback. Do not implement medical advice or claim to send real reminders. Keep the code in one app.py file.

**Expected use**
- Generate an initial app structure.
- Keep UI and logic easy to explain.
- Use session state for the prototype.

## Prompt 3 — Improve the user experience
**Prompt**

> Review the Streamlit appointment app for usability. Make the page clear for a first-time user, add a quick-start sample-data button, separate adding, viewing, and exporting into tabs, show upcoming appointments in plain language, and include a visible privacy note. Do not add unnecessary dependencies.

**Expected use**
- Refine layout and onboarding.
- Make the demo easier to present.

## Prompt 4 — Check edge cases and safety
**Prompt**

> Review this appointment scheduling demo for common issues: blank patient name, empty appointment list, sorting date/time, removing the correct row, CSV export, and appointments in the past. Suggest fixes and make sure the app clearly says it does not send actual SMS/email notifications, is not a clinical system, and should only use fictional data.

**Expected use**
- Find likely edge cases.
- Improve validation and accurately state limitations.

## Prompt 5 — Documentation and video
**Prompt**

> Write a beginner-friendly README for running this Streamlit app on Windows PowerShell in VS Code. Include setup commands, features, limitations, a six-step demo flow, and a checklist for the assessment submission. Also draft a video script that explains tool selection, prompt iterations, approach, challenge/solution, and final demo in over two minutes.

**Expected use**
- Prepare setup and presentation materials.

## Prompt refinement record
For your final submission, record your real iterations below. Example format:

| Iteration | What was wrong or missing? | Follow-up prompt used | What changed? |
|---|---|---|---|
| 1 | Initial app lacked a quick demo path. | “Add fictional sample data and a quick-start button.” | Sample records can be loaded. |
| 2 | Empty state was unclear. | “Show a helpful message when there are no appointments.” | Added guidance to add a record or load samples. |
| 3 | The app could be mistaken for a real notification service. | “Clearly label the project as a prototype and state that it does not send messages.” | Added limitation and privacy notices. |

**Important:** These are suggested prompts and example refinements for the project package. Replace them with the exact prompts and changes from your actual development process before submitting the assessment.
