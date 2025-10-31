# Readable Refactor Plan

This document outlines the detailed plan for completing the refactor of the `py-readability-metrics` library into the modernized `readable` library.

## Project Overview

The `readable` project is a fork of `py-readability-metrics`, which has been in low-maintenance mode for several years. The goal of this refactor is to:

1. Modernize the codebase with current Python best practices
2. Make the library more extensible for future enhancements
3. Initially retain the current functionality (but not necessarily the API)
4. Prepare for future additions of more modern (NLP-driven) metrics

## Current State

The refactor has been initiated with:
- Original codebase archived in the `archive/` directory
- New structure started in the `readable/` directory
- Modern Python tooling added (pyproject.toml, ruff, etc.)
- Core interfaces and type definitions started
- A CLI tool (`plainr.py`) created for license text comparison

## Implementation Plan

### 1. Complete Core Data Structures and Interfaces

**Description:** Finalize the foundational data structures and interfaces needed for the refactored architecture.

**Tasks:**
- Review and enhance the existing BaseResult, BaseStatSummary, and BaseMeasure abstract classes
- Create concrete implementations of these interfaces for each readability metric
- Implement a comprehensive statistics module to replace the existing text analyzer
- Define clear data models for text analysis results with proper typing
- Ensure all interfaces follow consistent patterns and naming conventions

**Key Files:**
- `readable/types/_interfaces.py` (existing)
- `readable/types/enums.py` (existing)
- `readable/types/results.py` (new)
- `readable/text/analyzer.py` (new)
- `readable/text/statistics.py` (new)

### 2. Implement Text Analysis Engine

**Description:** Create a modern, efficient text analysis engine to replace the original implementation.

**Tasks:**
- Implement a new TextAnalyzer class that follows the defined interfaces
- Create efficient methods for counting syllables, words, sentences, and other text features
- Implement caching mechanisms to avoid redundant calculations
- Ensure proper error handling and validation
- Add comprehensive type hints and documentation
- Optimize for performance while maintaining readability

**Key Files:**
- `readable/text/__init__.py` (new)
- `readable/text/analyzer.py` (new)
- `readable/text/syllables.py` (new)
- `readable/text/tokenizer.py` (new)

### 3. Implement Individual Readability Metrics

**Description:** Create implementations for each readability metric following the new architecture.

**Tasks:**
- Create a dedicated module for each metric following consistent patterns
- Implement the scoring algorithm based on the original implementation
- Add proper type hints, validation, and error handling
- Ensure compliance with the BaseMeasure interface
- Add comprehensive docstrings and examples
- Include any metric-specific optimizations or special cases

**Key Files:**
- `readable/metrics/__init__.py` (new)
- `readable/metrics/ari.py` (new)
- `readable/metrics/coleman_liau.py` (new)
- `readable/metrics/dale_chall.py` (new)
- `readable/metrics/flesch.py` (new)
- `readable/metrics/flesch_kincaid.py` (new)
- `readable/metrics/gunning_fog.py` (new)
- `readable/metrics/linsear_write.py` (new)
- `readable/metrics/smog.py` (new)
- `readable/metrics/spache.py` (new)

### 4. Create Main Readability Class

**Description:** Implement the main Readability class that serves as the primary API.

**Tasks:**
- Create a new Readability class that orchestrates the use of the individual metrics
- Implement methods for each readability calculation
- Add convenience methods for common operations
- Ensure proper error handling and validation
- Add comprehensive documentation and examples
- Implement caching to avoid redundant calculations

**Key Files:**
- `readable/__init__.py` (new)
- `readable/readability.py` (new)

### 5. Implement Data Loading and Resources

**Description:** Create modules for loading and managing resource data needed by metrics.

**Tasks:**
- Create a resources module to manage loading and caching of word lists
- Implement efficient data structures for word lookups
- Add proper error handling for missing resources
- Ensure resources are properly packaged with the library
- Add utilities for stemming and word normalization

