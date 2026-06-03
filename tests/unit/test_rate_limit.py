from app.modules.rate_limits.service import RateLimitService


def test_window_blocks_after_max():
    rl = RateLimitService(max_messages=3, window_seconds=60, cooldown_seconds=0)
    assert rl.check(1).allowed
    assert rl.check(1).allowed
    assert rl.check(1).allowed
    decision = rl.check(1)
    assert not decision.allowed
    assert decision.retry_after >= 1


def test_cooldown_between_messages():
    rl = RateLimitService(max_messages=100, window_seconds=60, cooldown_seconds=5)
    assert rl.check(7).allowed
    blocked = rl.check(7)
    assert not blocked.allowed


def test_users_are_isolated():
    rl = RateLimitService(max_messages=1, window_seconds=60, cooldown_seconds=0)
    assert rl.check(1).allowed
    assert rl.check(2).allowed  # different user, own bucket
