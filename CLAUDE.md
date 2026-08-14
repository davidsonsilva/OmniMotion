# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

**OmniMotion** is an agnóstic reverse-engineering engine for motion design. It analyzes screen recordings and interface videos using **CrewAI multi-agent orchestration** and **Clean Architecture**, extracting motion specifications (keyframes, layer positions, easing curves) and compiling them into executable artifacts (Astro, MP4, etc.).

- **Entry point**: `src/Presentation/CLI/main.py`
- **Framework**: CrewAI (multi-agent LLM coordination), Pydantic (domain validation)
- **Architecture**: Clean Architecture (Domain → Application → Infrastructure → Presentation)

## Architecture Overview

```
src/
├── Domain/                    # Enterprise rules (zero external deps)
│   ├── Entities/              # MotionTimeline, MediaLayer, Keyframe
│   └── ValueObjects/          # Dimensions (width, height)
│
├── Application/               # Use cases & interfaces
│   ├── Interfaces/            # IVideoAnalyzer, IArtifactCompiler
│   └── UseCases/              # ExtractLayoutSpecificationUseCase, CompileArtifactUseCase
│
├── Infrastructure/            # Agents, compilers, adapters
│   ├── Agents/                # CrewAIVideoAnalyzer, MotionAgentPack (Vision, Data Structuralist)
│   └── Compilers/             # AstroCompiler, MP4Compiler, CompilerFactory
│
└── Presentation/
    └── CLI/                   # main.py (argparse entry)

tests/
├── Domain/                    # Entity & ValueObject tests
├── Application/               # UseCase tests
├── Infrastructure/            # Agent & Compiler tests
└── Presentation/              # CLI integration tests
```

**Key principle**: Domain entities (MotionTimeline, Keyframe) carry zero Pydantic/CrewAI imports. They live in pure Python, tested independently. Infrastructure adapters (CrewAI, Compiler factories) depend on Domain, never the reverse.

## Common Commands

```bash
# Run video analysis pipeline
python src/Presentation/CLI/main.py --video path/to/video.mp4

# Run all tests (38 tests, ~0.1s)
python -m pytest

# Run tests in one file
python -m pytest tests/Domain/test_motion_timeline.py -v

# Run with coverage
python -m pytest --cov=src --cov-report=term-missing

# Install dependencies
pip install -e .
```

## Key Files & Layers

### Domain (`src/Domain/`)
- **Entities**: `MotionTimeline` (root aggregate: id, name, duration, keyframes[], layers[]), `MediaLayer` (screen region with z-index, opacity)
- **ValueObjects**: `Dimensions` (immutable width/height)
- **Rules**: Keyframe times must be ≥ 0, layers must not overlap beyond explicit z-index, duration must match longest keyframe
- No imports from Application, Infrastructure, or external libs (only `dataclasses`, `typing`)

### Application (`src/Application/`)
- **UseCases**: 
  - `ExtractLayoutSpecificationUseCase`: calls `IVideoAnalyzer` → returns `MotionTimeline`
  - `CompileArtifactUseCase`: takes `MotionTimeline` + compiler name → outputs artifact
- **Interfaces**: `IVideoAnalyzer` (abstract), `IArtifactCompiler` (abstract)
- Depends on Domain only. Infrastructure implements the interfaces.

### Infrastructure (`src/Infrastructure/`)
- **Agents** (`CrewAIVideoAnalyzer`): Wraps two specialized CrewAI tasks:
  - **Vision Agent** (motion tracking): reads video frame-by-frame, extracts bounding boxes, timing, easing curves
  - **Data Structuralist**: normalizes raw agent output into Pydantic `MotionTimelineSchema`, validates, returns `MotionTimeline`
- **Compilers**: 
  - `AstroCompiler`: generates `.astro` component with CSS animations
  - `MP4Compiler`: re-renders video with computed transforms
  - `CompilerFactory`: routes `MotionTimeline` → compiler by name
