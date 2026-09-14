"""Verify the pinned Vera settings defaults apply cleanly.

The acceptance shard repo pins ``auto_manage_issues: false`` in
``.vera/settings.yaml`` so acceptance runs are deterministic. This test
guards that the documented default is present and parses without error.
"""

from pathlib import Path


def _load_settings() -> dict[str, object]:
    """Parse the minimal ``key: value`` settings file into a dict."""
    text = (Path(__file__).resolve().parents[1] / ".vera" / "settings.yaml").read_text()
    settings: dict[str, object] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, raw = stripped.partition(":")
        value = raw.strip()
        if value.lower() in {"true", "false"}:
            settings[key.strip()] = value.lower() == "true"
        else:
            settings[key.strip()] = value
    return settings


def test_settings_defaults_apply_cleanly() -> None:
    settings = _load_settings()
    assert settings.get("auto_manage_issues") is False


def test_settings_file_is_parseable() -> None:
    # Fails if the settings file is missing or raises during parse.
    settings = _load_settings()
    assert isinstance(settings, dict)
    assert "auto_manage_issues" in settings
