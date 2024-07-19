# Proposed Changes for Compact Search/Replace Implementation

## 1. Add `compact_mode` Flag

- **Location**: `EditBlockCoder` class in `aider/coders/editblock_coder.py`
- **Details**:
  - Add class variable `compact_mode = False`
  - **Rationale**: Allows toggling between standard and compact search/replace modes.

## 2. Modify `get_edits` Method

- **Location**: `EditBlockCoder` class in `aider/coders/editblock_coder.py`
- **Current Behavior**: Uses `find_original_update_blocks` to parse edits.
- **Proposed Change**:
  def get_edits(self):
      content = self.partial_response_content
      if self.compact_mode:
          edits = list(find_compact_blocks(content))
      else:
          edits = list(find_original_update_blocks(content, self.fence))
      return edits
- **Reasoning**: Supports both compact and standard formats, maintaining backward compatibility.

## 3. Update `apply_edits` Method

- **Location**: `EditBlockCoder` class in `aider/coders/editblock_coder.py`
- **Current Behavior**: Uses `do_replace` to apply edits.
- **Proposed Change**:
  def apply_edits(self, edits):
      for edit in edits:
          if self.compact_mode:
              self.do_compact_replace(*edit)
          else:
              self.do_replace(*edit)
- **Rationale**: Ensures the appropriate replacement function is used based on the active mode.

## 4. Implement `find_compact_blocks` Function

- **Location**: `aider/coders/editblock_coder.py`
- **Details**:
  - Parses compact format edits using regex.
  - Extracts file path, line numbers, and replacement text.
  - **Example**:
    def find_compact_blocks(content):
        pattern = r'(\S+):(\d+)-(\d+)\n((?:.*\n)*?)\n'
        for match in re.finditer(pattern, content):
            yield match.group(1), int(match.group(2)), int(match(3)), match.group(4)
- **Reasoning**: Essential for interpreting and applying compact edits.

## 5. Implement `do_compact_replace` Function

- **Location**: `aider/coders/editblock_coder.py`
- **Details**:
  - Replaces specified lines in file content with provided replacement text.
  - **Example**:
    def do_compact_replace(self, file_path, start_line, end_line, replacement_text):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines[start_line-1:end_line] = replacement_text.splitlines(True)
        with open(file_path, 'w') as file:
            file.writelines(lines)
- **Rationale**: Performs efficient edits by directly targeting specific line ranges.

## 6. Update Error Messages and Logging

- **Location**: `apply_edits` method in `EditBlockCoder` class
- **Current Behavior**: Error messages are generic.
- **Proposed Change**:
  try:
      if self.compact_mode:
          self.do_compact_replace(*edit)
      else:
          self.do_replace(*edit)
  except ValueError as e:
      mode = "compact" if self.compact_mode else "standard"
      self.io.tool_error(f"Error applying {mode} edit: {str(e)}")
- **Reasoning**: Clear error messages help identify issues specific to each mode.

## 7. Add `/compact_sr` Command

- **Location**: `Commands` class in `aider/commands.py`
- **Details**:
  - Toggles `compact_mode` in `EditBlockCoder`.
  - **Example**:
    def cmd_compact_sr(self, args):
        "Toggle compact search/replace mode"
        self.coder.compact_mode = not self.coder.compact_mode
        mode = "enabled" if self.coder.compact_mode else "disabled"
        self.io.tool_output(f"Compact search/replace mode {mode}")
- **Rationale**: Provides users control over the mode, allowing easy switching.

## 8. Update AI Prompts

- **Location**: `EditBlockPrompts` class in `aider/coders/editblock_prompts.py`
- **Current Behavior**: Describes standard search/replace format.
- **Proposed Change**:
    compact_format_instruction = """
    When compact mode is active, use the following format for edits:
    filename:start_line-end_line
    replacement text
    """
- **Reasoning**: Guides AI to use the correct format based on the active mode.

## 9. Implement Logging and Metrics

- **Location**: `aider/coders/editblock_coder.py`
- **Details**:
  - Logs compact mode usage.
  - Tracks metrics like token savings and processing time.
  - **Example**:
    import time

    def apply_edits(self, edits):
        start_time = time.time()
        total_tokens = 0
        for edit in edits:
            if self.compact_mode:
                total_tokens += self.count_compact_tokens(edit)
            else:
                total_tokens += self.count_standard_tokens(edit)
            # Apply edit...
        end_time = time.time()
        self.log_edit_metrics(self.compact_mode, total_tokens, end_time - start_time)
- **Rationale**: Evaluates the effectiveness of compact mode and identifies areas for further optimization.

## 10. Create Unit Tests

- **Location**: `tests/test_editblock_coder.py`
- **Details**:
  - Tests for `find_compact_blocks`, `do_compact_replace`, and updated methods.
  - **Example**:
    def test_find_compact_blocks():
        content = "file.py:10-15\nnew content\nhere\n"
        blocks = list(find_compact_blocks(content))
        assert len(blocks) == 1
        assert blocks[0] == ("file.py", 10, 15, "new content\nhere\n")
- **Rationale**: Ensures reliability and correctness of the new features, catching regressions and verifying expected behavior.