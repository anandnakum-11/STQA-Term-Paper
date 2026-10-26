# STQA Fault-Injection Starter Project

This small Python experiment reuses the paper's E-commerce Discount System and compares the four existing test-design approaches with a hybrid suite that adds boundary-value cases.

## 1. Setup (Windows PowerShell)

Open PowerShell in this folder and run:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, skip activation and use `py -m pip install -r requirements.txt` followed by `py -m pytest` and `py -m coverage`.

## 2. Run all functional tests

```powershell
py -m pytest -q
```

All tests should pass against the correct reference implementation.

## 3. Run the seeded fault-injection experiment

```powershell
py run_experiment.py
```

The script applies eight predefined faulty implementations one at a time and checks whether each test suite detects a wrong output. It writes detailed results to `results/fault_injection_results.csv`.

Mutation score used by the script:

`Mutation Score = Mutants Killed / Total Mutants × 100`

A mutant is “killed” when at least one test produces an output different from the expected result. “Survived” means this suite did not detect that seeded fault; it does not prove the mutant is harmless.

## 4. Measure line and branch coverage separately for each suite

Run these commands one at a time. Each `erase` clears the previous suite's measurements.

```powershell
py -m coverage erase
py -m coverage run --branch -m pytest -q tests/test_statement_coverage.py
py -m coverage report -m src/discount_system.py

py -m coverage erase
py -m coverage run --branch -m pytest -q tests/test_branch_coverage.py
py -m coverage report -m src/discount_system.py

py -m coverage erase
py -m coverage run --branch -m pytest -q tests/test_decision_table.py
py -m coverage report -m src/discount_system.py

py -m coverage erase
py -m coverage run --branch -m pytest -q tests/test_oat.py
py -m coverage report -m src/discount_system.py

py -m coverage erase
py -m coverage run --branch -m pytest -q tests/test_hybrid.py
py -m coverage report -m src/discount_system.py
```

To create an HTML coverage report for the last suite:

```powershell
py -m coverage html
start htmlcov\index.html
```

## Important limitations for the paper

- Statement-coverage and branch-coverage suites use the same four input cases, matching the original paper's design. Similar mutation results are expected; do not claim the technique labels alone caused a difference.
- The eight seeded faults are deliberately selected examples, not a representative sample of all real-world defects. Describe the experiment as a small controlled case study.
- The hybrid suite adds boundary tests at 4999 and 5000. This is expected to detect threshold defects that the original representative tests can miss.
- Do not invent or pre-fill final measurements in the paper. Run the script and use its actual CSV output.
