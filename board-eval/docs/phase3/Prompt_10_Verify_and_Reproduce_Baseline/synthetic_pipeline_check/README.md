# SYNTHETIC — pipeline check only

`baseline_report_SYNTHETIC_mock.md` was produced by running the real scripts on outputs of `MockBackend`,
a fake model that answers correctly 60% of the time by construction. It shows that `run_experiment.py`
and `baseline_report.py` run end to end and that the determinism and SC-curve columns are computed.
**None of its numbers is a result and none may be reported.**
