# RPE-013 — CI amplification and batched materialization

## Trigger

RPE itself reproduced the resource-amplification pattern it was studying. The Part 3 branch accumulated 47 commits across 47 changed files while pull-request CI had been triggered 44 times by the observed snapshot.

This does **not** estimate runner cost, energy, carbon, billing, or Human delay. It establishes only that fine-grained branch materialization can multiply verification work.

## Failure biopsy

The previous write pattern was effectively:

```text
research atom
  -> create one file
  -> create one commit
  -> advance PR head
  -> trigger full CI
```

For a multi-file research step this couples logical authoring granularity to expensive verification granularity.

## Candidate correction

Build multiple blobs and one Git tree first, then create one commit and move the branch ref once:

```text
N pending files
  -> N blobs
  -> one tree
  -> one commit
  -> one branch update
  -> one PR CI run
```

The key invariant is not "fewer tests". The complete regression chain remains mandatory. The change is to **amortize branch-head materialization** across a coherent research batch.

## Bounded model

For `N` independent file writes:

```text
sequential branch updates = N
batched branch updates    = 1
avoided branch updates    = N - 1
reduction fraction        = (N - 1) / N
```

This is an update-count identity, not a claim that CI runtime or monetary cost falls by the same fraction.

## Self-hosted falsifier

RPE-013 must use the batched Git-tree path to add its own code, tests, and protocol in a **single branch-head advance**. If the implementation itself again requires one branch update per file, the experiment fails its own operational contract.

## Authority boundary

```text
authority_effect = NONE
claim_ceiling = REPOSITORY_WORKFLOW_OBSERVATION
```

No workflow is disabled. No existing E000-E023 verification is bypassed. Batching changes when the full verifier is triggered, not what evidence is required.

## Next bridge

RPE-014 should estimate projection maturity from downstream evidence, not from file persistence alone. After that bridge, the RPE bootstrap should stop expanding by default and hand control back to the main Market Microcosm programme.