**Key Files:**
- `readable/resources/__init__.py` (new)
- `readable/resources/data/dale_chall_easy.txt` (new)
- `readable/resources/data/spache_easy.txt` (new)
- `readable/resources/loader.py` (new)
- `readable/resources/stemmer.py` (new)

### 6. Update and Expand Tests

**Description:** Modernize the test suite and expand coverage for the new implementation.

**Tasks:**
- Update existing tests to work with the new API
- Add unit tests for each new component
- Add integration tests for the full pipeline
- Implement property-based tests for complex algorithms
- Add performance benchmarks
- Ensure high test coverage across the codebase

**Key Files:**
- `tests/__init__.py` (new)
- `tests/test_readability.py` (update existing)
- `tests/test_metrics/` (new directory)
- `tests/test_text/` (new directory)
- `tests/test_resources/` (new directory)
- `tests/conftest.py` (new)

### 7. Create Comprehensive Documentation

**Description:** Develop detailed documentation for the new implementation.

**Tasks:**
- Create a comprehensive README with examples and installation instructions
- Develop detailed API documentation for each component
- Add usage examples for common scenarios
- Create migration guides for users of the original library
- Document the architecture and design decisions
- Set up automated documentation generation

**Key Files:**
- `README.md` (update existing)
- `docs/` (new directory)
- `docs/api/` (new directory)
- `docs/examples/` (new directory)
- `docs/migration.md` (new)
- `docs/architecture.md` (new)

### 8. Enhance CLI Tool

**Description:** Expand and improve the plainr.py CLI tool.

**Tasks:**
- Refactor the CLI to use the new implementation
- Add additional features and options
- Improve error handling and user feedback
- Add comprehensive help text and examples
- Implement configuration options
- Add support for different output formats

**Key Files:**
- `plainr.py` (update existing)
- `readable/cli/__init__.py` (new)
- `readable/cli/commands.py` (new)
- `readable/cli/formatters.py` (new)

### 9. Package and Distribution Setup

**Description:** Finalize packaging configuration and prepare for distribution.

**Tasks:**
- Complete the pyproject.toml configuration
- Set up proper versioning
- Configure package metadata
- Ensure all dependencies are properly specified
- Set up CI/CD for automated releases
- Create distribution packages for PyPI

**Key Files:**
- `pyproject.toml` (new)
- `readable/__init__.py` (new)
- `readable/__about__.py` (new)
- `.github/workflows/release.yml` (new)

### 10. Create Extensibility Examples and Documentation

**Description:** Demonstrate how to extend the library with custom metrics.

**Tasks:**
- Create examples of how to implement custom readability metrics
- Document the extension points and interfaces
- Provide templates for common extension patterns
- Add tutorials for advanced customization
- Create a plugin system if appropriate

**Key Files:**
- `docs/extending.md` (new)
- `examples/custom_metric.py` (new)
- `examples/plugin_example.py` (new)

## Implementation Approach

The implementation will follow these general principles:

1. **Maintain Functionality**: Ensure all existing readability metrics continue to work correctly
2. **Improve Extensibility**: Design interfaces that make it easy to add new metrics
3. **Enhance Type Safety**: Use proper type annotations throughout the codebase
4. **Optimize Performance**: Implement efficient algorithms and caching where appropriate
5. **Document Thoroughly**: Provide comprehensive documentation for all components

## Future Enhancements (Post-Refactor)

Once the initial refactor is complete, the following enhancements could be considered:

1. **NLP-Driven Metrics**: Implement more modern readability metrics based on NLP techniques
2. **Language Support**: Extend the library to support languages other than English
3. **Performance Optimizations**: Further optimize the core algorithms for speed and memory usage
4. **Integration Options**: Provide integrations with popular NLP libraries and frameworks
5. **Web API**: Create a simple web API for readability scoring

## Timeline Estimate

The refactor is substantial and will require significant effort. A rough timeline estimate:

- Core interfaces and data structures: 1-2 weeks
- Text analysis engine: 1-2 weeks
- Individual metrics implementation: 2-3 weeks
- Main API and integration: 1-2 weeks
- Testing and documentation: 2-3 weeks

Total estimated time: 7-12 weeks of focused development effort.

