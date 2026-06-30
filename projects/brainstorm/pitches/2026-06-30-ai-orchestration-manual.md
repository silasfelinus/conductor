# Pitch: Build Your First AI Assistant — a Practical Manual for Running Autonomous Agent Systems

date: 2026-06-30
project-target: digital-storefront
status: awaiting-silas

## The idea

A short-form PDF manual (30–50 pages, written for technical hobbyists) explaining how to design and run an autonomous LLM agent orchestration system like conductor. Covers: how to write a system prompt that actually works, designing the Worker/Reviewer handoff loop, scoping tasks to prevent hallucination, structuring YAML task records, and building in human-approval gates without killing momentum. Sells on Gumroad at $9–$15. No code required to follow along; the examples use conductor as a concrete reference case study.

## Why it's worth doing

Conductor is a genuinely novel hobbyist-level system and there's almost nothing published about running private multi-agent loops at this level. The audience (technical founders, indie developers, AI-curious makers) is growing fast and underserved by both vendor docs (too vendor-specific) and academic papers (too abstract). This manual turns Silas's existing system into a monetizable artifact without building anything new — it's documentation of work already done. Product type `pdf-manual` is approved.

## Rough effort

medium

## Suggested first task

Write a table of contents and chapter outlines for the manual in `projects/digital-storefront/concepts/ai-orchestration-manual.md`, with a one-paragraph summary per chapter and a target word count per section. Gate on `approved_by_human: true` before starting the full draft.
