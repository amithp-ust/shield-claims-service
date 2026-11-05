# Linked implementation consumer

- Author specs only in [amithp-ust/Intent-to-spec](https://github.com/amithp-ust/Intent-to-spec).
  Full Spec Kit, authoring agents, gate workflows, and requirement metrics belong
  there. Do not install them here or duplicate specs/component slices.
- Read the approved spec at its full immutable commit SHA and exact canonical
  path, plus [Shield context](https://github.com/amithp-ust/shield-context) at its
  reviewed revision (glossary, map, scope, standards, policy). Branch links are
  discovery links, not approval evidence. Do not infer model/tool/compliance approval.
- Application issues and code PRs must link that source canonical spec, commit,
  requirement IDs, and context revision. Keep `CM-CLAIMS` implementation and
  contract ownership here. Code PRs require human review; no automatic merges.
- From this repo root, run `python -m unittest discover -s tests` (Python 3.11,
  standard library only). CI runs the same command. Use synthetic data only.
- Preserve fixture API/event schemas and linked policy-risk-view contracts.
  Coordinate provider/consumer contract changes, update affected tests, then run
  `python scripts/verify_fixture.py --repos-root ..` from a sibling
  `shield-context` checkout with all six app checkouts present. Context validation
  dependencies are documented there; do not install authoring to run fixtures.
- Empty `specs/.gitkeep` is legacy, not a publication target. Preserve historical
  specs; report existing authoring content for reviewed migration, not blind deletion.
