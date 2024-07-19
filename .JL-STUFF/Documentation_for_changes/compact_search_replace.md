# Compact Search/Replace Blocks Implementation Brief

## Overview

Implement a token-efficient approach for search and replace blocks as an optional feature in the aider codebase. This feature will allow for more efficient communication between the AI and the program while maintaining the user-friendly full-text representation for human interaction.

## Key Features

1. **Toggle command**: Implement a new system command (e.g., `/compact_sr`) to switch between standard and compact search/replace modes.
2. **Compact representation**: Develop a format for the AI to output compact search/replace instructions using efficient references.
3. **Interpretation and expansion**: Create functionality to interpret the compact format and expand it into full SEARCH/REPLACE blocks for user display and application.
4. **Verification mechanism**: Implement a multi-point verification system to ensure accuracy of replacements.

## Implementation Details

### 1. Compact Representation Format

The compact format will consist of:

- The first line of the code block to be replaced
- The last line of the code block to be replaced
- The number of lines between the first and last line
- The replacement code

Example: `["def get_all_commit_hashes_since_tag(tag):", 6, "        return commit_hashes", "replacement code here"]`

### 2. Verification Mechanism

The verification process will include:

- Checking the presence of the first line
- Checking the presence of the last line
- Verifying the total number of lines
- Ensuring the identified block is unique within the file

### 3. Git Integration

- Implement a check for uncommitted changes in the target file before applying S/R blocks
- Notify the AI if there are uncommitted changes that might affect the edit

### 4. Error Handling and Fallback

- If a compact block is not unique or cannot be applied, fall back to manual editing
- Provide clear error messages to the AI and user about why a compact edit failed

### 5. User Interface

- Expand compact blocks into full S/R blocks for user display
- Provide an option to view the compact representation for advanced users

## Implementation Steps

1. Modify `EditBlockCoder` class in `aider/coders/editblock_coder.py`:
   - Add `compact_mode` flag
   - Implement `toggle_compact_mode` method
   - Update `get_edits` to handle both compact and standard modes
   - Implement `find_compact_blocks` method
   - Update `apply_edits` to handle compact edits
   - Implement `apply_compact_edits` method
   - Implement `expand_compact_block` method

2. Update `commands.py` to add the `/compact_sr` command

3. Modify `GitRepo` class in `repo.py` to check for uncommitted changes

4. Update AI prompts in `editblock_prompts.py` to include instructions for compact mode

5. Implement error handling and fallback mechanisms

6. Update user documentation to explain the new compact mode feature

## Next Steps

1. Implement the core changes in `EditBlockCoder`
2. Add the `/compact_sr` command
3. Implement Git integration for change detection
4. Update AI prompts
5. Implement error handling and fallback mechanisms
6. Update user documentation
7. Conduct thorough testing, including edge cases and potential failure modes
8. Consider a phased rollout or feature flag to gradually introduce the compact mode to users

## Open Questions and Considerations

1. How will we measure the actual token savings and performance improvements?
2. How do we ensure this feature doesn't break existing functionality?
3. How do we best educate users about this new feature and its potential benefits/drawbacks?
4. Will this work consistently across different AI models and versions?
5. How do we efficiently handle very large files in the compact format?
6. How do we handle multi-file edits in compact mode?
