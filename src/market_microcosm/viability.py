from __future__ import annotations

from dataclasses import dataclass

from .toy_world import Action, ToyState, ToyWorld


@dataclass(frozen=True)
class ViabilityResult:
    kernel: frozenset[ToyState]
    iterations: int

    def safe_actions(self, world: ToyWorld, state: ToyState) -> tuple[Action, ...]:
        if state not in self.kernel:
            return ()
        actions: list[Action] = []
        for action in world.actions:
            if not world.feasible(state, action):
                continue
            successors = [world.step(state, action, w) for w in world.disturbances]
            if all(s in self.kernel for s in successors):
                actions.append(action)
        return tuple(actions)


def exact_robust_viability_kernel(world: ToyWorld) -> ViabilityResult:
    kernel = {s for s in world.states() if world.viable(s)}
    iterations = 0
    while True:
        iterations += 1
        next_kernel: set[ToyState] = set()
        for state in kernel:
            for action in world.actions:
                if not world.feasible(state, action):
                    continue
                if all(world.step(state, action, w) in kernel for w in world.disturbances):
                    next_kernel.add(state)
                    break
        if next_kernel == kernel:
            return ViabilityResult(frozenset(kernel), iterations)
        kernel = next_kernel


def oracle_action(world: ToyWorld, result: ViabilityResult, state: ToyState) -> Action:
    safe = result.safe_actions(world, state)
    if not safe:
        raise ValueError("state is outside the robust viability kernel")

    def score(action: Action) -> tuple[int, int]:
        successors = [world.step(state, action, w) for w in world.disturbances]
        return (
            min(s.minimum_reserve for s in successors),
            min(s.welfare for s in successors),
        )

    return max(safe, key=score)
