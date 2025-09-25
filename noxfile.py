from __future__ import annotations

import nox

from nox_uv import session as nox_session


nox.options.default_venv_backend = "uv"


@nox_session(
    python=["3.9", "3.10", "3.11", "3.12", "3.13"],
    uv_groups=["test"],
)
def test(session: nox.Session) -> None:
    coverage_file = session.posargs[0] if session.posargs else "coverage.xml"
    session.run("pytest", "--cov=cbridge", "-v", f"--cov-report=xml:{coverage_file}")
