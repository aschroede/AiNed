# TODO

1. Disable the commit button if there are no dirty dipoles
2. ~~Refactor the existing code to make it clean, organized, and reduce coupling and increase cohesian~~
3. ~~Include a seed value on the random number generator so you always get the same output (deterministic)~~
3. ~~Write unit tests for scenarios where there is only one dirty dipole~~
4. ~~Update code to handle calculations for multiple dirty dipoles~~
6. ~~Make sure you can write sequence of read-writes and states out to a file for comparison with testing guys~~
7. ~~Make a CLI interface~~
   - Initialise parameters
      - Width and height
      - Probability 
      - File location to save output to
      - Specify seed to use
   - Once board is initialised what do I want to do?
      - Visualise in the GUI
      - Pass in a series of writes
10. Make sure you can read in an initial set of values for a grid
8. Make sure you are not allowed to set dipole to unknown
9. ~~Make sure you can write a state to a dipole that is already in that states (blue -> blue, red -> red)~~
10. ~~Make sure results are reproducible with a seed~~
11. Make sure to use only integer values?
12. Clean up reinforce code

# Passing in Writes

## Single Write in a Single Timestep
Pass in a file where the first line is just <br>
``x, y, state;``

## Multiple Writes in a Single Timestep
Do the same as a single write in a timestep but put a semicolon after each dipole write. <br>
``x1, y1, state1; x2, y2, state2; x3, y3, state3``

## Multiple Writes across Multiple Timesteps
Each line of the file represents a new timestep, so one can do the following <br>

``x1, y1, state1; x2, y2, state2; x3, y3, state3`` <br>
``x1, y1, state1; x2, y2, state2; x3, y3, state3`` <br>
``x1, y1, state1; x2, y2, state2; x3, y3, state3``

# Daily Log

## Feb 23
