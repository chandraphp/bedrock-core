"""Tests for Event Bus and Stage protocol.

Workflow orchestration (the Workflow class) is tested here as an
internal implementation detail — it is NOT asserted as part of the
public API. See ADR-006 review decision: Workflow is promoted only
when a second independent workflow proves orchestration belongs in
the runtime.
"""

from bedrock_core import (
    EventBus, EventType, RuntimeEvent, Stage, StageResult,
)
# Workflow imported directly — not via public API
from bedrock_core.workflow import Workflow


# ── Helpers ───────────────────────────────────────────────────────────────────

class DoubleStage(Stage):
    name = "double"
    def run(self, input, context): return input * 2

class AddTenStage(Stage):
    name = "add_ten"
    def run(self, input, context): return input + 10

class FailStage(Stage):
    name = "fail"
    def run(self, input, context): raise ValueError("intentional failure")


# ── Event Bus ─────────────────────────────────────────────────────────────────

def test_event_bus_subscribe_and_publish():
    bus    = EventBus()
    events = []
    bus.subscribe(events.append)
    bus.publish(RuntimeEvent(event_type=EventType.WORKFLOW_STARTED, source="test"))
    assert len(events) == 1
    assert events[0].event_type == EventType.WORKFLOW_STARTED


def test_event_bus_type_filter():
    bus   = EventBus()
    all_  = []
    stage = []
    bus.subscribe(all_.append)
    bus.subscribe(stage.append, EventType.STAGE_COMPLETED)
    bus.publish(RuntimeEvent(event_type=EventType.WORKFLOW_STARTED, source="w"))
    bus.publish(RuntimeEvent(event_type=EventType.STAGE_COMPLETED,  source="s"))
    assert len(all_)  == 2
    assert len(stage) == 1


def test_event_bus_bad_handler_does_not_crash_runtime():
    bus = EventBus()
    bus.subscribe(lambda e: 1/0)
    bus.publish(RuntimeEvent(event_type=EventType.WORKFLOW_STARTED, source="test"))


def test_event_bus_history_and_filter():
    bus = EventBus()
    bus.publish(RuntimeEvent(event_type=EventType.STAGE_STARTED,   source="s"))
    bus.publish(RuntimeEvent(event_type=EventType.STAGE_COMPLETED, source="s"))
    assert len(bus.history) == 2
    assert len(bus.events_of_type(EventType.STAGE_STARTED)) == 1


def test_event_to_dict():
    e = RuntimeEvent(event_type=EventType.WORKFLOW_STARTED, source="test", correlation_id="abc")
    d = e.to_dict()
    assert d["event_type"] == "workflow.started"
    assert d["correlation_id"] == "abc"


# ── Stage protocol ────────────────────────────────────────────────────────────

def test_stage_result_succeeded():
    r = StageResult(stage_name="s", output=42, latency_ms=10.0)
    assert r.succeeded
    assert r.output == 42


def test_stage_result_failed():
    r = StageResult(stage_name="s", output=None, latency_ms=5.0, error="oops")
    assert not r.succeeded


def test_stage_is_abstract():
    import pytest
    with pytest.raises(TypeError):
        Stage()   # type: ignore


def test_stage_default_name_is_class_name():
    assert DoubleStage().name == "double"


# ── Workflow (internal — not public API) ──────────────────────────────────────

def test_workflow_executes_stages_in_order():
    result = Workflow(DoubleStage(), AddTenStage()).run(input=5)
    assert result.final_output == 20  # 5*2=10, 10+10=20
    assert result.succeeded


def test_workflow_emits_lifecycle_events():
    bus    = EventBus()
    events = []
    bus.subscribe(events.append)
    Workflow(DoubleStage(), bus=bus).run(input=3)
    types = [e.event_type for e in events]
    assert EventType.WORKFLOW_STARTED   in types
    assert EventType.STAGE_COMPLETED    in types
    assert EventType.WORKFLOW_COMPLETED in types


def test_workflow_records_stage_latency():
    result = Workflow(DoubleStage(), AddTenStage()).run(input=1)
    assert all(r.latency_ms >= 0 for r in result.stage_results)


def test_workflow_failed_stage_emits_event():
    bus    = EventBus()
    events = []
    bus.subscribe(events.append)
    result = Workflow(DoubleStage(), FailStage(), bus=bus).run(input=3)
    assert not result.succeeded
    types  = [e.event_type for e in events]
    assert EventType.STAGE_FAILED    in types
    assert EventType.WORKFLOW_FAILED in types


def test_workflow_correlation_id_consistent():
    bus    = EventBus()
    events = []
    bus.subscribe(events.append)
    Workflow(DoubleStage(), AddTenStage(), bus=bus).run(input=1)
    ids = {e.correlation_id for e in events if e.correlation_id}
    assert len(ids) == 1


def test_stage_composable_across_workflows():
    double = DoubleStage()
    r1 = Workflow(double).run(input=3)
    r2 = Workflow(double, AddTenStage()).run(input=3)
    assert r1.final_output == 6
    assert r2.final_output == 16


# ── Public API does NOT include Workflow ──────────────────────────────────────

def test_workflow_not_in_public_api():
    """Workflow is internal until a second independent workflow proves
    orchestration belongs in the runtime. See ADR-006 review decision."""
    import bedrock_core
    assert "Workflow"       not in bedrock_core.__all__
    assert "WorkflowResult" not in bedrock_core.__all__


def test_stage_and_events_are_in_public_api():
    import bedrock_core
    for symbol in ["Stage", "StageResult", "EventBus", "EventType", "RuntimeEvent"]:
        assert symbol in bedrock_core.__all__, f"{symbol} missing from public API"
