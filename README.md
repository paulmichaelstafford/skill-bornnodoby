# skill-bornnodoby

OpenCode skills for the bornnobody project and, where a skill is generic, for
other projects too.

## Layout

```
skills/
└── architecture-review/
    └── SKILL.md
```

One directory per skill, each with a `SKILL.md`. Supporting files (scripts,
references) sit beside it and are addressed relative to that directory. The
directory name is the skill ID; keep it lowercase kebab-case.

## Use in OpenCode

Point a config at the `skills/` directory:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["~/workspace/skill-bornodoby/skills"]
}
```

The bornnobody repository already has this in its `opencode.jsonc`, with the
same `~/` path. A project config is preferred for bornnobody-specific skills so
they are not advertised in unrelated projects.

On another machine, clone this repository and adjust the path, or check it out
where the config expects it.

## Adding a skill

1. Create `skills/<id>/SKILL.md` with `name` and a specific `description` —
   the description is what the model sees before loading the skill.
2. Keep one concern per skill, and say what it must not judge.
3. If the skill depends on a generated file in the target repository, name the
   generator and treat a stale file as a finding.
4. Commit and push.

## Skills here

| ID | Used by | Purpose |
| --- | --- | --- |
| `architecture-review` | bornnobody | Module and kind boundaries, the import matrix, and the architecture guard tests |
