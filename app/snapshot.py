"""Database model for snpashots.

___main__ will actually make the snapshot happen and persist it.
"""
import datetime
import speedtest

from app import db


def do_speedtest():
    """Run the speedtest and return results as a dict."""
    s = speedtest.Speedtest(source_address=None, timeout=10, secure=False)
    s.get_best_server()
    s.download()
    s.upload(pre_allocate=True)
    results_raw = s.results.dict()

    return dict(
        download_mbits=results_raw["download"] * 1e-6,
        upload_mbits=results_raw["upload"] * 1e-6,
        ping_ms=results_raw["ping"],
    )


class Snapshot(db.Model):
    """Database model for network snapshots."""

    __tablename__ = "snapshots"

    id = db.Column(db.Integer, primary_key=True)
    dttm_utc = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    ping_ms = db.Column(db.REAL, nullable=False)
    download_mbits = db.Column(db.REAL, nullable=False)
    upload_mbits = db.Column(db.REAL, nullable=False)


if __name__ == "__main__":
    results = do_speedtest()
    snapshot = Snapshot(**results)
    db.session.add(snapshot)
    db.session.commit()
