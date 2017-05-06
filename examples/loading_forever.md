This is to go along with _Noodel_'s very first
[challenge](http://codegolf.stackexchange.com/questions/101289/loading-forever) in which it competed in.
Currently the _Noodel_ script:

    Loading...¤”Ƈḟḋḣ⁺sḷạÇḍq

Which is __23 bytes__ and with _Turtel_ it is the following and is __22 bytes__:

    Loading... Þ|/-\ḟḷñȧẉq

    Loading... Þ           # Places the fixed "Loading... " onto the screen.

                |/-\ḟ      # Makes the stack -> ["|", "/", "-", "\"]

                     ḷñȧẉq # The main animation loop.
                     ḷ     # Endlessly loop the following code.
                      ñ    # Copies the top of the stack to the turtel not moving and prints to the screen.
                       ȧ   # Takes the top of the stack and makes it the bottom.
                        ẉq # Waits for a quarter of a second (250 milliseconds).