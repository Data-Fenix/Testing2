

*- WORK IN PROGRESS -*

# Linux Screen

Linux screen is a terminal multiplexer utility that allows you to create and manage multiple terminal sessions within a single shell session. It provides several advantages for managing remote virtual machines and running processes:

1. **Session Persistence:** Screen allows you to create terminal sessions that can be detached and reattached at will. This is particularly useful for remote virtual machines, as it ensures that your processes continue running even if your SSH connection is interrupted. You can simply reattach to the existing screen session later.

2. **Multi-Tasking:** With screen, you can run multiple terminal sessions within a single SSH connection, making it easier to manage multiple processes on your remote virtual machines simultaneously. This is especially beneficial for multitasking and monitoring various tasks without opening multiple SSH connections.

3. **Collaboration:** When working on remote virtual machines with colleagues or team members, you can share your screen sessions, allowing others to view or even collaborate on tasks being performed within the same terminal session.

4. **Script Execution:** Screen can be used to run long-duration or resource-intensive scripts in the background on your remote virtual machines, ensuring they continue to execute even after you log out.

In summary, Linux screen is a valuable tool for remote virtual machine management as it enhances session persistence, facilitates multitasking, and promotes collaboration, making it an efficient and convenient solution for running and monitoring processes on remote virtual machines.


### starting a screen session
`screen -S my_session_name`

### detaching from a screen session
`ctrl + a + d`

### current shortcuts
`Ctrl+a c` Create a new window (with shell). \
`Ctrl+a "` List all windows. \
`Ctrl+a 0` Switch to window 0 (by number). \
`Ctrl+a A` Rename the current window. \
`Ctrl+a S` Split current region horizontally into two regions. \
`Ctrl+a |` Split current region vertically into two regions. \
`Ctrl+a tab` Switch the input focus to the next region. \
`Ctrl+a Ctrl+a` Toggle between the current and previous windows \
`Ctrl+a Q `Close all regions but the current one. \
`Ctrl+a X` Close the current region \