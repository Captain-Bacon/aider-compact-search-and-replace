# Proposed Changes for Compact Search/Replace Implementation

1. Add a `compact_mode` flag to `EditBlockCoder` class in `aider/coders/editblock_coder.py`:
   - Add a class variable `compact_mode = False`
   - Rationale: This flag will allow us to toggle between the standard and compact search/replace modes. It needs to be a class variable so that it can be accessed and modified by other methods within the class.

2. Modify the `get_edits` method in `EditBlockCoder` class in `aider/coders/editblock_coder.py`:
   - Current behavior: The method only uses `find_original_update_blocks` to parse edits.
   - Proposed change: Add conditional logic to use either `find_compact_blocks` or `find_original_update_blocks` based on `compact_mode`.
   - Example:
     ```python
     def get_edits(self):
         content = self.partial_response_content
         if self.compact_mode:
             edits = list(find_compact_blocks(content))
         else:
             edits = list(find_original_update_blocks(content, self.fence))
         return edits
     ```
   - Reasoning: This change allows the `get_edits` method to handle both compact and standard formats, maintaining backwards compatibility while introducing the new feature.

3. Update the `apply_edits` method in `EditBlockCoder` class in `aider/coders/editblock_coder.py`:
   - Current behavior: The method only uses `do_replace` to apply edits.
   - Proposed change: Add conditional logic to use either `do_compact_replace` or `do_replace` based on `compact_mode`.
   - Example:
     ```python
     def apply_edits(self, edits):
         for edit in edits:
             if self.compact_mode:
                 self.do_compact_replace(*edit)
             else:
                 self.do_replace(*edit)
     ```
   - Rationale: This ensures that the appropriate replacement function is used based on the active mode, allowing for seamless integration of the compact format.

4. Implement `find_compact_blocks` function in `aider/coders/editblock_coder.py`:
   - This new function will parse the compact format edits using regex.
   - It should extract file path, line numbers, and replacement text.
   - Example structure:
     ```python
     def find_compact_blocks(content):
         pattern = r'(\S+):(\d+)-(\d+)\n((?:.*\n)*?)\n'
         for match in re.finditer(pattern, content):
             yield match.group(1), int(match.group(2)), int(match.group(3)), match.group(4)
     ```
   - Reasoning: This new function is essential for interpreting the AI's compact output correctly, enabling the system to understand and apply compact edits.

5. Implement `do_compact_replace` function in `aider/coders/editblock_coder.py`:
   - This function will replace specified lines in file content with provided replacement text.
   - Example structure:
     ```python
     def do_compact_replace(self, file_path, start_line, end_line, replacement_text):
         with open(file_path, 'r') as file:
             lines = file.readlines()
         lines[start_line-1:end_line] = replacement_text.splitlines(True)
         with open(file_path, 'w') as file:
             file.writelines(lines)
     ```
   - Rationale: This function will perform the actual replacements using the compact format, allowing for more efficient edits by directly targeting specific line ranges.

6. Update error messages and logging in `apply_edits` method in `EditBlockCoder` class:
   - Current behavior: Error messages are generic and don't distinguish between edit formats.
   - Proposed change: Modify messages to reflect whether the edit was in compact or standard format.
   - Example:
     ```python
     try:
         if self.compact_mode:
             self.do_compact_replace(*edit)
         else:
             self.do_replace(*edit)
     except ValueError as e:
         mode = "compact" if self.compact_mode else "standard"
         self.io.tool_error(f"Error applying {mode} edit: {str(e)}")
     ```
   - Reasoning: Clear error messages and logging are crucial for debugging and understanding the system's behavior, especially when introducing a new format. This change will help users and developers identify issues specific to each mode.

7. Add `/compact_sr` command to `Commands` class in `aider/commands.py`:
   - Implement a new method to toggle `compact_mode` in `EditBlockCoder`.
   - Example:
     ```python
     def cmd_compact_sr(self, args):
         "Toggle compact search/replace mode"
         self.coder.compact_mode = not self.coder.compact_mode
         mode = "enabled" if self.coder.compact_mode else "disabled"
         self.io.tool_output(f"Compact search/replace mode {mode}")
     ```
   - Rationale: This command provides users with direct control over which mode to use, allowing for flexibility in different scenarios and easy switching between modes.

8. Update AI prompts in `EditBlockPrompts` class in `aider/coders/editblock_prompts.py`:
   - Current behavior: Prompts only describe the standard search/replace format.
   - Proposed change: Add new prompts for compact mode and modify existing prompts to include compact format instructions when appropriate.
   - Example addition:
     ```python
     compact_format_instruction = """
     When compact mode is active, use the following format for edits:
     filename:start_line-end_line
     replacement text
     """
     ```
   - Reasoning: The AI needs to be aware of the compact mode to provide appropriately formatted responses. These updated prompts will guide the AI in using the correct format based on the active mode.

9. Implement logging and metrics for performance tracking in `aider/coders/editblock_coder.py`:
   - Add logging for compact mode usage and track metrics such as token savings and processing time improvements.
   - Example:
     ```python
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
     ```
   - Rationale: This data will help evaluate the effectiveness of the compact mode and identify areas for further optimization. It provides concrete metrics to assess the impact of the new feature.

10. Create unit tests for new functionality in `tests/test_editblock_coder.py`:
    - Add tests for `find_compact_blocks`, `do_compact_replace`, and updated `get_edits` and `apply_edits` methods.
    - Example test case:
      ```python
      def test_find_compact_blocks():
          content = "file.py:10-15\nnew content\nhere\n"
          blocks = list(find_compact_blocks(content))
          assert len(blocks) == 1
          assert blocks[0] == ("file.py", 10, 15, "new content\nhere\n")
      ```
    - Rationale: Comprehensive testing ensures the reliability and correctness of the new compact mode features. These tests will help catch regressions and ensure that both modes work as expected.

This detailed plan provides specific examples and explanations for the core functionality of the compact search/replace feature. It outlines the necessary changes in each relevant file and explains the reasoning behind each modification.
