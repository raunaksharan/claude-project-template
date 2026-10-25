---
name: clarify-before-building
description: Use before building anything non-trivial (a milestone module, a new rule, a new tool, a change of behaviour) to find out what is actually wanted and record the answers in CLAUDE.md › Clarifications. Adapted from obra/superpowers brainstorming (MIT).
---

# Clarify before building

You build what you believe is wanted, and that belief is usually thinner than it feels.
In a system that makes consequential decisions, a wrong guess becomes a wrong outcome,
so find out first. (Adapted from obra/superpowers `brainstorming`; see
THIRD_PARTY_NOTICES.md.)

## 1. Look before you ask

Read these before your first message, and never ask what they already answer:

- CLAUDE.md, including **Clarifications** (settled questions stay settled)
- the milestone's `SPEC.md`, its acceptance criteria and the tests it names
- `ARCHITECTURE.md`, `architecture/requirements.md`, the ADRs and `architecture/failure-modes.md`
- the source of truth for any rule or threshold involved

## 2. Decide whether anything is missing

- **Everything that matters is in the spec:** say so in one line and go to `write-plan`.
- **Something that would change the code is open:** ask about it, one question per
  message, in plain words, saying what the answer changes.

Typical open questions:

- `>` or `>=` for a threshold, and the unit;
- what happens when an input is missing, empty or malformed (never a default value);
- required or optional, for a new dependency (does its failure escalate or degrade?);
- which outcome a breach produces (reject, or escalate to a human);
- which source document or owner settles it.

## 3. Record the answer

Add one line under **Clarifications** in CLAUDE.md:

```text
- **<the question, short>:** <the answer>. (<who or what settled it: SPEC §, ADR, owner>)
```

## 4. Hand over

When nothing material is open, say what you understood in three lines or fewer, then use
`write-plan`.

<rules>
- One question per message.
- Never pick an interpretation silently (karpathy-guidelines §1).
- Thresholds and expected outcomes come from the people who own them, never from you.
- Unattended (nobody can answer): choose the reading most consistent with SPEC.md,
  CLAUDE.md and the existing code, write it as an assumption in the plan, and carry on.
</rules>
