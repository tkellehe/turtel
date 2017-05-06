This is just to show off the box move expression.

    bx8¤ḷ¢turtelñʂẉt

    bx8¤             # Sets the current turtle's move function.
    bx8              # Generates a function that allows the turtle to move around a 8x8 box.
       ¤             # Takes the parameter provided and makes the current turtle move based off of the box path.
        
        ḷ¢turtelñʂẉt # The main loop that creates the animation.
        ḷ            # Loops the folloing code endlessly.
         ¢           # Clears the current turtle of all text.
          turtelñ    # Writes to the current turtle but does not change its position then prints.
                 ʂ   # Moves the current turtle a single step further along its path.
                  ẉt # Waits for 100 milliseconds.
                     # Implicit end of the loop.
