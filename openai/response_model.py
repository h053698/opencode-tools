from dataclasses import dataclass
from typing import Literal

@dataclass
class Codex5HoursUsage:
    used_percent: int
    limit_window_seconds: int
    reset_after_seconds: int
    reset_at: int

@dataclass
class CodexWeeklyUsage:
    used_percent: int
    limit_window_seconds: int
    reset_after_seconds: int
    reset_at: int

@dataclass
class CodexCodeReviewUsage:
    allowed: bool
    limit_reached: bool
    used_percent: int
    limit_window_seconds: int
    reset_after_seconds: int
    reset_at: int


@dataclass
class CodexLimitResponse:
    plan_type: Literal["free", "pro", "plus"]
    rate_limited: bool
    has_credits: bool
    unlimited: bool
    credit_balance: int
    five_hours_usage: Codex5HoursUsage
    weekly_usage: CodexWeeklyUsage
    code_review_usage: CodexCodeReviewUsage
