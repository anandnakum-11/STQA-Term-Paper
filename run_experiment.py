"""Run a small, reproducible seeded-fault experiment for the STQA paper.

This uses explicit mutant functions so it can run on native Windows without
requiring a POSIX-only mutation-testing runner. It is a controlled teaching /
case-study experiment, not a substitute for a large industrial benchmark.
"""
from __future__ import annotations
import csv
from pathlib import Path
from src.discount_system import calculate_discount

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# Test cases are input + expected output, copied from / represented by the paper.
SUITES = {
    "Statement coverage": [
        (8000, 1, 0, 1600.0), (8000, 0, 0, 800.0),
        (3000, 0, 1, 500.0), (3000, 1, 0, 0.0),
    ],
    "Branch coverage": [
        (8000, 1, 0, 1600.0), (8000, 0, 0, 800.0),
        (3000, 0, 1, 500.0), (3000, 1, 0, 0.0),
    ],
    "Decision table": [
        (8000, 1, 0, 1600.0), (8000, 0, 1, 800.0),
        (3000, 0, 1, 500.0), (3000, 1, 0, 0.0),
    ],
    "OAT": [
        (8000, 1, 1, 1600.0), (8000, 0, 0, 800.0),
        (3000, 1, 0, 0.0), (3000, 0, 1, 500.0),
    ],
    "Hybrid + boundary cases": [
        (8000, 1, 0, 1600.0), (8000, 0, 0, 800.0),
        (3000, 0, 1, 500.0), (3000, 1, 0, 0.0),
        (5000, 1, 0, 1000.0), (5000, 0, 1, 500.0),
        (4999, 1, 1, 500.0), (4999, 0, 0, 0.0),
    ],
}

# Faults are intentionally introduced one at a time. Expected outputs always
# come from the correct specification, not from the mutant implementation.
def mutant_threshold_gt(amount, is_member, has_coupon):
    if amount > 5000:  # defect: >= changed to >
        return amount * (0.20 if is_member == 1 else 0.10)
    return 500.0 if has_coupon == 1 else 0.0

def mutant_member_inverted(amount, is_member, has_coupon):
    if amount >= 5000:
        return amount * (0.20 if is_member == 0 else 0.10)  # defect
    return 500.0 if has_coupon == 1 else 0.0

def mutant_member_rate(amount, is_member, has_coupon):
    if amount >= 5000:
        return amount * (0.30 if is_member == 1 else 0.10)  # defect: 30%
    return 500.0 if has_coupon == 1 else 0.0

def mutant_nonmember_rate(amount, is_member, has_coupon):
    if amount >= 5000:
        return amount * (0.20 if is_member == 1 else 0.15)  # defect: 15%
    return 500.0 if has_coupon == 1 else 0.0

def mutant_coupon_reversed(amount, is_member, has_coupon):
    if amount >= 5000:
        return amount * (0.20 if is_member == 1 else 0.10)
    return 500.0 if has_coupon == 0 else 0.0  # defect

def mutant_flat_discount(amount, is_member, has_coupon):
    if amount >= 5000:
        return amount * (0.20 if is_member == 1 else 0.10)
    return 50.0 if has_coupon == 1 else 0.0  # defect: 50 instead of 500

def mutant_no_coupon(amount, is_member, has_coupon):
    if amount >= 5000:
        return amount * (0.20 if is_member == 1 else 0.10)
    return 500.0 if has_coupon == 1 else 100.0  # defect: no-discount path

def mutant_threshold_shift(amount, is_member, has_coupon):
    if amount >= 6000:  # defect: threshold shifted from 5000 to 6000
        return amount * (0.20 if is_member == 1 else 0.10)
    return 500.0 if has_coupon == 1 else 0.0

MUTANTS = {
    "M1: >= changed to >": mutant_threshold_gt,
    "M2: membership condition inverted": mutant_member_inverted,
    "M3: member rate 20% to 30%": mutant_member_rate,
    "M4: non-member rate 10% to 15%": mutant_nonmember_rate,
    "M5: coupon condition reversed": mutant_coupon_reversed,
    "M6: flat discount 500 to 50": mutant_flat_discount,
    "M7: no-coupon result 0 to 100": mutant_no_coupon,
    "M8: threshold 5000 to 6000": mutant_threshold_shift,
}

# First verify the oracle/specification against the reference implementation.
for suite_name, cases in SUITES.items():
    for amount, member, coupon, expected in cases:
        actual = calculate_discount(amount, member, coupon)
        if actual != expected:
            raise AssertionError(
                f"Reference failed {suite_name}: {(amount, member, coupon)} "
                f"expected {expected}, got {actual}"
            )

rows = []
for suite_name, cases in SUITES.items():
    killed = []
    survived = []
    for mutant_name, mutant_fn in MUTANTS.items():
        detected = any(
            mutant_fn(amount, member, coupon) != expected
            for amount, member, coupon, expected in cases
        )
        (killed if detected else survived).append(mutant_name)
    score = len(killed) / len(MUTANTS) * 100
    rows.append({
        "technique": suite_name,
        "test_cases": len(cases),
        "mutants_total": len(MUTANTS),
        "mutants_killed": len(killed),
        "mutants_survived": len(survived),
        "mutation_score_percent": round(score, 2),
        "killed_mutants": "; ".join(killed),
        "survived_mutants": "; ".join(survived),
    })

out_file = RESULTS / "fault_injection_results.csv"
with out_file.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print("Controlled fault-injection results")
print("=" * 96)
print(f"{'Technique':<28} {'Cases':>5} {'Killed':>7} {'Survived':>9} {'Score':>9}")
print("-" * 96)
for row in rows:
    print(f"{row['technique']:<28} {row['test_cases']:>5} {row['mutants_killed']:>7} "
          f"{row['mutants_survived']:>9} {row['mutation_score_percent']:>8.2f}%")
print("\nDetailed results saved to:", out_file)
print("Note: the score is specific to these eight seeded faults and these test suites.")
