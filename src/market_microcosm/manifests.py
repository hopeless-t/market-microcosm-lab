from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json


@dataclass(frozen=True)
class RunManifest:
    generation: int
    world_version: str
    observer_version: str
    policy_name: str
    verifier_version: str
    scenario_ids: tuple[str, ...]
    code_revision: str = "working-tree"

    def canonical_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    @property
    def run_id(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()[:16]
