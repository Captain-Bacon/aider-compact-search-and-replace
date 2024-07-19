# Compact Search/Replace Blocks Implementation Brief

## Overview

Implement a token-efficient approach for search and replace blocks as an optional feature in the aider codebase. This feature will allow for more efficient communication between the AI and the program while maintaining the user-friendly full-text representation for human interaction.

## Key Features

1. **Toggle command**: Implement a new system command (e.g., `/compact_sr`) to switch between standard and compact search/replace modes.
2. **Compact representation**: Develop a format for the AI to output compact search/replace instructions (e.g., using line numbers or other efficient references).
3. **Interpretation and expansion**: Create functionality to interpret the compact format and expand it into full SEARCH/REPLACE blocks for user display and application.

## Implementation Steps

### 1. Command Implementation

- Add a new boolean flag to track the compact mode state.
- Implement the `/compact_sr` command to toggle this flag.
- Modify the AI prompt generation to include instructions for compact output when the flag is set.

### 2. AI Output Modification

- Update AI instructions to generate compact search/replace instructions when in compact mode.
- Define a clear and consistent format for the compact representation (e.g., `FILE:start_line-end_line:replacement_text`).

### 3. Parsing and Interpretation

- Modify `find_original_update_blocks` function to recognize and parse the compact format.
- Implement a new function to expand compact representations into full SEARCH/REPLACE blocks.

### 4. User Interface Updates

- Update the echo/display logic to show full SEARCH/REPLACE blocks to the user, regardless of the internal representation.

### 5. Application Logic

- Modify `do_replace` function to work with both standard and compact formats.

### 6. Testing and Validation

- Develop unit tests for new functions and modified existing functions.
- Perform integration testing to ensure compatibility with existing features.

## Considerations and Questions

1. **Format Specification**: What's the most efficient yet unambiguous format for the compact representation?
2. **Error Handling**: How should we handle potential mismatches due to file changes between AI response and application?
3. **Performance Metrics**: How will we measure the actual token savings and performance improvements?
4. **Backwards Compatibility**: How do we ensure this feature doesn't break existing functionality?
5. **User Education**: How do we inform users about this new feature and its potential benefits/drawbacks?
6. **AI Model Compatibility**: Will this work consistently across different AI models and versions?
7. **Large File Handling**: How do we efficiently handle very large files in the compact format?

## Next Steps

1. Review and refine this brief.
2. Prioritize implementation steps.
3. Begin with a proof-of-concept implementation of key components.
4. Iterate based on testing and feedback.
