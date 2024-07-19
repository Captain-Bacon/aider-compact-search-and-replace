# Compact Search/Replace Blocks Implementation Brief

## Overview

Implement a token-efficient approach for search and replace blocks as an optional feature in the aider codebase. This feature will allow for more efficient communication between the AI and the program while maintaining the user-friendly full-text representation for human interaction.

## Key Features

1. **Toggle command**: Implement a new system command (e.g., `/compact_sr`) to switch between standard and compact search/replace modes.
2. **Compact representation**: Develop a format for the AI to output compact search/replace instructions using efficient references.
3. **Interpretation and expansion**: Create functionality to interpret the compact format and expand it into full SEARCH/REPLACE blocks for user display and application.
4. **Verification mechanism**: Implement a checksum or hash-based verification system to ensure accuracy of replacements.

## Implementation Considerations

### 1. Code Ingestion and AI Representation

- Modify how code is initially processed and presented to the AI.
- Create a mapping between line numbers and content, or generate unique identifiers for code blocks.

### 2. Error Handling

- Update the error handling system to work with references instead of direct text matches.
- Provide context when a reference doesn't match, including surrounding lines.

### 3. Verification Mechanism

- Implement a checksum or hash of the block contents.
- Include the first and last lines of the block to be replaced as a built-in verification mechanism.

### 4. AI Prompt Updates

- Instruct the AI on how to generate compact references.
- Update prompts to include examples of the new format.

### 5. Parsing and Interpretation

- Create new functions to parse the compact format and expand it into full SEARCH/REPLACE blocks.

### 6. User Interface

- Update the UI to display both compact and expanded versions of edits.

### 7. Version Control Integration

- Consider how this change affects integration with version control systems.

### 8. Performance Considerations

- Measure the impact on processing time and memory usage, especially for large files.

### 9. Backwards Compatibility

- Implement a way to switch between compact and standard modes to maintain compatibility with existing workflows.

### 10. Testing Framework

- Develop comprehensive tests for the new functionality, including edge cases and potential failure modes.

## Implementation Steps

### 1. Core Changes

- Modify `EditBlockCoder` class to include compact mode functionality.
- Update `get_edits`, `apply_edits`, and implement new functions for compact parsing.

### 2. Supporting Changes

- Update `Coder` base class in `base_coder.py` to support compact mode.
- Modify `InputOutput` class in `io.py` to handle displaying compact vs. expanded edits.
- Add `/compact_sr` command in `commands.py`.
- Update `main.py` to initialize the compact mode flag.
- Modify `models.py` to update code representation in the model context.
- Update `GitRepo` class in `repo.py` to handle compact references in version control operations.
- Add utility functions in `utils.py` for handling compact references and checksums.
- Update `sendchat.py` to handle sending compact references in chat messages.
- Modify prompts in `editblock_prompts.py` to include instructions for compact mode.

### 3. Testing and Documentation

- Create new test files or update existing ones to cover the new functionality.
- Update user documentation to explain the new compact mode feature.

## Next Steps

1. Review and refine this implementation plan.
2. Prioritize implementation steps based on dependencies and complexity.
3. Begin with a proof-of-concept implementation of key components, starting with the `EditBlockCoder` class.
4. Implement and test each component separately before integrating them into the main codebase.
5. Conduct thorough testing, including edge cases and potential failure modes.
6. Update documentation and user guides to reflect the new functionality.
7. Consider a phased rollout or feature flag to gradually introduce the compact mode to users.

## Open Questions and Considerations

1. What is the most efficient yet unambiguous format for the compact representation?
2. How do we handle potential mismatches due to file changes between AI response and application?
3. How will we measure the actual token savings and performance improvements?
4. How do we ensure this feature doesn't break existing functionality?
5. How do we best educate users about this new feature and its potential benefits/drawbacks?
6. Will this work consistently across different AI models and versions?
7. How do we efficiently handle very large files in the compact format?
8. What are the security implications of using checksums or hashes for verification?
9. How do we handle multi-file edits in compact mode?
10. Should we implement a fallback mechanism if compact mode fails or causes errors?
