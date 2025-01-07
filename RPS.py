# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

"""
 MY FIRST ALMOST ACCEPTED SOLUTION
======================================================================
STRATEGY:
If the opponent has played more than X times, I will predict the next move based on the last X moves of the opponent.
The prediction will be based on the most common next move given the last X moves of the opponent.
X in the code is GROUP_SIZE which based on experiment provides the best results when the value is 3.

RESULT:
Final results: {'p1': 995, 'p2': 1, 'tie': 4}
Player 1 win rate: 99.8995983935743%
Final results: {'p1': 465, 'p2': 299, 'tie': 236}
Player 1 win rate: 60.86387434554974%
Final results: {'p1': 540, 'p2': 195, 'tie': 265}
Player 1 win rate: 73.46938775510205%
Final results: {'p1': 700, 'p2': 212, 'tie': 88}
Player 1 win rate: 76.75438596491229%

Testing game against abbey...
Final results: {'p1': 362, 'p2': 441, 'tie': 197}
Player 1 win rate: 45.08094645080946%
FTesting game against kris...
Final results: {'p1': 454, 'p2': 231, 'tie': 315}
Player 1 win rate: 66.27737226277372%
.Testing game against mrugesh...
Final results: {'p1': 720, 'p2': 236, 'tie': 44}
Player 1 win rate: 75.31380753138075%
.Testing game against quincy...
Final results: {'p1': 998, 'p2': 1, 'tie': 1}
Player 1 win rate: 99.8998998998999%
.
======================================================================
FAIL: test_player_vs_abbey (test_module.UnitTests.test_player_vs_abbey)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/hagairajasinulingga/Documents/Project/FreeCodeCamp/boilerplate-rock-paper-scissors/test_module.py", line 19, in test_player_vs_abbey
    self.assertTrue(
AssertionError: False is not true : Expected player to defeat abbey at least 60% of the time.

----------------------------------------------------------------------
Ran 4 tests in 3.985s

FAILED (failures=1)
"""
def player_weak(prev_play, opponent_history=[]):
    if prev_play: opponent_history.append(prev_play)
    GROUP_SIZE = 3
    guess = "R"
    if len(opponent_history) > GROUP_SIZE:
        mapping = {}
        for i in range(len(opponent_history)-GROUP_SIZE-1):
            pattern = "".join(opponent_history[i:i+GROUP_SIZE])
            if pattern not in mapping:
                mapping[pattern] = {"R": 0, "P": 0, "S": 0}
            mapping[pattern][opponent_history[i+GROUP_SIZE]] += 1

        cur_pattern = "".join(opponent_history[-GROUP_SIZE:])
        if cur_pattern in mapping:
            cur_map = mapping[cur_pattern]
            options = []
            for option in cur_map:
                options.append((cur_map[option], option))
            options.sort()
            guess = options[-1][1]

    counter = {"R": "P", "P": "S", "S": "R"}
    return counter[guess]

"""
 MY ACCEPTED SOLUTION :D
======================================================================
STRATEGY:
This one generalizes the previous solution by predicting the next move based on the last X-Y moves of the opponent.
I view this as attention mechanism where the model will pay attention to the last T moves of the opponent and predict the next move based on the most common next move given the last T moves of the opponent.
I experimented with different values of X and Y with X is the lower bound and Y is the upper bound of the attention size T.
I also setup different point for each attention size and incentivize more on the longer attention size in order to beat opponent that decides the next move based on a longer history.
I haven't rigorously tested all the possibilites, but using X as 3 and Y as 8 using this strategy has provided a good balance between speed and winrate.

RESULT:
Final results: {'p1': 995, 'p2': 1, 'tie': 4}
Player 1 win rate: 99.8995983935743%
Final results: {'p1': 474, 'p2': 266, 'tie': 260}
Player 1 win rate: 64.05405405405405%
Final results: {'p1': 903, 'p2': 55, 'tie': 42}
Player 1 win rate: 94.258872651357%
Final results: {'p1': 856, 'p2': 137, 'tie': 7}
Player 1 win rate: 86.20342396777441%

Testing game against abbey...
Final results: {'p1': 495, 'p2': 277, 'tie': 228}
Player 1 win rate: 64.11917098445595%
.Testing game against kris...
Final results: {'p1': 991, 'p2': 4, 'tie': 5}
Player 1 win rate: 99.59798994974875%
.Testing game against mrugesh...
Final results: {'p1': 856, 'p2': 143, 'tie': 1}
Player 1 win rate: 85.68568568568568%
.Testing game against quincy...
Final results: {'p1': 999, 'p2': 0, 'tie': 1}
Player 1 win rate: 100.0%
.
----------------------------------------------------------------------
Ran 4 tests in 6.930s

OK
"""
def player(prev_play, opponent_history=[]):
    if prev_play: opponent_history.append(prev_play)
    guess = "R"
    if len(opponent_history) > 3:
        oh = "".join(opponent_history)
        options = {"R": 0, "P": 0, "S": 0}
        for attention_size in range(3, 8):
            pattern = oh[-attention_size:]
            point = 2**(attention_size-3)
            for i in range(len(oh)-attention_size):
                if oh[i:i+attention_size] == pattern:
                    options[oh[i+attention_size]] += point
        guess = max(options, key=options.get)

    counter = {"R": "P", "P": "S", "S": "R"}
    return counter[guess]