- Implements `IVideoAnalyzer`, `IArtifactCompiler`. Can be swapped (e.g., replace CrewAI with Claude API).

### Presentation (`src/Presentation/CLI/`)
- **main.py**: argparse CLI, calls UseCase, formats `MotionTimeline` to JSON, outputs to stdout
- Expects `GEMINI_API_KEY` env var (LLM backend for CrewAI)

## CrewAI Agents Configuration

Prompts for both agents are defined in `src/Infrastructure/Agents/`. Each agent is stateless; the crew orchestrates them sequentially:

1. **Vision Agent** (prompt-driven): Analyzes video, outputs motion metadata (frame timings, positions, easing estimates)
2. **Data Structuralist** (Pydantic-driven): Takes Vision output, structures into domain schema, validates

Both agents call the same LLM (Gemini, configurable). No agent persistence; stateless per video.

## Adding a New Compiler

1. Create file: `src/Infrastructure/Compilers/my_compiler.py`
2. Inherit `IArtifactCompiler` interface
3. Implement `def compile(timeline: MotionTimeline) -> dict[str, Any]`
4. Register in `CompilerFactory._compilers` dict
5. Call via CLI: `python ... --compiler my_compiler`
6. Add test in `tests/Infrastructure/test_compiler_factory.py`

## Extending Motion Analysis

To add a new motion feature (e.g., 3D transforms, particle effects):

1. Extend `Keyframe` ValueObject with new property (e.g., `rotation_z`)
2. Update Vision Agent prompt to extract it
3. Update Data Structuralist Pydantic schema (`KeyframeSchema`)
4. Add domain test: `tests/Domain/test_motion_timeline.py`
5. Add agent test with sample video: `tests/Infrastructure/test_crewai_video_analyzer.py`

## Testing Strategy

- **Domain tests** (8 tests): Validate entity invariants, immutability of ValueObjects
- **Application tests** (3 tests): Mock `IVideoAnalyzer`, verify UseCase orchestration
- **Infrastructure tests** (16 tests): Test CrewAI agent output parsing, compiler output format
- **Presentation tests** (4 tests): CLI argument parsing, JSON output shape

Run specific layer: `pytest tests/Domain/ -v`

## Dependencies

- **pytest**: Test runner
- **pydantic**: Domain schema validation (Infrastructure only; Domain uses dataclasses)
- **crewai**: Multi-agent LLM orchestration (Infrastructure only)

No internal packages (`src` is not installed as a package yet; CLI imports use absolute paths with `sys.path` adjustment in `main.py`).

## Environment

- **Python**: ≥3.10 (f-strings, type hints)
- **GEMINI_API_KEY**: Required for CLI execution (LLM backend)
- **`.venv/`**: Standard virtualenv, committed to repo for reproducibility

## Architecture Decisions

1. **Clean Architecture** (not layered MVC): Entities have zero framework coupling. Compilers & agents are Infrastructure details, swappable.
2. **Pydantic only in Infrastructure**: Domain entities use `@dataclass`, Application interfaces use abstract base classes. Pydantic schemas (MotionTimelineSchema) bridge CrewAI output to Domain.
3. **Stateless agents**: No agent memory or context carry-over between videos. Each analysis is fresh.
4. **CompilerFactory pattern**: Avoids hardcoding compiler selection in CLI. Easy to add new output formats.

## Gotchas

- **sys.path in main.py**: Required because src/ is not installed as a package. If refactoring to a package, remove `sys.path.insert(0, ...)`.
- **Keyframe timing**: Must be in ascending order (enforced in MotionTimeline constructor). Tests include boundary cases (0ms, negative time).
- **Gemini API latency**: CrewAI agents make multiple LLM calls per video. Budget ~10–30s per analysis.
- **Video format support**: CrewAI Vision Task expects MP4 or WebM. Other formats may fail silently; add format validation if needed.
