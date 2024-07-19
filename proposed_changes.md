# Compact Search/Replace Implementation: High-Level Design Document

## 1. Overview

The compact search/replace feature aims to implement a token-efficient approach for search and replace blocks in the aider codebase. This feature will allow for more efficient communication between the AI and the program while maintaining the user-friendly full-text representation for human interaction.

## 2. Current Workflow

1. The AI receives code in text format from files in the chat session.
2. The AI processes the code and generates a response, which may include search/replace (S/R) blocks.
3. If S/R blocks are present in the AI's response, they are parsed and applied to the relevant files.
4. The changes are then committed to the git repository (if enabled).

The current S/R blocks use a verbose format that includes the full context of the changes, which is helpful for human readability but less efficient in terms of token usage.

The main scripts involved in this workflow are:

1. `aider/coders/editblock_coder.py`: Contains the `EditBlockCoder` class, which is responsible for parsing and applying the S/R blocks.
2. `aider/commands.py`: Handles various commands, including those related to git operations.
3. `aider/coders/editblock_prompts.py`: Defines the prompts used for the edit block format.

## 3. Proposed Workflow

1. The AI receives code in text format from files in the chat session.
2. Based on the active mode (standard or compact), the AI generates a response with appropriate S/R blocks.
3. If compact mode is active:
   a. The AI uses a more concise format for S/R blocks, specifying only file names, line numbers, and replacement text.
   b. The system parses these compact S/R blocks and applies the changes to the relevant files.
4. If standard mode is active, the current workflow is maintained.
5. The changes are committed to the git repository (if enabled).

## 4. Components Affected

1. `EditBlockCoder` class in `aider/coders/editblock_coder.py`
2. `Commands` class in `aider/commands.py`
3. `EditBlockPrompts` class in `aider/coders/editblock_prompts.py`

## 5. Detailed Changes

### EditBlockCoder class:
- Add a `compact_mode` flag to toggle between standard and compact modes.
- Modify `get_edits` method to use either `find_compact_blocks` or `find_original_update_blocks` based on the mode.
- Update `apply_edits` method to use either `do_compact_replace` or `do_replace` based on the mode.
- Implement new `find_compact_blocks` and `do_compact_replace` functions to handle the compact format.
- Update error messages and logging to reflect the active mode.

### Commands class:
- Add a new `/compact_sr` command to toggle the compact mode.

### EditBlockPrompts class:
- Update AI prompts to include instructions for the compact format when appropriate.

## 6. Considerations and Unknowns

- Token savings: We need to measure the actual token savings achieved by the compact mode.
- Backwards compatibility: Ensure that the system can still handle the standard format when needed.
- Error handling: Consider how to provide meaningful error messages when parsing compact format fails.
- User experience: Evaluate how the compact format affects user understanding of proposed changes.
- Performance: Assess any potential impact on processing time for parsing and applying edits.

## 7. Implementation Plan

1. Implement the `compact_mode` flag in `EditBlockCoder`.
2. Develop the `find_compact_blocks` and `do_compact_replace` functions.
3. Modify `get_edits` and `apply_edits` methods to use the new functions when in compact mode.
4. Add the `/compact_sr` command to toggle the mode.
5. Update AI prompts to include compact format instructions.
6. Implement logging and metrics for performance tracking.
7. Create unit tests for the new functionality.
8. Update documentation to reflect the new feature.
9. Conduct thorough testing, including edge cases and potential failure modes.
10. Consider a phased rollout or feature flag to gradually introduce the compact mode to users.

This high-level design document provides a narrative overview of the compact search/replace feature, explaining the current and proposed workflows, detailing the components affected, and outlining the implementation plan. It also highlights important considerations and potential unknowns that should be addressed during development.
