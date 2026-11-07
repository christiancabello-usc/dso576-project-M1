from datetime import date
import pytest
from src.setup import load_defaults

def test_default_dates():
    defaults = load_defaults()
    assert defaults.start == date(2025,2,1) and defaults.end == date(2026,7,31)

@pytest.mark.parametrize('content,match', [
 ('default_area="Hollywod"\nstart="2025-02-01"\nend="2026-07-31"','Hollywod'),
 ('default_area="Mission"\nstart=2024-06-01\nend=2026-07-31','start'),
 ('default_area="Mission"\nstart="bad"\nend="2026-07-31"','start'),
 ('default_area="Mission"\nstart="2025-02-01"\nend="2025-02-01"','end'),
 ('default_area="Mission"','missing'),
 ('default_area="Mission"\nstart="2025-02-01"\nend="2026-07-31"\nextra=1','extra')])
def test_invalid_config(tmp_path, content, match):
    path = tmp_path / 'config.toml'
    path.write_text(content)
    with pytest.raises(ValueError, match=match):
        load_defaults(path)
