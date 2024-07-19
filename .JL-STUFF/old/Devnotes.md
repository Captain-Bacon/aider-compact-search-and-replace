# Devnotes

## Editing Original Files

To maintain the stability of the existing system, we should avoid editing the original files unless absolutely necessary. Changes to logging, displays, or any other existing functionality should only be made if they are essential due to the new changes we've implemented. Unnecessary modifications can introduce errors and complexities to a system that is already functioning correctly.

If we identify areas that could benefit from improvements, these should be documented in a separate list of potential upgrades. These upgrades should be addressed only after the current upgrade is working flawlessly. This approach allows us to focus on the new functionality while preserving the stability of the existing system.

### Potential Upgrades List

- add stuff here

## Logging and Output in Aider

Aider uses different methods for logging and output depending on the context and purpose:

1. User-Facing Output:
   For messages that should be displayed to the user, use:
   - `self.io.tool_output(message)` for general information
   - `self.io.tool_error(message)` for error messages

   Example:

   ```python
   self.io.tool_output("Successfully parsed compact block for file: example.py")
   self.io.tool_error("Failed to parse compact block: invalid format")
   ```

   These methods are typically used in user-interactive parts of the code or for important status updates.

2. Internal Logging:
   For internal debugging or detailed logging that isn't typically shown to users, consider using Python's built-in `logging` module:

   ```python
   import logging

   logging.debug("Detailed debug information")
   logging.info("General information")
   logging.warning("Warning message")
   logging.error("Error message")
   ```

   This approach is useful for developer-focused logging that can be enabled or disabled as needed.

3. When to Use Each:
   - Use `self.io.tool_output` and `self.io.tool_error` for information that is directly relevant to the user's current operation or task.
   - Use `logging` for internal details that are primarily useful for debugging or monitoring the application's behavior.

4. Configuration:
   - The visibility and handling of `self.io.tool_output` and `self.io.tool_error` messages are typically configured in the IO class.
   - Logging levels and output for the `logging` module can be configured separately, allowing for more flexible control over internal logging.

Remember to choose the appropriate method based on the intended audience and the importance of the information being logged or displayed.
