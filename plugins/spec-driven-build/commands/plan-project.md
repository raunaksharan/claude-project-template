---
description: Turn a project objective into an approved build plan by interviewing you until every template field is filled; stops for your approval
argument-hint: "<path to your objective doc, or paste the feature list>"
---
<task>Plan the project described by: $ARGUMENTS</task>

<method>Use the plan-project skill (read its SKILL.md, QUESTIONS.md and CATALOG.md).
Fill in what the objective already answers first. Then interview me section by section,
1–4 questions at a time, writing each answer into its file. When I don't know, give me 2–3
options with a recommendation and record what I choose. Propose skills, MCP servers and
plugins, and include any I name.</method>

<done_when>check_ready.py passes, PLAN.md is filled with Status DRAFT, and you have said
"Okay, I'm good. This is the plan." with a short summary and the open assumptions. Then
stop and wait. No code, no tests. I approve by running:
! python3 scripts/approve_plan.py --by "<name>"</done_when>
